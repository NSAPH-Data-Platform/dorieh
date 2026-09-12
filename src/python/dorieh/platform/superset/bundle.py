#  Copyright (c) 2026. Harvard University
#
#  Developed by Research Software Engineering,
#  Faculty of Arts and Sciences, Research Computing (FAS RC)
#  Author: Michael A Bouzinier
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""Re-point a native Superset dashboard bundle onto a target connection,
entirely in memory.

Native bundles bind everything by uuid: charts -> datasets via ``dataset_uuid``,
datasets -> connection via ``database_uuid``, and the dashboard's ``position``
links charts by ``meta.uuid``. NOTHING is bound by name. Re-pointing is therefore:

  - every ``database_uuid`` -> the TARGET connection's uuid (passed in by the
    caller, who looks it up by name on the live instance),
  - every OTHER uuid -> by default PRESERVED, so a re-import (or an
    export->import round-trip) UPDATES the same objects and never duplicates
    them; with ``regenerate=True`` they are rewritten to a deterministic uuid5
    salted by ``salt`` (the connection name), producing an INDEPENDENT copy
    that coexists with the preserved-uuid original -- use that only for a fork
    on a second connection, never for the canonical bundle you export/refresh,
  - reconcile each dashboard position ``meta.uuid`` to the regenerated chart uuid,
  - retitle (optional), relocate the datasets/<db>/ folder, tidy vestigial legacy
    ``params``, and re-emit a databases/<name>.yaml repointed to the target
    (matched by uuid on import, so the existing connection is reused, never
    overwritten -- the masked credentials in it are not used).

``load()`` accepts an unpacked bundle dir (containing metadata.yaml, possibly
nested one level) or a .zip. ``to_zip_bytes()`` produces an importable bundle.
The on-disk source bundle is never modified.
"""
import io
import os
import re
import uuid
import zipfile

UUID_RE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-"
                     r"[0-9a-f]{4}-[0-9a-f]{12}")
NS = uuid.UUID("6f1a0c4e-0d2b-5e7a-9c3d-000000000000")  # fixed private namespace


def _new_uuid(old, tag):
    return str(uuid.uuid5(NS, "%s:%s" % (tag, old)))


def _find_root_dir(src):
    if os.path.exists(os.path.join(src, "metadata.yaml")):
        return src
    for name in sorted(os.listdir(src)):
        p = os.path.join(src, name)
        if os.path.isdir(p) and os.path.exists(os.path.join(p, "metadata.yaml")):
            return p
    return src


def _zip_root(names):
    for n in names:
        if n.endswith("metadata.yaml"):
            return n[:-len("metadata.yaml")].rstrip("/")
    return ""


def load(src):
    """Return {posix_relpath: text} for the files under a bundle dir or .zip."""
    files = {}
    if os.path.isdir(src):
        root = _find_root_dir(src)
        for dp, _, fs in os.walk(root):
            for f in fs:
                p = os.path.join(dp, f)
                rel = os.path.relpath(p, root).replace(os.sep, "/")
                with open(p, encoding="utf-8") as fh:
                    files[rel] = fh.read()
    else:
        with zipfile.ZipFile(src) as z:
            names = z.namelist()
            top = _zip_root(names)
            prefix = (top + "/") if top else ""
            for n in names:
                if n.endswith("/") or not n.startswith(prefix):
                    continue
                files[n[len(prefix):]] = z.read(n).decode("utf-8")
    return files


def _tidy_params(text, new_db_name):
    """Drop vestigial legacy params (remote_id/import_time) and fix the
    cosmetic database_name in chart ``params:`` blocks. Binding is uuid-based,
    so this is purely so the imported files read coherently."""
    out = []
    for ln in text.splitlines(keepends=True):
        s = ln.rstrip("\n")
        if re.fullmatch(r"  remote_id: .*", s) or re.fullmatch(r"  import_time: .*", s):
            continue
        m = re.fullmatch(r"(  database_name: ).*", s)
        if m:
            out.append(m.group(1) + new_db_name + "\n")
            continue
        out.append(ln)
    return "".join(out)


def repoint(files, *, target_db_uuid, target_db_name, title=None, salt=None,
            regenerate=False):
    """Transform an in-memory bundle (from load()) onto the target connection.

    By default object uuids are PRESERVED (idempotent: re-import updates the
    same objects). Pass regenerate=True to rewrite every non-database uuid to a
    deterministic uuid5 salted by ``salt`` (default: target_db_name), yielding
    an independent coexisting copy. Returns a new {posix_relpath: text} dict."""
    salt = salt or target_db_name

    src_db_uuids = set()
    for rel, text in files.items():
        if rel.startswith("databases/"):
            src_db_uuids.update(UUID_RE.findall(text))

    obj_prefixes = ("charts/", "datasets/", "dashboards/")
    all_uuids = set()
    for rel, text in files.items():
        if rel.startswith(obj_prefixes):
            all_uuids.update(UUID_RE.findall(text))

    # database uuid always repointed; other uuids preserved unless regenerating
    subs = {}
    for u in all_uuids:
        if u in src_db_uuids:
            subs[u] = target_db_uuid
        elif regenerate:
            subs[u] = _new_uuid(u, salt)

    def apply_subs(text):
        for old, new in subs.items():
            text = text.replace(old, new)
        return text

    # chartId -> regenerated chart uuid, to fix the dashboard position layout
    chartid_to_newuuid = {}
    for rel, text in files.items():
        if not rel.startswith("charts/"):
            continue
        fname = rel.split("/")[-1]
        try:
            cid = int(fname.rsplit("_", 1)[1].split(".")[0])
        except (IndexError, ValueError):
            continue
        m = re.search(r"^uuid:\s*(\S+)", text, re.M)
        if m:
            chartid_to_newuuid[cid] = subs.get(m.group(1), m.group(1))

    def fix_positions(text):
        def repl(mo):
            block = mo.group(0)
            cid = re.search(r"chartId:\s*(\d+)", block)
            if not cid:
                return block
            nid = chartid_to_newuuid.get(int(cid.group(1)))
            if not nid:
                return block
            return re.sub(r"(uuid:\s*)\S+", r"\g<1>" + nid, block)
        return re.sub(r"    meta:\n(?:      .*\n)+", repl, text)

    out = {}
    for rel, text in files.items():
        if rel == "metadata.yaml":
            out[rel] = text
            continue
        if rel.startswith("databases/"):
            continue  # re-emitted below
        text = _tidy_params(apply_subs(text), target_db_name)
        if rel.startswith("dashboards/"):
            if title is not None:
                text = re.sub(r"^dashboard_title: .*$",
                              "dashboard_title: " + title, text,
                              count=1, flags=re.M)
            text = fix_positions(text)
        elif rel.startswith("datasets/"):
            parts = rel.split("/")
            if len(parts) >= 3:                  # datasets/<db>/file.yaml
                parts[1] = target_db_name
                rel = "/".join(parts)
        out[rel] = text

    for rel, text in files.items():              # re-emit one databases/ file
        if rel.startswith("databases/"):
            dbtext = text
            for u in src_db_uuids:
                dbtext = dbtext.replace(u, target_db_uuid)
            dbtext = re.sub(r"^database_name: .*$",
                            "database_name: " + target_db_name, dbtext,
                            count=1, flags=re.M)
            out["databases/%s.yaml" % target_db_name] = dbtext
            break
    return out


def to_zip_bytes(files, top="bundle"):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for rel in sorted(files):
            z.writestr("%s/%s" % (top, rel), files[rel])
    return buf.getvalue()

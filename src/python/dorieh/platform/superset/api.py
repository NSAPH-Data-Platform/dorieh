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

"""Standard-library-only Apache Superset REST API client.

No third-party dependencies. Auth: POST /api/v1/security/login returns a JWT;
the import endpoint also needs the CSRF token (GET /api/v1/security/csrf_token/)
and a Referer header.
"""
import http.cookiejar
import json
import urllib.error
import urllib.parse
import urllib.request
import uuid as _uuid


def _opener():
    cj = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))


def multipart(fields, files):
    """fields: dict[str,str]; files: list[(name, filename, bytes, ctype)]."""
    boundary = "----sb" + _uuid.uuid4().hex
    crlf = b"\r\n"
    buf = []
    for k, v in fields.items():
        buf += [b"--" + boundary.encode(),
                ('Content-Disposition: form-data; name="%s"' % k).encode(),
                b"", str(v).encode()]
    for name, fname, data, ctype in files:
        buf += [b"--" + boundary.encode(),
                ('Content-Disposition: form-data; name="%s"; filename="%s"'
                 % (name, fname)).encode(),
                ("Content-Type: %s" % ctype).encode(), b"", data]
    buf += [b"--" + boundary.encode() + b"--", b""]
    return crlf.join(buf), "multipart/form-data; boundary=" + boundary


class SupersetClient:
    def __init__(self, base_url):
        self.base = base_url.rstrip("/")
        self.op = _opener()
        self.token = self.csrf = None

    def _req(self, path, *, data=None, headers=None, method=None, timeout=120):
        h = {"Authorization": "Bearer " + self.token} if self.token else {}
        if headers:
            h.update(headers)
        r = urllib.request.Request(self.base + path, data=data,
                                   headers=h, method=method)
        return self.op.open(r, timeout=timeout)

    def login(self, username, password):
        body = json.dumps({"username": username, "password": password,
                           "provider": "db", "refresh": True}).encode()
        r = urllib.request.Request(
            self.base + "/api/v1/security/login", data=body,
            headers={"Content-Type": "application/json"}, method="POST")
        with self.op.open(r, timeout=60) as resp:
            self.token = json.loads(resp.read())["access_token"]
        with self._req("/api/v1/security/csrf_token/") as resp:
            self.csrf = json.loads(resp.read()).get("result")

    def get_database_uuid(self, name):
        """Resolve a connection NAME to its uuid on THIS Superset instance.

        Each instance assigns its own uuid, so callers must look it up by name
        rather than hard-code it."""
        rison = "(filters:!((col:database_name,opr:eq,value:%s)))" % name
        with self._req("/api/v1/database/?q="
                       + urllib.parse.quote(rison, safe="")) as resp:
            result = json.loads(resp.read()).get("result", [])
        if not result:
            raise SystemExit(
                "No Superset connection named %r on %s. Create it first, then "
                "re-run." % (name, self.base))
        db = result[0]
        if db.get("uuid"):
            return db["uuid"]
        with self._req("/api/v1/database/%d" % db["id"]) as resp:
            return json.loads(resp.read())["result"]["uuid"]

    def export_dashboard(self, dashboard_id):
        """Return the native bundle (zip bytes) for one dashboard id."""
        rison = "!(%d)" % dashboard_id
        with self._req("/api/v1/dashboard/export/?q="
                       + urllib.parse.quote(rison, safe="")) as resp:
            return resp.read()

    def import_dashboard_zip(self, zip_bytes, overwrite=True):
        """POST a native bundle to the v1 importer (same code the UI uses; the
        legacy ``superset import-dashboards`` CLI silently drops charts from
        native bundles). Returns (http_status, body_text)."""
        body, ctype = multipart(
            {"overwrite": "true" if overwrite else "false"},
            [("formData", "bundle.zip", zip_bytes, "application/zip")])
        try:
            with self._req("/api/v1/dashboard/import/", data=body,
                           method="POST",
                           headers={"Content-Type": ctype,
                                    "X-CSRFToken": self.csrf or "",
                                    "Referer": self.base + "/"}) as resp:
                return resp.status, resp.read().decode()
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode(errors="replace")

    def _get_json(self, path):
        with self._req(path) as resp:
            raw = resp.read().decode()
        return json.loads(raw) if raw else {}

    def list_all(self, kind):
        """kind in {chart, dataset, dashboard}: return every result dict
        (paginated)."""
        items, page = [], 0
        while True:
            out = self._get_json(
                "/api/v1/%s/?q=(page:%d,page_size:100)" % (kind, page))
            batch = out.get("result", [])
            items.extend(batch)
            if not batch or len(items) >= out.get("count", len(items)):
                break
            page += 1
        return items

    def dashboard_charts(self, dashboard_id):
        """Charts that BELONG to a dashboard (m2m relationship), as result
        dicts with ids. Resolves charts precisely per dashboard, so copies of
        a dashboard that share chart names are not confused with each other."""
        items, page = [], 0
        while True:
            rison = ("(filters:!((col:dashboards,opr:rel_m_m,value:%d)),"
                     "page:%d,page_size:100)" % (dashboard_id, page))
            out = self._get_json(
                "/api/v1/chart/?q=" + urllib.parse.quote(rison, safe=""))
            batch = out.get("result", [])
            items.extend(batch)
            if not batch or len(items) >= out.get("count", len(items)):
                break
            page += 1
        return items

    def bulk_delete(self, kind, ids):
        """Delete many objects of one kind in a single request."""
        if not ids:
            return "nothing to delete"
        q = "q=!(" + ",".join(str(i) for i in ids) + ")"
        try:
            with self._req("/api/v1/%s/?%s" % (kind, q), method="DELETE",
                           headers={"X-CSRFToken": self.csrf or "",
                                    "Referer": self.base + "/"}) as resp:
                out = json.loads(resp.read().decode() or "{}")
            return out.get("message", out)
        except urllib.error.HTTPError as e:
            return "HTTP %d: %s" % (e.code, e.read().decode(errors="replace"))

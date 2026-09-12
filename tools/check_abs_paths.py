#!/usr/bin/env python3
#  Copyright (c) 2026. Harvard University
#
#  Developed by Research Software Engineering,
#  Harvard University Research Computing and Data (RCD) Services.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#           http://www.apache.org/licenses/LICENSE-2.0
#
"""
Reject machine-specific absolute paths before they reach a commit.

Generated documentation has repeatedly ended up committed with absolute
paths of a developer's checkout baked in (see doc/tutorial/climate/mddocs
history). Such files are broken for everyone else and leak the local
filesystem layout. This check refuses them.

Usage:
    tools/check_abs_paths.py          # check files staged for commit
    tools/check_abs_paths.py --all    # check every tracked file (CI mode)

Enable as a pre-commit hook with:  tools/install-hooks.sh
"""

import re
import subprocess
import sys

# Web links are removed from a line before matching: their path components
# are not filesystem locations. file:// is intentionally not included here.
WEB_URL = re.compile(rb"\b(https?|ftp|sftp|ssh|git)://\S+")

# Forbidden everywhere: a path that exists only on one person's machine.
HARD = [
    (re.compile(rb"(file://)?/Users/[A-Za-z0-9._-]+/"),
     "macOS home directory"),
    (re.compile(rb"(file://)?/home/(?!\$|\{|<|USERNAME\b|USER\b|username\b|user\b|airflow/|runner/)"
                rb"[A-Za-z0-9._-]+/"),
     "Linux home directory"),
    (re.compile(rb"\b[A-Za-z]:\\[A-Za-z0-9_. -]{2,}\\"),
     "Windows drive path"),
    (re.compile(rb"/(private/)?var/folders/"),
     "macOS per-user temp directory"),
    (re.compile(rb"/Volumes/"),
     "macOS mounted volume"),
    (re.compile(rb"/(n|net)/[a-z0-9_]+/[a-z0-9_]+/"),
     "cluster/NFS mount"),
]

# Allowed only where the path names a location *inside a container image*
# (or is prose describing one); anywhere else it is a portability bug.
CONTAINER_ONLY = [
    (re.compile(rb"/opt/"), "/opt path outside container context"),
    (re.compile(rb"/tmp/"), "/tmp path outside container context"),
    (re.compile(rb"/usr/local/bin/"), "hardcoded tool location"),
]
# docs/ is the BUILT documentation site (doc-builder branch): its pages
# legitimately render container paths quoted from prose and CWL sources.
# HARD rules still apply there in full.
CONTAINER_DIRS = ("docker/", "src/cwl/", "src/workflows/", "examples/",
                  "docs/")
PROSE_EXT = (".md", ".rst", ".txt")

# Binary or image formats where a path fragment is noise, not a reference;
# this checker itself (its patterns literally contain what it forbids);
# and IDE state, which is a separate policy decision (see git history of
# .idea/runConfigurations: they embed personal interpreter paths).
SKIP_PREFIX = (".idea/", "tools/check_abs_paths.py")
# .svg and .dot are deliberately NOT skipped: in this repository the
# generated diagrams carry clickable URL= / href= references.
SKIP_EXT = (".gz", ".zip", ".png", ".jpg", ".jpeg", ".gif", ".eps", ".pdf",
            ".ipynb", ".fst", ".parquet", ".ico")


def list_files(scan_all: bool):
    if scan_all:
        cmd = ["git", "ls-files", "-z"]
    else:
        cmd = ["git", "diff", "--cached", "--name-only", "-z",
               "--diff-filter=ACMR"]
    out = subprocess.run(cmd, stdout=subprocess.PIPE, check=True).stdout
    return [f.decode("utf-8", "replace") for f in out.split(b"\0") if f]


def content(path: str, scan_all: bool):
    if scan_all:
        try:
            with open(path, "rb") as f:
                return f.read()
        except OSError:
            return None
    # staged mode: check what is actually being committed, not the worktree
    r = subprocess.run(["git", "show", f":{path}"], stdout=subprocess.PIPE)
    return r.stdout if r.returncode == 0 else None


def main():
    scan_all = "--all" in sys.argv
    problems = []
    for path in list_files(scan_all):
        if path.startswith(SKIP_PREFIX) or path.lower().endswith(SKIP_EXT):
            continue
        data = content(path, scan_all)
        if data is None or b"\0" in data[:8192]:
            continue
        in_container_ctx = (path.startswith(CONTAINER_DIRS)
                            or path.lower().endswith(PROSE_EXT))
        checks = list(HARD)
        if not in_container_ctx:
            checks += CONTAINER_ONLY
        for lineno, line in enumerate(data.splitlines(), 1):
            # web links are not filesystem paths: a URL like
            # https://host/net/x/ or .../home/y/ must not trip the check
            # (file:// is deliberately kept)
            stripped = WEB_URL.sub(b"", line)
            for rx, reason in checks:
                if rx.search(stripped):
                    excerpt = line.decode("utf-8", "replace").strip()[:120]
                    problems.append(f"{path}:{lineno}: {reason}: {excerpt}")
                    break
    if problems:
        print("Machine-specific absolute paths found:", file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
        print(f"\n{len(problems)} problem(s). Use paths relative to the "
              "repository (or to the file being written) instead.",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

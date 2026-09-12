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

"""
Import a native Superset dashboard bundle, re-pointed onto a local connection
ON THE FLY (console script: ``import_dashboard``).

Why on the fly: a native bundle binds its datasets to a connection by ``uuid``,
and that uuid is assigned per-instance -- so a committed bundle cannot hard-code
it or it would only import on the machine it was exported from. This tool
instead resolves the connection BY NAME via the REST API, rewrites the bundle
into a throwaway temp zip bound to that uuid, and imports that. The source
bundle on disk is never modified.

By default object uuids are PRESERVED, so the import UPDATES the dashboard the
bundle represents (idempotent: re-importing the same bundle, or an
export->edit->import round-trip, never duplicates charts/datasets). It binds to
the ``DORIEH`` connection unless --connection-name says otherwise.

Use --copy to stand up an INDEPENDENT dashboard on another connection (e.g. a
``DORIEH2`` dev comparison) that coexists with the canonical one: object uuids
are regenerated deterministically per connection name. Do NOT use --copy for the
canonical bundle you export/refresh -- regenerated uuids compound across
export->import cycles and cause duplicates.

Examples::

  import_dashboard path/to/medicare_quality_dashboard
  import_dashboard bundle.zip --connection-name DORIEH2 --copy \\
      --dashboard-name "Medicare Demo Quality Dashboard (DORIEH2 dev)"
  import_dashboard bundle/ --base-url http://localhost:8088/ --username admin
"""
import argparse
import getpass
import json
import os
import sys

from dorieh.platform.superset import bundle as bundle_mod
from dorieh.platform.superset.api import SupersetClient


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="import_dashboard", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bundle",
                    help="Native dashboard bundle to import (a directory "
                         "containing metadata.yaml, or a .zip).")
    ap.add_argument("--connection-name", default="DORIEH",
                    help="Target Superset connection name (default: DORIEH).")
    ap.add_argument("--dashboard-name", default=None,
                    help="Override the dashboard title (default: keep the "
                         "title baked in the bundle).")
    ap.add_argument("--copy", action="store_true",
                    help="Import as an independent copy (regenerate object "
                         "uuids, salted by connection name) that coexists with "
                         "the canonical import. Default preserves uuids and "
                         "updates the canonical dashboard in place.")
    ap.add_argument("--base-url", default="http://localhost:8088/")
    ap.add_argument("--username", default="admin")
    ap.add_argument("--password", default=None, help="Omit to be prompted.")
    ap.add_argument("--no-overwrite", action="store_true",
                    help="Do not overwrite an existing dashboard with the same "
                         "uuid (default: overwrite, i.e. update in place).")
    args = ap.parse_args(argv)

    if not os.path.exists(args.bundle):
        sys.exit("Bundle not found: %s" % args.bundle)

    pw = args.password or getpass.getpass("Superset password: ")
    client = SupersetClient(args.base_url)
    client.login(args.username, pw)

    db_uuid = client.get_database_uuid(args.connection_name)
    print("Connection %r -> uuid %s" % (args.connection_name, db_uuid))

    files = bundle_mod.load(args.bundle)
    out = bundle_mod.repoint(
        files, target_db_uuid=db_uuid, target_db_name=args.connection_name,
        title=args.dashboard_name, salt=args.connection_name,
        regenerate=args.copy)
    zip_bytes = bundle_mod.to_zip_bytes(out)

    code, text = client.import_dashboard_zip(
        zip_bytes, overwrite=not args.no_overwrite)
    print("HTTP", code)
    try:
        print(json.dumps(json.loads(text), indent=2))
    except ValueError:
        print(text)

    if code == 200:
        print("\nSUCCESS: dashboard imported onto connection %r. Open the "
              "Dashboards list in Superset to view it." % args.connection_name)
        return 0
    print("\nImport REJECTED -- the JSON above names the offending file/field.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

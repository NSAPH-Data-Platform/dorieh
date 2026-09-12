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
Export a single Superset dashboard (by id) to a native YAML bundle
(console script: ``export_dashboard``). Examples::

  export_dashboard 6
  export_dashboard 6 --base-url http://localhost:8088/ --out medicare_6.zip \\
      --unpack medicare_6/

Find a dashboard's id from its Superset URL: .../superset/dashboard/<id>/.

To refresh a committed canonical bundle, export with --unpack into a temp dir,
review the diff, then replace the committed bundle with it.
"""
import argparse
import getpass
import sys
import zipfile

from dorieh.platform.superset.api import SupersetClient


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="export_dashboard", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dashboard_id", type=int,
                    help="Dashboard id (from its Superset URL).")
    ap.add_argument("--base-url", default="http://localhost:8088/")
    ap.add_argument("--username", default="admin")
    ap.add_argument("--password", default=None, help="Omit to be prompted.")
    ap.add_argument("--out", default=None,
                    help="Output .zip path (default: dashboard_<id>.zip).")
    ap.add_argument("--unpack", default=None,
                    help="Also extract the bundle into this directory.")
    args = ap.parse_args(argv)

    out = args.out or ("dashboard_%d.zip" % args.dashboard_id)
    pw = args.password or getpass.getpass("Superset password: ")
    client = SupersetClient(args.base_url)
    client.login(args.username, pw)

    blob = client.export_dashboard(args.dashboard_id)
    with open(out, "wb") as fh:
        fh.write(blob)
    print("Wrote %s (%d bytes)" % (out, len(blob)))

    if args.unpack:
        with zipfile.ZipFile(out) as z:
            z.extractall(args.unpack)
        print("Unpacked into %s/" % args.unpack)
    return 0


if __name__ == "__main__":
    sys.exit(main())

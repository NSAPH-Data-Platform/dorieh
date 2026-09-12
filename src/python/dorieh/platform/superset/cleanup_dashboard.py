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
Delete Superset dashboard(s) by title -- AND the charts that belong to them --
via the REST API, so you don't click through per-object DELETE confirmations
(console script: ``cleanup_dashboard``).

HOW TARGETS ARE RESOLVED
------------------------
* Dashboards: matched by EXACT title (--title, and/or the title in --bundle).
* Charts: resolved by MEMBERSHIP of the matched dashboards (queried from the
  API before the dashboards are deleted), NOT by name. This is deliberate:
  independent copies of a dashboard on different connections (e.g. DORIEH vs a
  DORIEH2 dev copy) share chart names like "Enrollments By Year", so matching
  by name would miss or over-delete. Membership matches each copy's own charts.
* Datasets are NOT deleted by default (they represent DB tables/views and are
  typically shared). They are deleted only when named via --bundle, and you
  should scope them with --dataset-connection to avoid hitting another copy.

SAFETY
------
* Dry-run by default: prints exactly what it WOULD delete and stops. Nothing is
  deleted unless you pass --execute.
* Deletes in dependency-safe order: dashboards -> charts -> datasets.

Examples (dry run -- always do this first)::

  cleanup_dashboard --title "Medicare Demo Quality Dashboard (DORIEH2 dev)"
  cleanup_dashboard --title "…" --bundle path/to/bundle --dataset-connection DORIEH2

Then, once the printed list looks correct, append --execute.
"""
import argparse
import getpass
import sys

import yaml

from dorieh.platform.superset import bundle as bundle_mod
from dorieh.platform.superset.api import SupersetClient


def bundle_targets(path):
    """Derive (dashboard titles, dataset (schema, table) keys) from a bundle."""
    files = bundle_mod.load(path)
    titles, datasets = set(), set()
    for rel, text in files.items():
        if rel.startswith("dashboards/"):
            d = yaml.safe_load(text) or {}
            if d.get("dashboard_title"):
                titles.add(d["dashboard_title"])
        elif rel.startswith("datasets/"):
            t = yaml.safe_load(text) or {}
            if t.get("table_name"):
                datasets.add((t.get("schema"), t["table_name"]))
    return titles, datasets


def _ds_connection(d):
    return (d.get("database") or {}).get("database_name")


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="cleanup_dashboard", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--title", action="append", default=[],
                    help="Dashboard title to delete (repeatable).")
    ap.add_argument("--bundle", default=None,
                    help="Native bundle (dir or .zip): also target its "
                         "dashboard title and (with --dataset-connection) its "
                         "datasets.")
    ap.add_argument("--dataset-connection", action="append", default=None,
                    help="Also delete the bundle's datasets, restricted to "
                         "these connection names (repeatable). Without this, "
                         "datasets are left alone.")
    ap.add_argument("--base-url", default="http://localhost:8088/")
    ap.add_argument("--username", default="admin")
    ap.add_argument("--password", default=None, help="Omit to be prompted.")
    ap.add_argument("--execute", action="store_true",
                    help="Actually delete. Without this flag it is a dry run.")
    args = ap.parse_args(argv)

    titles, dataset_keys = set(args.title), set()
    if args.bundle:
        bt, bd = bundle_targets(args.bundle)
        titles |= bt
        dataset_keys |= bd
    if not titles:
        ap.error("specify --title and/or --bundle (no dashboard to match)")

    pw = args.password or getpass.getpass("Superset password: ")
    s = SupersetClient(args.base_url)
    s.login(args.username, pw)

    dashes = [d for d in s.list_all("dashboard")
              if d.get("dashboard_title") in titles]

    # Charts: by membership of the matched dashboards (resolved BEFORE deletion)
    charts_by_id = {}
    for d in dashes:
        for c in s.dashboard_charts(d["id"]):
            charts_by_id[c["id"]] = c
    charts = list(charts_by_id.values())

    # Datasets: only when explicitly requested via --dataset-connection, and
    # only those named in the bundle, scoped to the given connection(s).
    datasets = []
    if dataset_keys and args.dataset_connection is not None:
        for d in s.list_all("dataset"):
            if (d.get("schema"), d.get("table_name")) not in dataset_keys:
                continue
            if _ds_connection(d) not in args.dataset_connection:
                continue
            datasets.append(d)

    print("\n=== MATCHED OBJECTS ===")
    print("\nDashboards (%d):" % len(dashes))
    for d in dashes:
        print("  [%s] %s" % (d["id"], d["dashboard_title"]))
    print("\nCharts on those dashboards (%d):" % len(charts))
    for c in charts:
        print("  [%s] %s" % (c["id"], c.get("slice_name")))
    print("\nDatasets (%d):" % len(datasets))
    for d in datasets:
        print("  [%s] %s.%s @ %s" % (d["id"], d.get("schema"),
                                     d.get("table_name"), _ds_connection(d)))

    if not args.execute:
        print("\nDRY RUN -- nothing deleted. Re-run with --execute to delete "
              "the objects listed above.")
        return 0

    print("\n=== DELETING (dashboards -> charts -> datasets) ===")
    print("dashboards:", s.bulk_delete("dashboard", [d["id"] for d in dashes]))
    print("charts    :", s.bulk_delete("chart", [c["id"] for c in charts]))
    print("datasets  :", s.bulk_delete("dataset", [d["id"] for d in datasets]))
    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

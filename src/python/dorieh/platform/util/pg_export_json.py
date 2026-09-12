#  Copyright (c) 2024. Harvard University
#
#  Developed by Research Software Engineering,
#  Harvard University Research Computing and Data (RCD) Services.
#
#  Author: Michael A Bouzinier
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#           http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
import gzip
import logging
import os.path
from argparse import Namespace
from dorieh.platform.db import Connection
from dorieh.platform.util.pg_json_dump import dump


def export_json_lines(arguments: Namespace):
    output: str = arguments.output
    table = arguments.table
    if output.lower().endswith(".json.gz") or output.lower().endswith(".jsonl.gz"):
        data_path = output
    elif output.lower().endswith(".json") or output.lower().endswith(".jsonl"):
        data_path = output + ".gz"
    elif not os.path.isdir(output) and '.' in output:
        raise ValueError("Ambiguous output specification")
    else:
        if not os.path.isdir(output):
            os.makedirs(output)
        data_path = os.path.join(output, table) + ".json.gz"
    with Connection(arguments.db, arguments.connection) as db:
        with gzip.open(data_path, "wt") as fd:
            dump(db, table, fd)
    logging.info("Exported table {} to {}.".format(table, data_path))








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
from dorieh.platform import init_logging
from dorieh.platform.util.export_args import parse_args, FORMATS
from dorieh.platform.util.pg_export_hdf5 import export_hdf5
from dorieh.platform.util.pg_export_json import export_json_lines
from dorieh.platform.util.pg_export_parquet import PgPqBase


def export():
    init_logging()
    arguments = parse_args()
    fmt = arguments.format
    if fmt is None:
        pp = arguments.output.split('.')
        for p in pp:
            if p in FORMATS:
                fmt = p
                break
    if fmt is None:
        raise ValueError("Please specify export format")
    if fmt in ["json", "jsonl", "jsonlines"]:
        export_json_lines(arguments)
    elif fmt in ["parquet"]:
        PgPqBase.run(arguments)
    elif fmt in ["hdf5"]:
        export_hdf5(arguments)
    else:
        raise ValueError(f"Format {fmt} is not implemented")


if __name__ == '__main__':
    export()


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
#
from argparse import ArgumentParser, Namespace
import logging


FORMATS = ["parquet", "json", "jsonl", "jsonlines", "csv", "hdf5"]


def parse_args() -> Namespace:
    parser = ArgumentParser (description="Export data to file system")
    parser.add_argument("--format", "-f",
                        help="Format to export to", 
                        choices=FORMATS,
                        default="parquet",
                        required=False)
    parser.add_argument("--sql", "-s",
                        help="SQL Query or a path to a file containing SQL query",
                        required=False)
    parser.add_argument("--schema",
                        help="Export all columns for all tables in the given schema",
                        required=False)
    parser.add_argument("--table", "-t",
                        help="Export all columns a given table (fully qualified name required)",
                        required=False)
    parser.add_argument("--partition", "-p",
                        help="Columns to be used for partitioning",
                        nargs='+',
                        required=False)
    parser.add_argument("--output", "--destination", "-o",
                        help="Path to a directory, where the files will be exported",
                        required=True)
    parser.add_argument("--db",
                        help="Path to a database connection parameters file",
                        default="database.ini",
                        required=True)
    parser.add_argument("--connection", "-c",
                        help="Section in the database connection parameters file",
                        default="nsaph2",
                        required=True)
    parser.add_argument("--batch_size", "-b",
                        help="The size of a single batch",
                        default=2000,
                        type=int,
                        required=False)
    parser.add_argument("--hard",
                        help="Hard partitioning: execute separate SQL statement for each partition",
                        action='store_true'
                        )
    parser.add_argument("--compatibility",
                        help="Make output compatible with specified framework",
                        required=False,
                        choices=["spark"]
                        )
    parser.add_argument("--dryrun",
                        help="Do not perform actual export, just print SQL Query or do a dry run",
                        action='store_true'
                        )

    arguments = parser.parse_args()
    if arguments.sql and arguments.table:
        logging.warning("Both table and sql are provided. SQL will be appended to the Table query.")
    if arguments.sql and arguments.schema:
        raise ValueError("Only one type of argument is accepted: sql or schema")
    elif arguments.table and arguments.schema:
        raise ValueError("Only one type of argument is accepted: sql, schema or table")

    return arguments

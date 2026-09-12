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

from psycopg2.extras import RealDictCursor

from dorieh.platform.db import Connection
from dorieh.platform.requests.hdf5_export import export_dataset
from dorieh.platform.util.pg_json_dump import dump


def export_hdf5(arguments: Namespace):
    output: str = arguments.output
    table = arguments.table
    partitions = arguments.partition
    if output.lower().endswith(".hdf5"):
        data_path = output
    elif not os.path.isdir(output) and '.' in output:
        raise ValueError("Ambiguous output specification")
    else:
        if not os.path.isdir(output):
            os.makedirs(output)
        data_path = os.path.join(output, table) + ".hdf5"
    sql = f"SELECT * FROM {table}"
    if partitions:
        sql += f" ORDER BY {','.join(partitions)}"
    db = None
    try:
        db = Connection(arguments.db, arguments.connection)
        cnxn = db.connect()
        types = db.get_database_types()
        with cnxn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql)
            export_dataset(cursor=cursor, output_file=data_path, name=table, groups=partitions, db_types=types)
        logging.info("Exported table {} to {}.".format(table, data_path))
    finally:
        db.close()









#  Copyright (c) 2025. Harvard University
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

from pyhive import hive
from dorieh.platform.util.spsql import execute, start_session
import os


class HiveImporter:
    def __init__(self, host: str = "127.0.0.1", port: int = 10000, database: str = "hive"):
        self.hive_host = host
        self.hive_port = port
        self.hive_database = database
        self.hive_table_name = 'your_table'
        self.hive_table_location = 'hdfs:///path/to/your/hive/directory'

    def introspect(self, path_to_data: str, name: str):
        spark = start_session()
        sql = f"DESCRIBE TABLE {name}"
        df = execute(spark, path_to_data, sql, name)
        columns = [
            f"{row['col_name']} {row['data_type'].upper()}"
            for row in df.collect()
        ]
        return "\n  ".join(columns)

    def import_table(self, path_to_data: str, name: str, hive_table_location = None):
        if hive_table_location is None:
            hive_table_location = path_to_data
        parquet_schema = self.introspect(path_to_data, name)
        conn = hive.Connection(host=self.hive_host, port=self.hive_port)
        with conn.cursor() as cursor:
            create_table_sql = f"""
            CREATE EXTERNAL TABLE IF NOT EXISTS {self.hive_database}.{name} (
              {parquet_schema}
            )
            STORED AS PARQUET
            LOCATION '{hive_table_location}'
            """

            cursor.execute(create_table_sql)
            cursor.close()


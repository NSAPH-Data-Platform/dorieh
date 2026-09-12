"""
Utility to execute SQL statement or statements taken from
command line arguments over Parquet file(s) using Spark
"""

#  Copyright (c) 2024-2025. Harvard University
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
#
import os
from argparse import ArgumentParser
from typing import Dict

from pyspark.sql import SparkSession, DataFrame


def read_parquet(spark: SparkSession, location: str) -> DataFrame:
    reader = spark.read.option("mergeSchema", "true")
    if os.path.isdir(location):
        content = os.listdir(location)
        partitioned = False
        is_parquet_dir = False
        for f in content:
            if os.path.isdir(os.path.join(location, f)) and '=' in f:
                partitioned = True
                break
            if f.endswith('.parquet'):
                is_parquet_dir = True
                break
        if partitioned:
            reader = reader.option("basePath", location)
            path_to_parquet = os.path.join(location, '*', '*')
        elif is_parquet_dir:
            path_to_parquet = os.path.join(location, '*.parquet')
        else:
            raise ValueError(f"Unknown directory structure: {location}")
    else:
        path_to_parquet = location
    return reader.parquet(path_to_parquet)


def start_session(app_name = None, xmx: str = None, hive = False, config: Dict = None):
    if app_name is None:
        app_name = "Dorieh SparkSQL"
    session_builder = SparkSession.builder.appName(app_name) \
        .config("spark.driver.extraJavaOptions", "--add-exports=java.base/sun.nio.ch=ALL-UNNAMED") \
        .config("spark.executor.extraJavaOptions", "--add-exports=java.base/sun.nio.ch=ALL-UNNAMED")

    if xmx is None:
        xmx = os.environ.get("xmx")
    if xmx:
        session_builder = session_builder.config("spark.driver.memory", xmx).config("spark.executor.memory", xmx)
    cores = os.environ.get("xcores")
    if cores:
        session_builder = session_builder.master(f"local[{cores}]")
    if hive:
        session_builder = session_builder.enableHiveSupport()
    if config:
        for key in config:
            session_builder = session_builder.config(key, config[key])

    session = session_builder.getOrCreate()
    print(session.sparkContext.getConf().getAll())
    return session


def execute(spark: SparkSession, location: str, sql: str, table: str = None) -> DataFrame:
    if table is None:
        table = "parquet_table"
    df = read_parquet(spark, location)
    df.createOrReplaceTempView(table)
    return spark.sql(sql)


def execute_and_show(args):
    spark = start_session()
    sql = ' '.join(args.sql)
    print("Executing: " + sql)
    try:
        result_df = execute(spark, args.location, sql, args.table)
        result_df.show(n=args.n, truncate=False)
    finally:
        spark.stop()


def parse_args():
    parser = ArgumentParser (description="Tool to query Spark SQL Warehouse and/or Parquet files")
    parser.add_argument("--location", "-l", "-p",
                        help="URI or path to file(s) or directory containing data (e.g., in Parquet format). "
                             + "Wildcards are supported",
                        required=True)
    parser.add_argument("--table", "-t",
                        help="Optional table name")
    parser.add_argument("--n", type=int, default=20,
                        help="Number of rows to output, defaults to 20")
    parser.add_argument(dest="sql",
                        nargs='+',
                        help="SQL statement(s)")

    return parser.parse_args()


if __name__ == '__main__':
    arguments = parse_args()
    execute_and_show(arguments)


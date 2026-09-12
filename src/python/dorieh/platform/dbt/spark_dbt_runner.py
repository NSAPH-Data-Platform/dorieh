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
#
from pyspark.sql import SparkSession

from dorieh.platform import init_logging
from dorieh.platform.dbt.dbt_runner import DBTRunner
from dorieh.platform.util.spsql import read_parquet


class SparkDBTRunner(DBTRunner):
    def __init__(self):
        super().__init__()
        self.path_to_parquet = self.context.location
        if not self.path_to_parquet:
            raise ValueError("Parameter `location` is not defined, it is required for Spark")
        if self.context.table:
            self.table: str = self.context.table
            if '.' in self.table:
                self.table = self.table.replace('.', '___')
        else:
            self.table = "parquet_table"


    def run(self):
        spark = SparkSession.builder.appName("Dorieh Spark DBT Runner").getOrCreate()
        try:
            df = read_parquet(spark, self.context.location)
            df.createOrReplaceTempView(self.table)
            for script_file in self.scripts:
                self.run_script(self.form_query(script_file), spark)
        finally:
            spark.stop()

    def run_script(self, query: str, spark: SparkSession):
        if self.table != self.context.table:
            query = query.replace(self.context.table, self.table)
        df = spark.sql(query)
        df.show()
        columns = df.columns
        list_of_rows = df.collect()
        rows = [list(row) for row in list_of_rows]
        self.analyze_results(columns, rows)


if __name__ == '__main__':
    init_logging(name="run-spark-tests")
    runner = SparkDBTRunner()
    runner.test()

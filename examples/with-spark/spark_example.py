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
import os.path
import sys
from typing import List, Dict

from pyspark.sql import SparkSession

from dorieh.platform.util.spsql import read_parquet


def group_by_counts(path_to_parquet: str, group_by: List[str]) -> Dict[str,int]:
    spark = SparkSession.builder.appName("GroupByCountsQuery").getOrCreate()
    try:
        df = read_parquet(spark, path_to_parquet)
        result_df = df.groupBy(group_by).count()
        result_list = result_df.orderBy(group_by).collect()

        result_dict = {
            ','.join(str(row[col]) for col in group_by): row['count']
            for row in result_list
        }

        return result_dict
    finally:
        spark.stop()


def main():
    groups = group_by_counts(sys.argv[1], sys.argv[2:])
    print(groups)


if __name__ == '__main__':
    main()
    
#  Copyright (c) 2021. Harvard University
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

from typing import Dict

import logging

from dorieh.platform import init_logging
from dorieh.platform.db import Connection
from dorieh.platform.loader.common import DBConnectionConfig


class Aggregator:
    QUERY = """
    SELECT
        1 as ORD,
        'cms.ps' as table, 
        COUNT(*) 
    FROM 
        "cms"."ps"
    UNION
    SELECT
        2 as ORD,
        'medicaid.beneficiaries' as table, 
        COUNT(*) 
    FROM 
        "medicaid"."beneficiaries"
    UNION
    SELECT
        3 as ORD,
        'medicaid.enrollments' as table, 
        COUNT(*) 
    FROM 
        "medicaid"."enrollments"
    UNION
    SELECT
        4 as ORD,
        'medicaid.eligibility' as table, 
        COUNT(*) 
    FROM 
        "medicaid"."eligibility"
    ORDER BY 1
    """

    def __init__(self, context: DBConnectionConfig = None):
        init_logging()
        if not context:
            context = DBConnectionConfig(None, __doc__).instantiate()
        self.context = context

    def count(self) -> Dict[str,int]:
        counts = dict()
        with Connection(self.context.db,
                        self.context.connection,
                        silent=True).connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(self.QUERY)
                for row in cursor:
                    table = row[1]
                    n = row[2]
                    logging.info("{}: {:,d}".format(table, n))
                    counts[table] = n
        return counts

    def verify(self, expected):
        actual = self.count()
        for key in expected:
            if expected[key] != actual[key]:
                msg = "Verification failed for {}. " \
                      "Expected: {:,d}; Actual: {:,d}".format(
                    key, expected[key], actual[key]
                )
                raise ValueError(msg)
            logging.debug("{} count OK".format(key))
        logging.info("All counts OK.")


class ExpectedData:
    def __init__(self):
        self.micro_random_counts = {
            'cms.ps': 341233,
            'medicaid.beneficiaries': 313777,
            'medicaid.enrollments': 314272,
            'medicaid.eligibility': 3771264
        }


if __name__ == '__main__':
    Aggregator().verify(ExpectedData().micro_random_counts)

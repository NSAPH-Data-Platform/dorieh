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

import datetime
from typing import Dict

RECORD_NUM_FORMAT = "{:d}-{:010d}"
STATE_CODE = "State Code"
COUNTY_CODE = "County Code"
SITE_NUM = "Site Num"
PARAMETER_CODE = "Parameter Code"
MONITOR = "Monitor"
RECORD = "Record"


def add_record_num(row: Dict, record_index: int):
    year = None
    if "Year" in row:
        year = int(row["Year"])
    else:
        for column in ["Date Local", "UTC"]:
            if column in row:
                dt = datetime.datetime.fromisoformat(row[column])
                year = dt.year
                break
    if not year:
        raise ValueError("No information about year")
    r = RECORD_NUM_FORMAT.format(year, record_index)
    row[RECORD] = r

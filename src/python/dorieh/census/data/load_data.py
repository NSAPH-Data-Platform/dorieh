
#  Copyright (c) 2022. Harvard University
#
#  Developed by Harvard T.H. Chan School of Public Health
#  (HSPH) and Research Software Engineering,
#  Faculty of Arts and Sciences, Research Computing (FAS RC)
#  Author: Ben Sabath (https://github.com/mbsabath)
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
import pandas as pd

DATA_DIR = os.path.dirname(__file__)


def load_county_codes():
    """
    Read in data file listing all counties in the US, with their state and county FIPS codes

    :return: pandas data frame
    """

    file_path = DATA_DIR + os.sep + "county_fips.csv"
    return pd.read_csv(file_path, dtype=str)


def load_state_codes():
    """
    Read in data file listing all states in the US, with their FIPS codes

    :return: pandas data frame
    """

    file_path = DATA_DIR + os.sep + "state_fips.csv"
    return pd.read_csv(file_path, dtype=str)
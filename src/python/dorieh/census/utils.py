"""
utils.py
========================
Census utility functions
"""

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


def show_api_keys():
    """
    Prints out api keys.
    """
    list_of_keys = ['CENSUS_API_KEY']

    for item in list_of_keys:
        if item not in os.environ.keys():
            print(f"Key: {item}, is not defined.")
        else:
            print(f"Key: {item}, Value: {os.environ[item]}")

"""
census_info.py
========================================
Core module for handling census metadata
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
# Code for handling census metadata

import logging
import os

import requests as r

from dorieh.census.exceptions import CensusException

LOG = logging.getLogger(__name__)


def get_endpoint(year: int, dataset: str, sum_file: str = None):
    """
    Returns a string containing the URL to the census API endpoint

    :param year: The year for which you want data
    :param dataset: The census data set you want (dec, acs1, acs5, pums)
    :param sum_file: For the 2000 census, sf1 or sf3
    :return:
    """
    # Questions about where best to fail?
    # Do we throw an error here (or elsewhere while prepping the query

    if dataset not in ['dec', 'acs1', 'acs5']:
        raise CensusException(f"Input dataset ({dataset}) is not currently supported. Supported datasets: dec, acs1, acs5.")

    out = "https://api.census.gov/data/" + str(year) + "/"

    if dataset == 'dec':
        if year not in [2000, 2010]:
            raise CensusException(f"{year} is not valid for decennial census. Valid options: 2000, 2010.")
        out += "dec/"
        if year == 2000:
            if sum_file not in ["sf1", "sf3"]:
                raise CensusException(f"Summary file input ({sum_file}) is not valid. Valid options: sf1, sf3")
            out += sum_file
        else:
            out += "sf1"
    elif dataset in ['acs1', 'acs5']:
        if year <= 2008:
            #TODO: Either the condition or error message is not correct. What if dataset is acs1?
            raise CensusException(f"ACS5 dataset cannot be <= 2008. Curren input: {year}")
        out += "acs/" + dataset
    #elif dataset == 'pums':
    #    assert year > 2008
    #    out += 'acs/acs5/pums'

    return out


def get_varlist(year: int, dataset: str, sum_file: str = None):
    """
    :param year: Year of data
    :param dataset: The census data set you want (dec, acs1, acs5, pums)
    :param sum_file: For the 2000 census, sf1 or sf3
    :return: Dataframe of available variables in a given data set
    """

    try:
        endpoint = get_endpoint(year, dataset, sum_file)
    except CensusException as e:
        print(f"{e}")
        return

    params = {}

    if "CENSUS_API_KEY" in os.environ.keys():
        params['key'] = os.environ["CENSUS_API_KEY"]

    num_tries = 0
    while num_tries < 5:
        try:
            out = r.get(endpoint + "/variables.json", params=params)
            out.raise_for_status()
            break
        except:
            LOG.warning("Varlist Query Failed, re-trying")
            num_tries += 1
    if num_tries >= 5:
        LOG.critical("Unable to complete query after " + str(num_tries) + " tries")
        raise CensusException("Unable to complete varlist query after " + str(num_tries) + " tries")

    out = out.json()
    varnames = list(out['variables'].keys())[3:]

    return varnames


def set_api_key(key: str):
    """
    Sets an environment variable to contain your census API key. To avoid needing to run this
    every session you can also permanently set CENSUS_API_KEY to your key in your environment.

    :param key: Your Census API key as a string
    :return: nothing
    """
    os.environ['CENSUS_API_KEY'] = key


def census_years(min_year: int = 2000, max_year: int = 2019):
    """
    Constructs a list of years for which census data is available in the range provided. At this point assumes we want the decennial census and acs5. Future functionality might expand to allow this to vary.

    :param min_year: minimum year we want data for
    :param max_year: max year we want data for (inclusive)
    :return: list of all years in specified range for which data is available
    """

    out = []
    if min_year <= 2000:
        out.append(2000)

    out = out + list(range(max(min_year, 2009), min(max_year, 2019) + 1))
    return out

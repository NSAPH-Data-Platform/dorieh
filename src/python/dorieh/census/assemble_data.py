"""
assemble_data.py
=======================================
Core module for assembling a census plan
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

import logging

import yaml
import numpy as np
import pandas as pd
import dorieh.utils.qc as qc
import dorieh.utils.interpolation  as interpolation

from .data import *
from .exceptions import CensusException
from .tigerweb import get_area
from .census_info import census_years
from .query import get_census_data, _clean_acs_vars

class DataPlan:
    """
    A class containing information on how to create a desired set of census data.

    Inputs for initializing a DataPlan object from a census yaml document

    :yaml_path: path to a yaml file. Structure defined in :doc:`census_yaml`
    :geometry: which census geography this plan is for
    :years: The list of years to query data from. The census_years() function can calculate which years in your timeframe of interest can be queried for the decennial and 5 year acs data. Note that this may not apply for the ACS1 or other data. That function may be updated in the future, but for now creating lists of years besides the defaults is left as an exercise for the interested reader.
    :state: 2 digit FIPS code of the state you want to limit the query to (i.e. "06" for CA)
    :county: 3 digit FIPS code of the county you want to include. Requires state to be specified

    Members:

    * ``geometry``: which census geography this plan is for
    * ``years``: The ``list`` of years that the data should be queried for
    * ``state``: 2 digit FIPS code of the state you want to limit the query to (i.e. "06" for CA)
    * ``county``: 3 digit FIPS code of the county you want to include. Requires state to be specified
    * ``plan``: A ``dict`` with keys of years, storing lists of ``VariableDef`` objects defining the variables to be calculated for that year. Created from a yaml file. Structure defined in :doc:`census_yaml`
    * ``data``: A pandas data frame created based on the defined data plan. only exists after the ``DataPlan.assemble_data()`` method is called.
    """

    supported_out_formats = ["csv"]

    def __init__(self, yaml_path, geometry, years=census_years(), state=None, county=None):
        """
        initialize a DataPlan object from a census yaml document

        :param yaml_path: path to a yaml file. Structure defined in :doc:`census_yaml`
        :param geometry: which census geography this plan is for
        :param years: The list of years to query data from. The census_years() function can
            calculate which years in your timeframe of interest can be queried for the decennial and
            5 year acs data. Note that this may not apply for the ACS1 or other data. That function may be
            updated in the future, but for now creating lists of years besides the defaults is left as an exercise
            for the interested reader.
        :param state: 2 digit FIPS code of the state you want to limit the query to (i.e. "06" for CA)
        :param county: 3 digit FIPS code of the county you want to include. Requires state to be specified
        """
        self.geometry = geometry
        self.__logger = logging.getLogger(__name__ + ".DataPlan." + self.geometry)
        self.years = years
        if type(self.years) is int:
            self.years = [self.years]
        self.state = state
        self.county = county

        self.plan = dict()
        self._yaml_to_dict(yaml_path)
        self.__has_missing = False

        self.data = pd.DataFrame()

    def _yaml_to_dict(self, yaml_path):
        """
        Convert a yaml file detailing how to get census variables in to a
        dictionary. Handles the issue of forward counting years to make future
        code readable.

        Yaml structure defined in :doc:`census_yaml`

        :param yaml_path:
        :return: dictionary

        """

        # Read in Raw YAML

        with open(yaml_path) as f:
            yaml_dict = yaml.load(f, Loader=yaml.FullLoader)

        for year in self.years:
            self.plan[year] = list()
            for varname in yaml_dict.keys():
                plan_year = _find_year(year, list(yaml_dict[varname].keys()))
                if plan_year is None:
                    continue
                if yaml_dict[varname][plan_year] != "skip":
                    self.plan[year].append(VariableDef(varname,
                     yaml_dict[varname][plan_year], self.__logger))

    def assemble_data(self):
        """
        Create a data frame for each geoid , for each year, with each variable as defined in the data plan

        :return: Assembled data frame stored in self.data
        """

        self.data = None  # Clear in case this has been run previously
        self.__logger.info("Beginning Census Data Acquisition")

        for year in self.years:
            year_data = None
            if len(self.plan[year]) == 0:
                continue

            for var_def in self.plan[year]:
                self.__logger.info("Processing " + str(year) + " " + var_def.name)
                var_data = var_def.calculate_var(year, self.geometry, self.state, self.county)
                join_vars = list(set(var_data.columns).difference([var_def.name]))

                if year_data is None:
                    year_data = pd.DataFrame(columns=join_vars)

                year_data = pd.merge(year_data, var_data, how="outer", on=join_vars)

            if self.data is None:
                self.data = year_data
            else:
                self.data = self.data.append(year_data, ignore_index=True)

    def get_var_names(self):
        """
        Return a list containing all the variable names that are created in the data plan

        :return: List of strings
        """

        var_names = set()
        for year in self.plan.keys():
            var_names.update([var_def.name for var_def in self.plan[year]])

        # Add in density columns
        var_names.update([column for column in self.data.columns if "_density" in column])
        return list(var_names)

    def add_geoid(self):
        """
        add a single column named 'geoid' to self.data combining all portions of a data sets geographical identifiers

        :return: None
        """
        # handle known cases, then try a naive method

        if self.geometry == "county":
            self.data['geoid'] = self.data['state'] + self.data['county']

        elif self.geometry == "tract":
            self.data['geoid'] = self.data['state'] + self.data['county'] + self.data['tract']

        elif self.geometry == "block group":
            self.data['geoid'] = self.data['state'] + self.data['county'] + \
                                 self.data['tract'] + self.data['block group']

        else:
            geo_vars = list(set(self.data.columns).difference(self.get_var_names() + ['year']))

            # assume that all geo_vars are string columns (should be the case with census data)
            self.data['geoid'] = ""
            for geo_var in geo_vars:
                self.data['geoid'] = self.data['geoid'] + self.data[geo_var]

    def adjust_geo_fields(self):
        """
        Adds geo columns to standardize it's set

        :return: None
        """
        if self.geometry == "zcta":
            self.data['zcta'] = self.data['zip code tabulation area']

    def create_missingness(self, min_year=None, max_year=None):
        """
        Create a row for all combinations of geospatial ID and year
        :return:
        """
        if not min_year:
            min_year = min(self.years)

        if not max_year:
            max_year = max(self.years)

        if self.__has_missing:
            self.__logger.warning("Can't create missingness, Missing values already created.")
            return

        if "geoid" not in self.data.columns:
            self.add_geoid()

        self.adjust_geo_fields()

        all_vals = pd.DataFrame([[x, y] for x in range(min_year, max_year + 1)
                                 for y in self.data.geoid.unique()], columns=['year', 'geoid'])
        self.data = pd.merge(all_vals, self.data, how="left", on=['year', 'geoid'])
        self.__has_missing = True

    def write_data(self, path, file_type="csv"):
        """
        Write data  out to a file. Default method is to write out to csv. new methods can be implemented in the future.

        :param path: Path to write the data to
        :param file_type: Method to output data, currently only implemented for csv files
        :return: None, writes data to disk.
        """

        if file_type == "csv":
            self.data.to_csv(path, index=False)
            return True
        else:
            self.__logger.error("Can't output file, No Method currently implemented for file type: " + file_type)
            return False

    # noinspection PyDefaultArgument
    def calculate_densities(self, variables=["population"], sq_mi=True):
        """
        Divide specified variables by area
        :param variables: List of variables to calculate densities for
        :param sq_mi: Should denisties be calculated per square mile? If false, calculated per square meter
        :return: None
        """
        if self.geometry == "block group":
            self.__logger.error("No support currently added for block group densities, skipping densities")
            return

        if "geoid" not in self.data.columns:
            self.add_geoid()

        self.adjust_geo_fields()

        areas = get_area(self.geometry, sq_mi)
        self.data = pd.merge(self.data, areas, how="left", on="geoid")

        for variable in variables:
            new_varname = variable + "_density"
            self.data[new_varname] = self.data[variable] / self.data['arealand']

        self.data.drop(columns='arealand', inplace=True)
        self.data['geoid'] = pd.to_numeric(self.data['geoid'], errors='coerce')

    def interpolate(self, method="ma", min_year=None, max_year=None):
        """
        Fill in values
        :param method: Interpolation method to use
        :param min_year: Minimum year to interpolate
        :param max_year: Maximum year to interpolate
        :return:
        """
        if method not in interpolation.IMPLEMENTED_METHODS:
            self.__logger.exception("Can't interpolate, Invalid Interpretation Method")
            raise CensusException("Invalid Interpretation Method")

        if not min_year:
            min_year = min(self.years)

        if not max_year:
            max_year = max(self.years)

        if not self.__has_missing:
            self.create_missingness(min_year, max_year)

        interpolation.interpolate(self.data, self.get_var_names(), method, "year", "geoid")

    def quality_check(self, test_file: str):
        """
        Test self.data for the checks defined in the test file
        :param test_file: path to a yaml file defining tests per the quality check paradigm in dorieh.utils.qc
        :return: None
        """
        name = "census_" + self.geometry + "_" + str(min(self.years)) + "_" + str(max(self.years))
        census_tester = qc.Tester(name, yaml_file=test_file)
        census_tester.check(self.data)

    def _schema_dict_old(self, table_name: str = None):
        """
        return a dictionary containing the names and data types of variables that would be loaded in to a database.
        Structured as a dictionary to enable writing to either yaml of json
        :return: dict
        """
        if "geoid" not in self.data.columns:
            self.add_geoid()

        self.adjust_geo_fields()

        if not table_name:
            table_name = self.geometry

        out_cols = ["geoid", "year"] + self.get_var_names()
        col_dicts = dict()
        for col in out_cols:
            col_dicts[col] = {"type": _get_sql_type(self.data[col])}

        out = dict()
        out[table_name] = dict()
        out[table_name]["columns"] = col_dicts
        out[table_name]["primary_key"] = ["geoid", "year"]

        return out

    def _schema_dict(self, table_name: str = None):
        if "geoid" not in self.data.columns:
            self.add_geoid()

        self.adjust_geo_fields()

        if not table_name:
            table_name = self.geometry

        name = "census"
        out_cols = ["geoid", "year"] + self.get_var_names()
        domain = {
            name: {
                "schema": name,
                "index": "all",
                "description": "NSAPH data model for Census",
                "header": True,
                "quoting": 3,
                "tables": {
                    table_name: {
                        "columns": [
                            {
                                col: {
                                    "type": _get_sql_type(self.data[col])
                                }
                            }
                            for col in out_cols
                        ],
                        "primary_key": ["geoid", "year"],
                    }
                }
            }
        }

        return domain

    def write_schema(self, filename: str = None, table_name: str = None):
        """
        Write out a yaml file describing the data schema
        :param filename: path to write to
        :param table_name: Name of the table for the schema
        :return: True
        """
        if not filename:
            if table_name:
                filename = table_name + "_schema.yml"
            else:
                filename = "census_" + self.geometry + "_schema.yml"

        with open(filename, 'w') as ff:
            yaml.dump(self._schema_dict(table_name), ff)


class VariableDef:
    """
    Structured way of representing what we need to know for a variable.
    Members:
    * ``dataset``: a string. The data set used to calculate a variable, should be dec, acs1, acs5, or pums
    * ``num``: a list, the names of variables that make up the numerator
    * ``den``: a list, the names of the variables that make up the denominator. Can be missing
    * ``has_den``: a boolean, indicates whether or not there is a denominator.


    """

    def __init__(self, name: str, var_dict: dict, log: logging.Logger = None):

        self.name = name

        if not log:
            self.__logger = logging.getLogger(__name__ + ".VariableDef." + self.name)
        else:
            self.__logger = log

        self.dataset = list(var_dict.keys())[0]
        self.num = var_dict[self.dataset]['num']
        if type(self.num) is str:
            self.num = [self.num]

        if 'den' in var_dict[self.dataset].keys():
            self.has_den = True
            self.den = var_dict[self.dataset]['den']
            if type(self.den) is str:
                self.den = [self.den]
        else:
            self.has_den = False
            self.den = []

        if "acs" in self.dataset:
            self._make_acs_vars()

    def _make_acs_vars(self):
        _clean_acs_vars(self.num)
        if self.has_den:
            _clean_acs_vars(self.den)

    def get_vars(self):
        """
        :return: a union of all census variables needed for this variable


        """
        return list(set().union(self.num, self.den))

    def do_query(self, year, geometry, state=None, county=None):
        """
        Run the query defined by the contained variables
        :param geometry: census geometry to query
        :param year: year of data to query
        :param state: 2 Digit Fips code of state to limit the query to
        :param county: 3 Digit county code to limit the query to, must be used with state
        :return: data frame of all census variables specified by the query


        """
        if geometry == "tract":
            return self._do_query_tract(year, geometry, state, county)
        elif geometry == "block group":
            return self._do_query_block_group(year, geometry, state, county)

        return get_census_data(year, self.get_vars(), geometry, self.dataset, state=state, county=county)

    def _do_query_tract(self, year, geometry, state=None, county=None):
        # If state is specified, pull for just that state
        if state is not None:
            return get_census_data(year, self.get_vars(), geometry, self.dataset, state=state, county=county)

        # Otherwise loop over all states
        out = None
        state_codes = load_state_codes()
        num_queries = 0
        for i, row in state_codes.iterrows():
            num_queries += 1
            self.__logger.debug("Running query " + str(num_queries)  + " of " + str(len(state_codes.index)))
            state_data = get_census_data(year, self.get_vars(), geometry, self.dataset, state=row['state'])
            if out is None:
                out = state_data
            else:
                out = out.append(state_data, ignore_index=True)
        return out

    def _do_query_block_group(self, year, geometry, state=None, county=None):
        # if state and county are specified
        out = None
        county_codes = load_county_codes()

        if state is not None:
            if county is not None:
                return get_census_data(year, self.get_vars(), geometry, self.dataset, state=state, county=county)
            else:
                # iterate over all counties in the state
                county_codes = county_codes[county_codes.state == state]

        # iterate over all counties and states
        num_queries = 0
        for i, row in county_codes.iterrows():
            num_queries += 1
            self.__logger.debug("Running query " + str(num_queries)  + " of " + str(len(county_codes.index)))
            county_data = get_census_data(year, self.get_vars(), geometry,
                                          self.dataset, state=row['state'], county=row['county'])
            if out is None:
                out = county_data
            else:
                out = out.append(county_data, ignore_index=True)
        return out

    def calculate_var(self, year, geometry, state=None, county=None):
        """
        Query the required data from the census, then calculate the variable defined
        :param year: year of data to query
        :param geometry: census geometry to query
        :param state: 2 Digit Fips code of state to limit the query to
        :param county: 3 Digit county code to limit the query to, must be used with state
        :return: a data frame with one column of the calcualted variable and the census geography columns


        """

        data = self.do_query(year, geometry, state, county)

        # calculate numerator
        data['num'] = 0
        for num_var in self.num:
            data['num'] += data[num_var]

        if self.has_den:
            data['den'] = 0
            for den_var in self.den:
                data['den'] += data[den_var]

        if self.has_den:
            data[self.name] = data['num'] / data['den']
        else:
            data[self.name] = data['num']

        data.drop(columns=self.get_vars(), inplace=True)
        data.drop(columns="num", inplace=True)
        if self.has_den:
            data.drop(columns="den", inplace=True)

        return data

    def __str__(self):
        out = ""
        out += "Name: " + self.name + "\n"
        out += "Dataset: " + self.dataset + "\n"
        out += "Num: " + str(self.num) + "\n"

        if self.has_den:
            out += "Den: " + str(self.den)

        return out

    def __repr__(self):
        out = "<"
        out += self.name + " "
        out += self.dataset + ">"

        return out


def _find_year(year, year_list):
    """
    Internal helper function, not exported. Returns the first
    year in the list greater or equal to the year
    :param year: year of interest
    :param year_list:list: list of years, likely from a yaml census list
    :return: first year greater than or equal to "year" in "year_list"


    """

    year_list.sort()  # Should be sorted, but just in case
    for i in year_list:
        if i >= year:
            return i


def _get_sql_type(col):
    """
    given a numpy array, return the POSTGRES data type needed for that column as a string
    :param col: a numpy array
    :return: string of sql type
    """
    if type(col[0]) is np.float64:
        return "FLOAT4"
    elif type(col[0]) is np.int64:
        return "INT"
    elif type(col[0]) is str:
        max_len = max(map(len, col))
        return "VARCHAR(" + str(max_len) + ")"
    else:
        raise CensusException("unexpected column type in data")

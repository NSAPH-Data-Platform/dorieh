"""
fst2csv.py
====================================================
Command Line Interface for the census python package
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
import pickle
from dorieh.utils.context import Context, Argument, Cardinality

from dorieh.census.assemble_data import DataPlan
from dorieh.census.census_info import census_years
from dorieh.census.query import SUPPORTED_GEOMETRIES


class CensusContext(Context):
    """
    Context object supporting the CLI functionality of this package
    """
    _var_file = Argument("var_file",
                         help="Path to yaml file specifying census variables",
                         aliases=["vars"],
                         cardinality=Cardinality.single,
                         )
    _geometry = Argument("geometry",
                         help="Geographic Resolution to download census data at",
                         aliases=["geom"],
                         cardinality=Cardinality.single,
                         valid_values=SUPPORTED_GEOMETRIES
                         )
    _state = Argument("state",
                      help='2 digit FIPS code of the state you want to limit the query to (i.e. "06" for CA)',
                      cardinality=Cardinality.single,
                      default=None,
                      required=False
                      )
    _densities = Argument("densities",
                          aliases=['d'],
                          help="""Names of variables to calculate denisity per square mile for. If ommitted, 
                              density calculation will be skipped. To calculate population density, assuming
                              population is stored in a variable named 'population', the option would be specified
                              -d population""",
                          cardinality=Cardinality.multiple,
                          default=None,
                          required=False)
    _county = Argument("county",
                       help="3 digit FIPS code of the county you want to include. Requires state to be specified",
                       cardinality=Cardinality.single,
                       default=None,
                       required=False
                       )
    _interpolate = Argument("interpolate",
                            help="""Years to interpolate for. Takes min year + max year formatted 
                            as <min_year>:<max_year>. Enter 'x' to skip interpolation""",
                            aliases=["i"],
                            cardinality=Cardinality.single,
                            default="1999:2019",
                            )
    _out_file = Argument("out_file",
                         aliases=["out"],
                         help="name of file to write output to",
                         cardinality=Cardinality.single,
                         default=None)
    _out_format = Argument("out_format",
                           help="file format to store output as.",
                           default="csv",
                           cardinality=Cardinality.single,
                           valid_values=DataPlan.supported_out_formats)
    _years = Argument("years",
                      aliases=["y"],
                      help="""
                      Year or list of years to download. For example, 
                      the following argument: 
                      `-y 1992:1995 1998 1999 2011 2015:2017` will produce 
                      the following list: 
                      [1992,1993,1994,1995,1998,1999,2011,2015,2016,2017]
                      
                      Note that in the census module CLI, only the minimum and maximum year passed are used
                      and are passed to census.census_years() to ensure that only years that are available are used.
                      Additional variable level year control is determined by the variable specification yaml file. 
                      """,
                      cardinality=Cardinality.multiple,
                      default="2000:2019"
                      )
    _quality_check = Argument("quality_check",
                              aliases=["qc"],
                              help="""
                              Path to a yaml file specifying the checks to be run on the data. Yaml file should be 
                              structured per the paradigm used by dorieh.utils.qc
                              """,
                              cardinality=Cardinality.single,
                              default=None,
                              required=False)
    _log = Argument("log",
                    help="""
                    Path to output log file. If you want logging info to print on the screen, enter "screen".
                    """,
                    cardinality=Cardinality.single,
                    default="census.log")
    _debug = Argument("debug",
                      help = """
                      Boolean. If included, debug level messages will be logged. Otherwise defaults to "info" level.
                      """,
                      type=bool)
    _pkl_file = Argument("pkl_file",
                         help="Path to temporary pkl file",
                         cardinality=Cardinality.single,
                         default="census.pkl")

    def __init__(self, doc=None):
        self.var_file = None
        self.geometry = None
        self.state = None
        self.county = None
        self.densities = None
        self.interpolate = None
        self.out_file = None
        self.out_format = None
        self.quality_check = None
        self.log = None
        self.debug = None
        self.pkl_file = None
        super().__init__(CensusContext, doc)

    def validate(self, attr, value):
        value = super().validate(attr, value)

        if attr == "interpolate":
            if value == "x":
                return None
            else:
                value = value.split(":")
                out = dict()
                out["min"] = int(value[0])
                out["max"] = int(value[1])
                return out

        return value


def census_cli():

    context = CensusContext(__doc__).instantiate()

    if context.debug:
        level = logging.DEBUG
    else:
        level = logging.INFO

    if context.log == "screen":
        logging.basicConfig(level=level)
    else:
        logging.basicConfig(filename=context.log, level = level)

    census = DataPlan(context.var_file,
                      context.geometry,
                      years=census_years(min(context.years), max(context.years)),
                      state=context.state,
                      county=context.county)
    census.assemble_data()

    if context.interpolate:
        census.interpolate(min_year=context.interpolate["min"], max_year=context.interpolate["max"])

    if context.densities:
        census.calculate_densities(context.densities)

    census.write_data(context.out_file, file_type=context.out_format)

    if context.quality_check:
        census.quality_check(context.quality_check)

    with open(context.pkl_file, 'wb') as f:
        pickle.dump(census, f)


if __name__ == "__main__":
    census_cli()

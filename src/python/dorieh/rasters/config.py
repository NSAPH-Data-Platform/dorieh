"""
This module contains classes and enums used to configure
gridMET processing and specify its parameters
"""


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
from enum import Enum
from typing import Optional

from dorieh.gis.constants import Geography, RasterizationStrategy
from dorieh.utils.context import Context, Argument, Cardinality

var_doc_string = """
        Gridmet bands or variables. 
        :ref: `doc/bands`
"""


class DateFilter:
    """
    Class, implementing filtering by dates. Primarily used for
    debugging and testing purposes to avoid long running calculations.

    The condition can be specified in one of the following ways:

    - Range: `YYYY-MM-DD:YYYY-MM-DD` only dates falling in the given
        range will be accepted. Example: '2009-12-30:2010-01-03' means
        that only 5 days between the 30-th of December of 2009 and
        January 3, 2010 will be accepted
    - Day of Month: `dayofmonth:DD`, example: 'dayofmonth:12' means that
        only dates corresponding to the 12-th of every month will be accepted
    - Month: `month:MM` only dates in the given month will be accepted
    - Month and day of a year: `date:MM-DD`, example: 'date:03-14' means
        that only March 14 for each year will be accepted.
    """

    def __init__(self, value: str):
        self.min = None
        self.max = None
        self.ftype = None
        self.values = []
        if not value:
            return
        if ':' not in value:
            # raise ValueError("Filter spec must include ':'")
            bounds = [value, value]
        else:
            bounds = value.split(':')
        if bounds[0].lower() in ["dayofmonth", "month", "date"]:
            self.ftype = bounds[0].lower()
            self.values = [v.strip() for v in bounds[1].split(',')]
        else:
            self.ftype = "range"
            self.min = datetime.date.fromisoformat(bounds[0])
            self.max = datetime.date.fromisoformat(bounds[1])

    def accept(self, day: datetime.date):
        if self.ftype == "dayofmonth":
            dom = str(day.day)
            if dom in self.values:
                return True
            return False
        elif self.ftype == "month":
            mnth = str(day.month)
            if mnth in self.values:
                return True
            return False
        elif self.ftype == "date":
            dt = day.strftime("%m-%d")
            if dt in self.values:
                return True
            if dt.strip('0') in self.values:
                return True
            return False
        if self.min and day < self.min:
            return False
        if self.max and day > self.max:
            return False
        return True


class Shape(Enum):
    """Type of shape"""

    point = "point"
    """Point"""
    polygon = "polygon"
    """Polygon"""


class GridmetVariable(Enum):
    """
    `GridMET Bands <https://developers.google.com/earth-engine/datasets/catalog/IDAHO_EPSCOR_GRIDMET#bands>`_
    and additional exposure variable types
    """
    bi = "bi"
    """Burning index: NFDRS fire danger index"""
    erc = "erc"
    """Energy release component: NFDRS fire danger index"""
    etr = "etr"
    """Daily reference evapotranspiration: Alfalfa, mm"""
    fm100 = "fm100"
    """100-hour dead fuel moisture: %"""
    fm1000 = "fm1000"
    """1000-hour dead fuel moisture: %"""
    pet = "pet"
    """Potential evapotranspiration"""
    pr = "pr"
    """Precipitation amount: mm, daily total """
    rmax = "rmax"
    """Maximum relative humidity: %"""
    rmin = "rmin"
    """Minimum relative humidity: %"""
    sph = "sph"
    """Specific humididy: kg/kg"""
    srad = "srad"
    """Surface downward shortwave radiation: W/m^2"""
    th = "th"
    """Wind direction: Degrees clockwise from North"""
    tmmn = "tmmn"
    """Minimum temperature: K"""
    tmmx = "tmmx"
    """Maximum temperature: K"""
    vpd = "vpd"
    """Mean vapor pressure deficit: kPa"""
    vs = "vs"
    """Wind velocity at 10m: m/s"""


class OutputType(Enum):
    """
    Type of teh output that the tool should produce
    """

    aggregation     = "aggregation"
    data_dictionary = "data_dictionary"


class GridContext(Context):
    """
    Defines a configuration object to process aggregations and other tasks
    over data grids
    """

    _variables = Argument("variables",
                          help="Gridmet bands or variables",
                          aliases=["var"],
                          cardinality=Cardinality.multiple)
    _strategy = Argument("strategy",
                         aliases=['s'],
                         default=RasterizationStrategy.default.value,
                         help="Rasterization Strategy",
                         valid_values=[v.value for v in RasterizationStrategy])
    _destination = Argument("destination",
                            aliases=['dest', 'd'],
                            cardinality=Cardinality.single,
                            default="data/processed",
                            help="Destination directory for the processed files"
                            )
    _raw_downloads = Argument("raw_downloads",
                              cardinality=Cardinality.single,
                              default="data/downloads",
                              help="Directory for downloaded raw files"
                            )
    _geography = Argument("geography",
                          cardinality = Cardinality.single,
                          default = "zip",
                          help = "The type of geographic area over "
                                 + "which we aggregate data",
                          valid_values=[v.value for v in Geography]
                          )
    _shapes_dir = Argument("shapes_dir",
                           default="shapes",
                           help="Directory containing shape files for"
                            + " geographies. Directory structure is"
                            + " expected to be: "
                            + ".../${year}/${geo_type}/{point|polygon}/")
    _shapes = Argument("shapes",
                       cardinality=Cardinality.multiple,
                       default=[Shape.polygon.value],
                       help="Type of shapes to aggregate over",
                       valid_values=[v.value for v in Shape]
                       )
    _points = Argument("points",
                       cardinality=Cardinality.single,
                       default="",
                       help="Path to CSV file containing points")
    _coordinates = Argument("coordinates",
                            aliases=["xy", "coord"],
                            cardinality=Cardinality.multiple,
                            default="",
                            help="Column names for coordinates")
    _metadata = Argument("metadata",
                            aliases=["m", "meta"],
                            cardinality=Cardinality.multiple,
                            default="",
                            help="Column names for metadata")
    _extra_columns = Argument("extra_columns",
                              aliases=["e", "extra"],
                              cardinality=Cardinality.multiple,
                              default="",
                              help="Columns with constant values to be added to the output file"
    )
    _statistics = Argument("statistics",
                           cardinality=Cardinality.single,
                           default="mean",
                           help="Type of statistics"
                           )
    _dates = Argument("dates",
                      help="Filter dates, can be used "
                           + "to paralellize computations "
                           + "(e.g., over months) and "
                           + "for debugging purposes",
                      required=False)
    _shape_files = Argument("shape_files",
                       cardinality=Cardinality.multiple,
                       default="",
                       help="Path to shape files",
                       )
    _description = Argument("description",
                   cardinality=Cardinality.single,
                   default="Dorieh data model for aggregations of netCDF data",
                   help="Description to be added to data dictionary"
                   )
    _table = Argument("table",
          help = "Name of the table where the aggregated data will be stored",
          type = str,
          required = False,
          aliases = ["t"],
          default = None,
          cardinality = Cardinality.single
          )
    _output = Argument("output",
                       aliases=['o'],
                       cardinality=Cardinality.multiple,
                       default=[OutputType.aggregation.value],
                       help="What the tool should output",
                       valid_values=[v.value for v in OutputType])
    _ram = Argument("ram",
                    cardinality=Cardinality.single,
                    help="Runtime memory available to the process",
                    default="2G"
    )

    def __init__(self, subclass = None, doc = None):
        """
        Constructor
        
        :param doc: Optional argument, specifying what to print as documentation
        """

        self.variables = None
        """
        Gridmet bands or variables 
        
        :type: List[GridmetVariable] 
        """

        self.strategy = None
        """
        Rasterization strategy
        :type: RasterizationStrategy
        """

        self.destination = None
        '''Destination directory for the processed files'''
        self.raw_downloads = None
        '''Directory for downloaded raw files'''
        self.geography = None
        """
        The type of geographic area over which we aggregate data
        
        :type: Geography
        """

        self.shapes_dir = None
        '''Directory containing shape files for geographies'''
        self.shapes = None
        """
        Type of shapes to aggregate over, e.g. points, polygons
        
        :type: List[Shape]
        """
        self.shape_files = None

        self.points = None
        '''Path to CSV file containing points'''
        self.coordinates = None
        '''Column names for coordinates'''
        self.metadata = None
        '''Column names for metadata'''
        self.extra_columns = None
        '''Columns with constant values to be added to the output file'''
        self.dates: Optional[DateFilter] = None
        '''Filter on dates - for debugging purposes only'''
        self.statistics = None
        '''Type of statistics'''
        self.description = None
        '''Description to be added to data dictionary'''
        self.table = None
        '''Name of the table where the aggregated data will be stored'''
        self.output = None
        '''Type of the output the tool should produce'''
        self.ram = None
        '''Runtime memory available to the process'''

        if subclass is None:
            super().__init__(GridContext, doc, include_default = True)
        else:
            super().__init__(subclass, doc, include_default = True)
            self._attrs += [
                attr[1:] for attr in GridContext.__dict__
                if attr[0] == '_' and attr[1] != '_'
            ]

    def validate(self, attr, value):
        value = super().validate(attr, value)
        if attr == self._shapes.name:
            return [Shape(v) for v in value]
        if attr == self._geography.name:
            return Geography[value]
        if attr == self._strategy.name:
            return RasterizationStrategy[value]
        if attr == self._output.name:
            return [OutputType[v] for v in value]
        if attr == self._dates.name:
            if value:
                return DateFilter(value)
        if attr == self._ram.name:
            value = value.strip().lower()
            nv = ""
            postfix = ""
            for c in value:
                if c.isdigit():
                    nv += c
                else:
                    postfix += c
            n = int(nv)
            m = {
                "": 1,
                "k": 1000,
                "m": 1000000,
                "g": 1000000000,
                "t": 1000000000000
            }.get(postfix[0])
            if m is None:
                raise ValueError("Invalid value for RAM: " + value)
            value = n * m
        return value


class GridMETContext(GridContext):
    """
    Defines a configuration object to process aggregations and other tasks
    over data grids containing gridMET data. Includes validation that
    a correct gridMET band is provided
    """

    # _variables = Argument("variables",
    #                       help="Gridmet bands or variables",
    #                       aliases=["var"],
    #                       cardinality=Cardinality.multiple,
    #                       valid_values=[v.value for v in GridmetVariable])
    GridContext._variables.valid_values=[v.value for v in GridmetVariable]

    def __init__(self, doc = None):
        super().__init__(GridMETContext, doc)

    def validate(self, attr, value):
        value = super().validate(attr, value)
        if attr == self._variables.name:
            return [GridmetVariable(v) for v in value]
        return value

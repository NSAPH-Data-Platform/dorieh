"""
Module contains classes to describe the context in which AirNow data is downloaded
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

from enum import IntEnum, Enum
from dorieh.utils.context import Context, Argument, Cardinality


class Parameter(Enum):
    """
    An Enum with mnemonic names for the most common EPA AirNow Parameter Codes
    See more at https://docs.airnowapi.org/Data/docs
    """

    NO2 = "no2"
    '''NO2'''
    OZONE = "ozone"
    '''ozone'''
    PM25 = "pm25"
    '''PM25'''
    PM10 = "pm10"
    '''PM10'''
    CO = "co"
    '''co'''
    SO2 = "so2"
    '''SO2'''

    def __str__(self):
        return str(self.name)

    @classmethod
    def values(cls):
        return {p.value for p in Parameter}


class AirNowContext(Context):
    """
    This class is part of EPA AirNow Toolkit. It allows user to define any
    parameters that are used to select what data to download,
    how to format it and where to place the results.

    It is a concrete subclass of :class Context:
    """

    _parameters = Argument("parameters",
                          aliases=['p'],
                          cardinality=Cardinality.multiple,
                          valid_values=[a.value.lower() for a in Parameter]
                           + [a.value.upper() for a in Parameter],
                          help="EPA AirNow Parameter Codes",
                          required=True
    )
    _destination = Argument("destination",
        aliases=['dest', 'd'],
        cardinality=Cardinality.single,
        help="Destination directory for the downloaded files",
        required=False
    )
    _start_date = Argument("start_date",
        aliases=["start-date", "from"],
        help="First date in the range to download (inclusive)",
        required=True
    )
    _end_date = Argument("end_date",
        aliases=["end-date", "to"],
        help="Last date in the range to download (inclusive)",
        required=True
    )
    _reset = Argument("reset",
                      help="Discard previously downloaded data if exists",
                      type=bool,
                      default=True
    )

    _qc = Argument("qc",
                      help="Perform basic data QC",
                      type=bool,
                      default=True
    )
    _cfg = Argument("cfg",
                    help = "An optional path to config file",
                    required=False
    )
    _shapes = Argument("shapes",
                    help = "An optional path to shape files",
                    cardinality= Cardinality.multiple,
                    required=False
    )
    _api_key = Argument("api_key",
                        aliases=["api-key"],
                        help = "AirNow API Key",
                        required=False
    )
    _proxy = Argument("proxy",
                        help = "Proxy for external connections, i.e. https://1.1.1.1:3128 ",
                        required=False
    )

    def __init__(self, doc = None):
        """
        Constructor

        :param doc: Optional argument, specifying what to print as documentation
        """

        self.parameters = None
        '''Parameters (variables, e.g. PM25, NO2, etc.) to download'''
        self.destination = None
        '''Destination directory for the downloaded files'''
        self.start_date = None
        '''First date in the range to download (inclusive)'''
        self.end_date = None
        '''Last date in the range to download (inclusive)'''
        self.reset = None
        '''Discard previously downloaded data if exists'''
        self.qc = None
        '''Perform basic data QC'''
        self.cfg = None
        ''' Optional path to config file '''
        self.shapes = None
        ''' Optional path to shapes directory '''
        self.api_key = None
        ''' AirNow API Key '''
        self.proxy = None
        ''' Proxy address '''
        super().__init__(AirNowContext, doc)
        self.instantiate()

    def validate(self, attr, value):
        if attr == "parameters" and value is not None:
            value = [v.lower() for v in value]
        return super().validate(attr, value)

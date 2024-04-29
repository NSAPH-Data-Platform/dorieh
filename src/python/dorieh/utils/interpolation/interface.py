#  Copyright (c) 2021. Harvard University
#
#  Developed by Research Software Engineering,
#  Faculty of Arts and Sciences, Research Computing (FAS RC)
#  Author: Ben Sabath
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
# Code for wrapping the various interpolation functions
import logging

import pandas as pd
from tqdm import tqdm

from .interpolate_ma import interpolate_ma

IMPLEMENTED_METHODS = ['ma']
LOG = logging.getLogger(__name__)


def interpolate(data: pd.DataFrame, interpolate_vars: list, method: str, tvar: str, by_var: str, ma_num: int = 4):
    """
    General function for calling interpolation. Will be updated as additional interpolation
    methods are developed

    :param data: A pandas data frame, containing geospatial data with missingness included
    :param interpolate_vars: list of variable names to interpolate
    :param method: A string containing the interpolation method to use. Valid vales:
        - "ma": moving average method, see ``interpolate_ma``
    :param tvar: variable containing the time dimension
    :param by_var: single variable uniquely identifying each spatial division. If this information is contained
        in more than one variable in the intitial data, a separate ID column should be created.
    :param ma_num: Only used when method = "ma". The default size f the moving average window to use. Defaults to 3.
    :return: None, replaces missing values in the data frame in place
    """

    assert method in IMPLEMENTED_METHODS

    if method == "ma":
        data.sort_values(by=[tvar, by_var], inplace=True)
        id_vals = data[by_var].unique()

        for data_var in interpolate_vars:
            LOG.info("Interpolating " + data_var)
            for id_val in tqdm(id_vals):
                data.loc[data[by_var] == id_val, data_var] = interpolate_ma(data[data[by_var] == id_val][data_var],
                                                                            ma_num)

    return True

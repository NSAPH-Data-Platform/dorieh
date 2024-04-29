"""
Reads a NetCDF file (*.nc) and prints some information
about it
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
import sys

import netCDF4 as nc
import random

from dorieh.rasters.gridmet_tools import get_address

if __name__ == '__main__':
    fn = sys.argv[1]
    ds = nc.Dataset(fn)
    print(ds)

    pm25 = ds["PM25"]
    lat = ds["LAT"]
    lon = ds["LON"]
    random.seed(0)
    for i in range(0, 20):
        lo = random.randrange(0, len(lon))
        la = random.randrange(0, len(lat))
        address = get_address(float(lat[la]), float(lon[lo]))
        data = "[{:d},{:d}]: ({:f}, {:f}: {})".format(lo, la, lat[la], lon[lo], str(pm25[la, lo]))
        if address is not None:
            data += "; Address: " + str(address)
        print(data)


    pass
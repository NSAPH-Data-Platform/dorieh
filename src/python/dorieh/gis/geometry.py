"""
Utilities to work with points in a raster
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

import itertools
from typing import Optional

from numpy.ma import masked
from rasterstats import point


class PointInRaster:
    """
    Class denoting a point in a raster. This a wrapper
    around class rasterstats.point optimizing some operations,
    primarily the bilinear interpolation

    See also https://pythonhosted.org/rasterstats/_modules/rasterstats/point.html
    """

    COMPLETELY_MASKED = 1
    PARTIALLY_MASKED = 2

    def __init__(self, raster, affine, x, y):
        self.x = None
        '''X coordinate of the point'''

        self.y = None
        '''Y coordinate of the point'''

        self.window = None
        '''Window representing 2x2 window whose center points encompass point'''

        self.window, unitxy = point.point_window_unitxy(x, y, affine)
        self.x, self.y = unitxy
        self.masked = 0

        m = 0
        array = raster.read(window=self.window, masked=True).array
        for i, j in itertools.product([0,1], [0,1]):
            r = self.window[0][0] + i
            c = self.window[1][0] + j
            if array[i, j] is masked:
                m += 1
            elif raster.array[r, c] is masked:
                m += 1
            else:
                self.r, self.c = r, c

        if m == 4:
            self.masked = self.COMPLETELY_MASKED
        elif m > 0:
            self.masked = self.PARTIALLY_MASKED

    def is_masked(self) -> bool:
        return self.masked == self.COMPLETELY_MASKED

    def array(self, raster):
        """
        Returns an array consisting of the corners of the rectangular, containing this point.

        :param raster:
        :return:

        """

        return raster.array[
            self.window[0][0]:self.window[0][1],
            self.window[1][0]:self.window[1][1],
        ]

    def bilinear(self, raster) -> Optional[float]:
        """
        An optimized version of rasterstats.point function:
        given a point's window as 2x2 array, and x, y as its coordinates,
        treat center points as a unit square.

            +---+---+
            | A | B |      +----+
            +---+---+  =>  |    |
            | C | D |      +----+
            +---+---+

            e.g.: Center of A is at (0, 1) on unit square, D is at (1, 0), etc

        :param raster: Raster, to which the point belongs
        :return: the value for the fractional row/col
                using bilinear interpolation between the cells
        """

        if self.masked == self.COMPLETELY_MASKED:
            return None

        if self.masked == self.PARTIALLY_MASKED:
            return raster.array[self.r, self.c]

        array = self.array(raster)

        x, y = self.x, self.y
        ulv, urv, llv, lrv = array[0,0], array[0,1], array[1,0], array[1,1]
        return (
            (llv * (1 - x) * (1 - y)) +
            (lrv * x * (1 - y)) +
            (ulv * (1 - x) * y) +
            (urv * x * y)
        )

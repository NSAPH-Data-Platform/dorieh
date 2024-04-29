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
import glob
import math
import os
from typing import List, Optional
import rasterio

from netCDF4._netCDF4 import Dataset
import numpy
import geopy


def get_atmos_url(year:int, variable ="PM25") -> str:
    """
    Constructs URL to download data from the
    Atmospheric Composition Analysis Group
    given a year and a band

    :param year: year
    :param variable: Gridmet band (variable)
    :return: URL for download
    """

    base = "http://fizz.phys.dal.ca/~atmos/datasets/V4NA03/"
    pattern = base + "V4NA03_{}_NA_{:d}01_{:d}12-RH35.nc"
    return pattern.format(variable, year, year)


def get_nkn_url(variable:str, year:int) -> str:
    """
    Constructs URL to download data from University of Idaho (UI)
    Northwest Knowledge Network
    given a year and a band

    :param year: year
    :param variable: Gridmet band (variable)
    :return: URL for download
    """

    base = "https://www.northwestknowledge.net/metdata/data/"
    pattern = base + "{}_{:d}.nc"
    return pattern.format(variable, year)


def check_shape_file(shapes_dir: str,
                     year: int,
                     geography_type: str,
                     shape_type: str) -> [Optional[str], list]:
    d = os.path.join(shapes_dir, "{:d}".format(year))
    if os.path.isdir(d):
        f = "{}/{}/ESRI{:02d}USZIP5_POLY_WGS84.shp".format(
            geography_type, shape_type,  year - 2000)
        return os.path.join(d, f)
    tiger_format = "tl_{:04d}_us_{}*.shp"
    tiger_pattern = tiger_format.format(year, geography_type)
    tiger_shapes = glob.glob(os.path.join(shapes_dir, tiger_pattern))
    if tiger_shapes:
        return tiger_shapes

    return None


def find_shape_file(shapes_dir: str, year: int,
                    geography_type: str, shape_type: str) -> str:
    """
    Finds shapefile for a given type of geographies for the
    closest available year

    :param shapes_dir: Directory containing shape files organized as
        ${year}/${geo_type}/{point|polygon}
    :param year: year
    :param geography_type: Geography type, e.g. zip, county, etc.
    :param shape_type: Shape type: polygon, point, etc.
    :return: a shape file for a given year if it exists or for the latest
        year before the given
    """

    shape_file = None
    for d in [-1, 1]:
        y = year
        while (1980 < y < 2021) and (shape_file is None):
            shape_file = check_shape_file(shapes_dir, y, geography_type, shape_type)
            y += d
        if shape_file:
            break
    if shape_file is None:
        raise Exception(
            "Could not find ZIP shape file for year {:d} or earlier"
                .format(year))
    return shape_file

def get_variable(dataset: Dataset,  variable: str):
    """
    Extracts a variable (column) name by a variable "standard name"
    from NCDF4 dataset

    Standard name is a name of a band as described here:
    https://gee.stac.cloud/WUtw2spmec7AM9rk6xMXUtStkMtbviDtHK?t=bands

    A column name is a name of the column in the dataset

    :param dataset: an NCDF4 dataset
    :param variable: "standard name" of a variable, e.g. "tmmx"
    :return:
    """

    standard_name = variable
    for var in dataset.variables.values():
        if hasattr(var,"standard_name") \
                and var.standard_name == standard_name:
            return var.name
    raise Exception("Not found in the dataset: " + standard_name)


def get_days(dataset: Dataset) -> List:
    """
    Extracts a table fo days from NCDF4 dataset

    :param dataset: NCDF4 dataset
    :return: List, containing days
    """

    return dataset["day"][:]


def get_affine_transform(nc_file: str, factor: int = 1):
    """
    Returns affine transformation for a NCDF4 dataset.

    Uses rasterio package: https://rasterio.readthedocs.io/en/latest/index.html

    The `Affine` object is a named tuple with elements
    `a, b, c, d, e, f` corresponding to the elements in
    the matrix equation below, in which a pixel’s image
    coordinates are `x, y` and its world coordinates are `x', y'`

    See more:
    https://rasterio.readthedocs.io/en/latest/topics/georeferencing.html

    :param factor: factor used for disaggregation, None or 0 means
        no disaggregation
    :param nc_file: path to file, containing dataset
    :return: Instance of affine transformation
    """

    with rasterio.open(nc_file) as rio:
        affine = rio.transform
    if factor and factor != 1:
        affine = rasterio.Affine(affine.a / factor,
                                 affine.b,
                                 affine.c,
                                 affine.d,
                                 affine.e / factor,
                                 affine.f
                                 )
    return affine


def disaggregate(layer, factor: int):
    """
    Implementation of R `disaggregate` function with method == ''.

    See details:
    https://www.rdocumentation.org/packages/raster/versions/3.4-5/topics/disaggregate

    or, original source code:

    https://github.com/r-forge/raster/blob/master/pkg/raster/R/disaggregate.R

    :param layer:
    :param factor:
    :return:
    """

    if not factor or factor == 1:
        return layer
    arr = numpy.repeat(layer, factor, axis=0)
    return numpy.repeat(arr, factor, axis=1)


geolocator = geopy.Nominatim(user_agent='NSAPH')


def get_address(latitude:float, longitude: float):
    location = geolocator.reverse((latitude, longitude))
    return location


def estimate_optimal_downscaling_factor(size: int, ram: int):
    x = ram / 1000000000
    max_size = 50000000.0
    max_size *= x
    f = math.sqrt(max_size / size)
    if f < 1:
        f = 1
    return int(f)

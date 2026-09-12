"""
This module contains Enums used by configuration for
processing of GIS information
"""

from enum import Enum


class RasterizationStrategy(Enum):
    """
    `Rasterization Strategy  <https://pythonhosted.org/rasterstats/manual.html#rasterization-strategy>`_
    to rasterize a vector.

    While `downscale` strategy provides the best accuracy it requires
    significantly more resources, especially RAM.
    """

    default = 'default'
    """
    The default strategy is to include all pixels along the line render path
    (for lines), or cells where the center point is within the polygon
    (for polygons).

    .. :noindex:
    """

    all_touched = 'all_touched'
    """
    Alternate, all_touched strategy, rasterizes the geometry
    by including all pixels that it touches.

    .. :noindex:
    """

    combined = 'combined'
    """
    Calculate statistics using both default and all_touched strategy and
    combine results, e.g. using arithmetic means

    .. :noindex:
    """

    downscale = 'downscale'
    """
    A combination of "default" rasterization strategy with 
    affine transformation with downscaling. Downscaling factor 
    is computed based on the grid size and runtime memory available 
    to the process. 
    
    Effectively, the grid is interpolated with intermediate nodes,
    increasing the number of nodes by the factor of 25 (5 x 5). Hence,
    the accuracy is better, especially for complex and small shapes,
    however, the aggregation will require 25 times more memory (RAM)
    and will run slower.
    
    See `get_affine_transform <../../../gridmet/doc/gridmet_tools.html#gridmet.gridmet_tools.get_affine_transform>`_

    .. :noindex:
    """

    auto = 'auto'
    """
    A combination of "all_touched" rasterization strategy with 
    affine transformation with downscaling. Downscaling factor 
    is computed based on the grid size and runtime memory available 
    to the process. 
    
    Effectively, the grid is interpolated with intermediate nodes,
    increasing the number of nodes by the factor of 25 (5 x 5). Hence,
    the accuracy is better, especially for complex and small shapes,
    however, the aggregation will require 25 times more memory (RAM)
    and will run slower.
    
    See `get_affine_transform <../../../gridmet/doc/gridmet_tools.html#gridmet.gridmet_tools.get_affine_transform>`_

    .. :noindex:
    """


class Geography(Enum):
    """Type of geography"""
    zip = 'zip'
    zcta = 'zcta'
    county = 'county'
    custom = 'custom'
    all    = 'all'

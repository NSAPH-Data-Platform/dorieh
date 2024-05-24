# Dorieh GIS python package

## GIS Library Overview 

Per [USGS](https://www.usgs.gov/faqs/what-geographic-information-system-gis), 
a Geographic Information System (GIS) is a computer system that 
analyzes and displays geographically referenced information. 
It uses data that is attached to a unique location.

This `dorieh.gis` library contains several modules, aimed to work with US Census shape files. 
They fall into two categories:

* Utilities to download appropriate shapefiles for a given geography type and year
* Utilities to aggregate raster data over given shapefiles 

## Shape files Downloader

### US Census Shapefiles collections

[See also](https://www2.census.gov/geo/tiger/GENZ2022/description.pdf)

We predominantly focus on two types of geographical areas:  US counties and 
US Zip Code Tabulation Areas (ZCTAs). 
ZCTAs, created by the US Census Bureau, are generalized representations of the
United States Postal Service (USPS) zip code service areas. 
Shape files for these specific types of areas can be obtained freely from the 
US Census website, which offers two collections: TIGER/Line and TIGER/GENZ. 
These collections are part of the Topologically Integrated Geographic 
Encoding and Referencing (TIGER) system, a digital database of geographic 
features, such as roads, rivers, and legal and statistical geographic areas. 
Each shape file in these collections contains a series of polygons, each 
corresponding to a specific geographical area. TIGER/GENZ shape files, 
while providing simplified representations of selected geographic areas, are 
specifically designed for small scale thematic mapping and improved visual representations. 
However, due to their lack of detail, they are not recommended for calculations. 
Therefore, our work primarily utilizes the more detailed TIGER/Line shape files. 

### Downloader Python Modules

Python tools to download shapefiles from US Census website.
Files to be downloaded are selected based on a desired year and
shapefiles collection.

If the desired year is not present in the requested collection,
the most recent prior year is used.

If HTTP Proxy is used the environment variable
`HTTPS_PROXY` must be defined.


```{toctree}
---
glob: true
---
Python class GISDownloader, a Python API to download shapefiles from US Census website    <members/downloader>
Python module to be used as command line for downloading shapefiles <members/shapes_downloader>
```
                                   
### Shapefiles-based computations

```{toctree}
---
glob: true
---
Dorieh GIS Annotator annotates records in the stream fo data with labels attached to polygons in shapefiles   <members/gis_annotator.rst>
A Python module to take layer(s) from a raster file and aggregate teh data to given shapes <members/compute_shape>
```


### A Point in raster tools

PointInRaster Python class provides an abstraction for a point superimposed on a raster. 
It provides methods to check if a point is masked, obtain the rectangular containing 
the given point, and, most importantly, providing fast bilinear interpolation for the 
raster data to the point.

The most important application of this class is for processing a stream of points, for example,
when one needs to process a huge number of points, so it is not viable to create a single
dataframe containing them all.


```{toctree}
---
glob: true
---
A point in raster Python API   <members/geometry>
```


### GIS-related constants (enums)

```{toctree}
---
glob: true
---
Dorieh GIS enums    <members/gis_constants>
```

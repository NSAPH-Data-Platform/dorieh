# Computational Utilities for working with Climate gridMET data

For the guided end-to-end climate pipeline (Bronze/Silver/Gold layers), see the tutorial [Building a Bronze–Silver–Gold Climate Pipeline with Dorieh](tutorial/climate/building-climate-pipeline.md).

This page documents the command-line utilities and CWL pipelines for
downloading gridMET data and aggregating it over geographies such as
ZIP codes and counties.

```{contents}
---
local:
---
```

## What is gridMET?

gridMET is a dataset of daily high-spatial resolution (~4-km, 1/24th degree)
surface meteorological data covering the contiguous US from 1979-yesterday.
The data are also known and cited as METDATA.

Executing pipelines from this package requires a collection of shape
files for the geographies over which data is aggregated (for example,
ZIP code areas or counties).

The shape files must be placed in the following directory structure:
`${year}/${geo_type: zip|county|etc.}/${shape:point|polygon}/`

The geography is selected by the `geography` argument (default: "zip").
Only the geographies and years you actually use need shape files.

## Using command line gridMET utility 

```
usage: 
Executing pipelines through this class requires a collection of shape files
corresponding to geographies for which data is aggregated
(for example, zip code areas or counties).

The data has to be placed in the following directory structure:
${year}/${geo_type: zip|county|etc.}/${shape:point|polygon}/

Which geography is used is defined by `geography` argument that defaults
to "zip". Only actually used geographies must have their shape files
for the years actually used.

Output file format:
At the moment output is a simple 3+ columns file (most files contain 3
columns, but parameter “metadata” can define more columns to include):

1. Variable (aka band) mean value. The actual band is given in the arguments
   (or configuration object) and is printed in the header line of the file

2. Date in YYYY-mm-dd format (SQL date format)

3. Label, associated with location. E.g., zip code for zip shapes,
   county fips for county shapes or custom label for point file.
   For points file, the label is taken from the first column defined by
   “metadata” argument.

4+. If more than one column is included in metadata, the output file
    will contain more than 3 columns

       [-h] [--years [YEARS ...]] [--compress]
       --variables VARIABLES [VARIABLES ...]
       [--strategy {default,all_touched,combined,downscale,auto}]
       [--destination DESTINATION] [--raw_downloads RAW_DOWNLOADS]
       [--geography {zip,zcta,county,custom,all}] [--shapes_dir SHAPES_DIR]
       [--shapes [{point,polygon} ...]] [--points POINTS]
       [--coordinates COORDINATES [COORDINATES ...]]
       [--metadata METADATA [METADATA ...]]
       [--extra_columns EXTRA_COLUMNS [EXTRA_COLUMNS ...]]
       [--statistics STATISTICS] [--dates DATES]
       [--shape_files SHAPE_FILES [SHAPE_FILES ...]]
       [--description DESCRIPTION] [--table TABLE]
       [--output [{aggregation,data_dictionary} ...]] [--ram RAM]

options:
  -h, --help            show this help message and exit
  --years, -y [YEARS ...]
                        Year or list of years to download. For example, the
                        following argument: `-y 1992:1995 1998 1999 2011
                        2015:2017` will produce the following list:
                        [1992,1993,1994,1995,1998,1999,2011,2015,2016,2017] ,
                        default: 1990:2026
  --compress, -c        Use gzip compression for the result, default: True
  --variables, --var VARIABLES [VARIABLES ...]
                        Gridmet bands or variables
  --strategy, -s {default,all_touched,combined,downscale,auto}
                        Rasterization Strategy, default: default
  --destination, --dest, -d DESTINATION
                        Destination directory for the processed files,
                        default: data/processed
  --raw_downloads RAW_DOWNLOADS
                        Directory for downloaded raw files, default:
                        data/downloads
  --geography {zip,zcta,county,custom,all}
                        The type of geographic area over which we aggregate
                        data, default: zip
  --shapes_dir SHAPES_DIR
                        Directory containing shape files for geographies.
                        Directory structure is expected to be:
                        .../${year}/${geo_type}/{point|polygon}/, default:
                        shapes
  --shapes [{point,polygon} ...]
                        Type of shapes to aggregate over, default: ['polygon']
  --points POINTS       Path to CSV file containing points, default:
  --coordinates, --xy, --coord COORDINATES [COORDINATES ...]
                        Column names for coordinates, default:
  --metadata, -m, --meta METADATA [METADATA ...]
                        Column names for metadata, default:
  --extra_columns, -e, --extra EXTRA_COLUMNS [EXTRA_COLUMNS ...]
                        Columns with constant values to be added to the output
                        file, default:
  --statistics STATISTICS
                        Type of statistics, default: mean
  --dates DATES         Filter dates, can be used to paralellize computations
                        (e.g., over months) and for debugging purposes,
                        default: None
  --shape_files SHAPE_FILES [SHAPE_FILES ...]
                        Path to shape files, default:
  --description DESCRIPTION
                        Description to be added to data dictionary, default:
                        Dorieh data model for aggregations of netCDF data
  --table, -t TABLE     Name of the table where the aggregated data will be
                        stored, default: None
  --output, -o [{aggregation,data_dictionary} ...]
                        What the tool should output, default: ['aggregation']
  --ram RAM             Runtime memory available to the process, default: 2G
```

## Example


```shell
python -u -m dorieh.rasters.launcher --var tmmx -y 2001 --shapes_dir shapes/zip_shape_files --strategy downscale
```

The results can be then found in `data/processed` folder

## Python modules

```{toctree}
---
maxdepth: 2
glob:
---
members/gridmet_tools
members/launcher
members/task
members/registry
```

## CWL pipelines and tools

```{toctree}
---
maxdepth: 2
glob:
---
pipeline/gridmet*
```

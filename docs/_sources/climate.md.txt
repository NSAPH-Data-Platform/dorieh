# Computational Utilities for working with Climate gridMET data

<!-- TODO -->

[Documentation Home](home)


```{contents}
---
local:
---
```

## What is gridMET?

gridMET is a dataset of daily high-spatial resolution (~4-km, 1/24th degree)
surface meteorological data covering the contiguous US from 1979-yesterday.
The data are also known and cited as METDATA.

Executing pipelines from this package require a collection of shape files
corresponding to geographies for which data is aggregated
(for example, zip code areas or counties).

The data has to be placed in the following directory structure:
`${year}/${geo_type: zip|county|etc.}/${shape:point|polygon}/`

Which geography is used is defined by `geography` argument that defaults
to "zip". Only actually used geographies must have their shape files
for the years actually used.

## Using command line gridMET utility 

```
    usage: python -m dorieh.rasters.launcher [-h] --variable
                      {bi,erc,etr,fm100,fm1000,pet,pr,rmax,rmin,sph,srad,th,tmmn,tmmx,vpd,vs}
                      [{bi,erc,etr,fm100,fm1000,pet,pr,rmax,rmin,sph,srad,th,tmmn,tmmx,vpd,vs} ...]
                      [--strategy {default,all_touched,combined}]
                      [--destination DESTINATION] [--downloads DOWNLOADS]
                      [--geography GEOGRAPHY] [--shapes_dir SHAPES_DIR]
                      [--shapes [SHAPES [SHAPES ...]]]
    
    optional arguments:
      -h, --help            show this help message and exit
      --years [YEARS [YEARS ...]], -y [YEARS [YEARS ...]]
                            Year or list of years to download. For example, the
                            following argument: `-y 1992:1995 1998 1999 2011
                            2015:2017` will produce the following list:
                            [1992,1993,1994,1995,1998,1999,2011,2015,2016,2017] ,
                            default: 1990:2020
      --compress, -c        Use gzip compression for the result, default: True
      --variables {bi,erc,etr,fm100,fm1000,pet,pr,rmax,rmin,sph,srad,th,tmmn,tmmx,vpd,vs} [{bi,erc,etr,fm100,fm1000,pet,pr,rmax,rmin,sph,srad,th,tmmn,tmmx,vpd,vs} ...], --var {bi,erc,etr,fm100,fm1000,pet,pr,rmax,rmin,sph,srad,th,tmmn,tmmx,vpd,vs} [{bi,erc,etr,fm100,fm1000,pet,pr,rmax,rmin,sph,srad,th,tmmn,tmmx,vpd,vs} ...]
                            Gridmet bands or variables
      --strategy {default,all_touched,combined,downscale}, -s {default,all_touched,combined,downscale}
                            Rasterization Strategy, default: default
      --destination DESTINATION, --dest DESTINATION, -d DESTINATION
                            Destination directory for the processed files,
                            default: data/processed
      --raw_downloads RAW_DOWNLOADS
                            Directory for downloaded raw files, default:
                            data/downloads
      --geography {zip,county,custom}
                            The type of geographic area over which we aggregate
                            data, default: zip
      --shapes_dir SHAPES_DIR
                            Directory containing shape files for geographies.
                            Directory structure is expected to be:
                            .../${year}/${geo_type}/{point|polygon}/, default:
                            shapes
      --shapes [{point,polygon} [{point,polygon} ...]]
                            Type of shapes to aggregate over, default: ['polygon']
      --points POINTS       Path to CSV file containing points, default:
      --coordinates COORDINATES [COORDINATES ...], --xy COORDINATES [COORDINATES ...], --coord COORDINATES [COORDINATES ...]
                            Column names for coordinates, default:
      --metadata METADATA [METADATA ...], -m METADATA [METADATA ...], --meta METADATA [METADATA ...]
                            Column names for metadata, default:
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

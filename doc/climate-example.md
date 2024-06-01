# Sample workflow to download and aggregate a given variable (default: maximum temperature) for a given date


 [Source code](climate-examplecwl_src.md) 


![](climate-example.png)

```{contents}
---
local:
---
```

**Workflow**

## Inputs

| Name      | Type   | Default | Description                                                                                                                                                  | 
|:----------|:-------|:--------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| geography | string | `zcta`  | Type of geography: zip codes or counties Valid values: "zip", "zcta" or "county"                                                                             | 
| band      | string | `tmmx`  | University of Idaho Gridded Surface Meteorological Dataset  [bands](https://developers.google.com/earth-engine/datasets/catalog/IDAHO_EPSCOR_GRIDMET#bands)  | 
| date      | string |         | a date to retrieve data for in the 'YYYY-mm-dd' format                                                                                                       | 
| ram       | string | `2GB`   | Runtime memory, available to the process                                                                                                                     | 

## Outputs

| Name             | Type   | Description | 
|:-----------------|:-------|:------------|
| netCDF_file      | File   |             | 
| csv_file         | File   |             | 
| shapefiles       | File[] |             | 
| download_log     | File   |             | 
| download_err     | File   |             | 
| aggregate_log    | File   |             | 
| aggregate_errors | File   |             | 

## Steps

| Name       | Runs                                               | Description                                                                                                                                                                           | 
|:-----------|:---------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| download   | [download.cwl](pipeline/download.md)               | Downloads NetCDF file with gridMET data from Atmospheric Composition Analysis Group                                                                                                   | 
| get_shapes | [get_shapes.cwl](pipeline/get_shapes.md)           | This step downloads Shape files from a given collection (TIGER/Line or GENZ)  and a geography (ZCTA or Counties) from the US Census website, for a given year or for the closest one. | 
| aggregate  | [aggregate_daily.cwl](pipeline/aggregate_daily.md) | This step aggregates gridded data from a NetCDF file over polygons from the provided shapefiles                                                                                       | 


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

| Name       | Runs                                                            | Description                                                                         | 
|:-----------|:----------------------------------------------------------------|:------------------------------------------------------------------------------------|
| download   | [../src/cwl/download.cwl](../src/cwl/download.md)               | Downloads NetCDF file with gridMET data from Atmospheric Composition Analysis Group | 
| get_shapes | [../src/cwl/get_shapes.cwl](../src/cwl/get_shapes.md)           |                                                                                     | 
| aggregate  | [../src/cwl/aggregate_daily.cwl](../src/cwl/aggregate_daily.md) |                                                                                     | 


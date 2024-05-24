# Computational Utilities for working with Exposure data from Washington University in St. Louis
       
## Exposure data by Atmospheric Composition Analysis Group


Various datasets of the exposure data are 
available for download from this website: 
[Atmospheric Composition Analysis Group](https://sites.wustl.edu/acag/datasets/surface-pm2-5).

We have used monthly data for the PM25 absolute values and annual data for 
PM25 and its components due to their relevance in assessing air 
quality and potential health impacts. The data is provided 
as absolute values in ug/m3 units. However, PM25 components are provided as 
percentage values not usable for aggregation. Dorieh utilities convert 
these values into absolute values and combine the result as a single tabular dataset.
          

## Python packages


```{toctree}
---
maxdepth: 2
glob:
---
members/wustl*
members/netCDF*
```
                  
## CWL Workflows

```{toctree}
---
maxdepth: 2
glob:
---
pipeline/pm25_yearly_download
pipeline/wustl
```

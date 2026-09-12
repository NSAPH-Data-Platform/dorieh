# Exposure Data from the Atmospheric Composition Analysis Group at Washington University in St. Louis

This page describes the PM2.5 exposure datasets published by the
[Atmospheric Composition Analysis Group](https://sites.wustl.edu/acag/datasets/surface-pm2-5)
at Washington University in St. Louis, and the Dorieh utilities and
pipelines that download them, convert component percentages to absolute
values, and combine the results into a single tabular dataset.

We use monthly data for absolute PM2.5 values and annual data for
PM2.5 and its components. The absolute values are provided in ug/m3
units, but the PM2.5 components are published as percentage values,
which are not usable for aggregation; Dorieh utilities convert them
into absolute values before combining the results.


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

The exposure pipelines are documented in the
[Data Processing Pipelines](pipelines.md) section:

* [PM2.5 yearly download](pipeline/pm25_yearly_download.md)
* [WashU exposure pipeline](pipeline/wustl.md)

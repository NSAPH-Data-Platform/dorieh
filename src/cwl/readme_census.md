# Census workflow
## Tools
- `census_assemble.cwl`: Initializes the `get_census.DataPlan` object, 
  downloads and calculates the census variables, saves the object out as a pickle
- `census_interpolate.cwl`: Loads `get_census.DataPlan` object, and calls the interpolate
  method. Saves new object out as a pickle
- `census_density.cwl`: Loads `get_census.DataPlan` object, downloads areas for the needed
  geography, can calculates densities for the specified variables
- `census_qc.cwl`: Loads `get_census.DataPlan` object, performs QC on it, logs the result
- `census_write.cwl`: Loads `get_census.DataPlan` object, writes out data schema as a YAML file,
  writes out data as a csv.

## General Workflow:

Contained in `census_workflow.cwl`. Runs `census_assemble.cwl` to download the data. 
Then runs `census_interpolate.cwl` to create an interpolated version of the data. Then for
both the interpolated and uninterpolated data calculates densities, does QC, then writes out
the data.

#!/usr/bin/env cwl-runner
### Aggregates data in NetCDF file over given geographies
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

cwlVersion: v1.2
class: CommandLineTool
baseCommand: [python, -m, dorieh.rasters.file_processors.wustl_file_processor]

requirements:
  InlineJavascriptRequirement: {}
  ResourceRequirement:
    coresMin: 2
    ramMin: 8192
    outdirMin: 5120
    # coresMax: 6


doc: |
  This tool aggregates data in NetCDF or GeoTiff file over provided shapes
  (zip codes or counties). It produces mean values over shape.
  
  The tool expects one value for every variable in every grid node. 
  The variables are expected to be formatted as they are for 
  [Atmospheric Composition Analysis Group of Washington University](https://sites.wustl.edu/acag/datasets/surface-pm2-5/)
  
  See also [aggregate_daily.cwl](aggregate_daily) - a tool, that expects 
  multiple (daily) values at every grid node.


hints:
  DockerRequirement:
    dockerPull: forome/dorieh

inputs:
  strategy:
    type: string
    default: downscale
    inputBinding:
      prefix: --strategy
    doc: "Rasterization strategy"
  ram:
    type: string
    default: 2GB
    doc: Runtime memory, available to the process
    inputBinding:
      prefix: --ram
  shapes_dir:
    type: Directory?
    inputBinding:
      prefix: --shapes_dir
  band:
    type: string[]
    inputBinding:
      prefix: --var
  geography:
    type: string
    doc: |
      Type of geography: zip codes or counties
    inputBinding:
      prefix: --geography
  netcdf_data:
    type: File
    doc: "Path to downloaded file"
    inputBinding:
      prefix: --raw_downloads
  shape_files:
    type: File[]?
    doc: "Paths to shape files"
    inputBinding:
      prefix: --shape_files
  output_type:
    type: string[]
    doc: What to output as the result of executing the tool
    default:
      - aggregation
      - data_dictionary
    inputBinding:
      prefix: --output
  table:
    type: string?
    doc: |
      Optional name ot the table where the aggregated data will be
      eventually stored
    inputBinding:
      prefix: --table

arguments:
  - valueFrom: "."
    prefix: --destination

outputs:
  log:
    type: File?
    outputBinding:
      glob: "*.log"
  csv_data:
    type: File
    outputBinding:
      glob:
        - "*.csv*"
        - "**/*.csv*"
    doc: |
      The output CSV file, containing mean values of the given
      variable over given geographies. Each line
      contains date, geo id (zip or county FIPS) and value
  data_dictionary:
    type: File?
    outputBinding:
      glob:
        - "*.yaml"
        - "**/*.yaml"
    doc: |
      Data dictionary for teh aggregated data

  errors:
    type: stderr

stderr: $("aggr-" + inputs.netcdf_data.nameroot + ".err")

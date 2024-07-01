#!/usr/bin/env cwl-runner
### Workflow to aggregate and ingest NetCDF files for one year
#  Copyright (c) 2021-2022. Harvard University
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
class: Workflow

requirements:
  SubworkflowFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  InlineJavascriptRequirement: {}
  ScatterFeatureRequirement: {}
  MultipleInputFeatureRequirement: {}


doc: |
  Sub-workflow to aggregate a NetCDF file for one year over a given
  geography (zip codes or counties). Before aggregation, downloads
  shape files fo this year from US Census website

inputs:
  depends_on:
    type: Any?
  proxy:
    type: string?
    default: ""
    doc: HTTP/HTTPS Proxy if required
  downloads:
    type: Directory
  geography:
    type: string
  variable:
    type: string
  component:
    type: string[]
  year:
    type: int
  strategy:
    type: string
    doc: "Rasterization strategy"
  ram:
    type: string
    default: 2GB
    doc: Runtime memory, available to the process
  shape_file_collection:
    type: string
    default: tiger
    doc: |
      [Collection of shapefiles](https://www2.census.gov/geo/tiger), 
      either GENZ or TIGER
  table:
    type: string?
    doc: |
      Optional name ot the table where the aggregated data will be
      eventually stored

steps:
  get_shapes:
    run: get_shapes.cwl
    doc: |
      This step downloads Shape files from a given collection (TIGER/Line or GENZ) 
      and a geography (ZCTA or Counties) from the US Census website,
      for a given year or for the closest one.

    in:
      year:
        valueFrom: $(String(inputs.yy))
      yy: year
      geo: geography
      collection: shape_file_collection
      proxy: proxy
    out:
      - shape_files

  find_pm25_file:
    doc: |
      Given input directory, variable (band), year and month,
      evaluates the expected file name for the main variable input data
    run:  wustl_file_pattern.cwl
    in:
      year: year
      variables:
        valueFrom: $([inputs.variable])
      variable: variable
      downloads: downloads
    out: [netcdf_files]

  find_components_files:
    doc: |
      Given input directory, variable (band), year and month,
      evaluates the expected file name for the main variable input data
    run:  wustl_file_pattern.cwl
    in:
      year: year
      variables: component
      downloads: downloads
    out: [netcdf_files]

  consolidate:
    doc: consolidate components into one file
    run: wustl_consolidate_components.cwl
    in:
      abs_values: find_pm25_file/netcdf_files
      components: find_components_files/netcdf_files
    out:
      - consolidated_data

  aggregate:
    doc: Aggregate data over geographies
    run: aggregate_wustl.cwl
    in:
      strategy: strategy
      ram: ram
      geography: geography
      netcdf_data: consolidate/consolidated_data
      shape_files: get_shapes/shape_files
      variable: variable
      components: component
      table: table
      band:
        valueFrom: $([inputs.variable].concat(inputs.components))
    out:
      - log
      - errors
      - csv_data
      - data_dictionary

outputs:
  shapes:
    type: File[]
    outputSource: get_shapes/shape_files

  consolidated_data:
    type: File
    outputSource: consolidate/consolidated_data
  aggregate_data:
    type: File
    outputSource: aggregate/csv_data
  data_dictionary:
    type: File?
    outputSource: aggregate/data_dictionary
  aggregate_log:
    type: File?
    outputSource: aggregate/log
  aggregate_err:
    type: File
    outputSource: aggregate/errors







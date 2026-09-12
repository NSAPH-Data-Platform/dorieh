#!/usr/bin/env cwl-runner
### Sample workflow to download and aggregate a given variable (default: maximum temperature) for a given date
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
  NetworkAccess:
    networkAccess: True

#hints:
#  DockerRequirement:
#    dockerPull: forome/dorieh


inputs:
  geography:
    type: string
    default: zcta
    doc: |
      Type of geography: zip codes or counties
      Valid values: "zip", "zcta" or "county"
  band:
    type: string
    default: tmmx
    doc: |
      University of Idaho Gridded Surface Meteorological Dataset 
      [bands](https://developers.google.com/earth-engine/datasets/catalog/IDAHO_EPSCOR_GRIDMET#bands)
  date:
    type: string
    doc: a date to retrieve data for in the 'YYYY-mm-dd' format
  ram:
    type: string
    default: 2GB
    doc: Runtime memory, available to the process

steps:
  download:
    run: https://raw.githubusercontent.com/ForomePlatform/dorieh/main/src/cwl/download.cwl
    doc: Downloads NetCDF file with gridMET data from Atmospheric Composition Analysis Group
    in:
      year:
        valueFrom: $(inputs.date.split('-')[0])
      band: band
      date: date
    out:
      - data
      - log
      - errors
  get_shapes:
    run: https://raw.githubusercontent.com/ForomePlatform/dorieh/main/src/cwl/get_shapes.cwl
    doc: |
      This step downloads Shape files from a given collection (TIGER/Line or GENZ) 
      and a geography (ZCTA or Counties) from the US Census website,
      for a given year or for the closest one.

    in:
      year:
        valueFrom: $(inputs.date.split('-')[0])
      geo: geography
      date: date
    out: [shape_files]
  aggregate:
    run: https://raw.githubusercontent.com/ForomePlatform/dorieh/main/src/cwl/aggregate_daily.cwl
    doc: |
      This step aggregates gridded data from a NetCDF file over polygons from the provided shapefiles
    in:
      geography: geography
      year:
        valueFrom: $(inputs.date.split('-')[0])
      dates:
        valueFrom: $(inputs.date + ':' + inputs.date)
      band: band
      input: download/data
      date: date
      ram: ram
      shape_files: get_shapes/shape_files
    out:
      - data
      - log
      - errors

outputs:
  netCDF_file:
    type: File?
    outputSource: download/data
  csv_file:
    type: File?
    outputSource: aggregate/data
  shapefiles:
    type: File[]
    outputSource: get_shapes/shape_files

  download_log:
    type: File?
    outputSource: download/log
  download_err:
    type: File?
    outputSource: download/errors

  aggregate_log:
    type: File?
    outputSource: aggregate/log
  aggregate_errors:
    type: File?
    outputSource: aggregate/errors

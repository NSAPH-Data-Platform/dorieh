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
  Sub-workflow to aggregate and ingest NetCDF files for one year over a given
  geography (zip codes or counties) and ingest the
  aggregated data into the database. Before aggregation, downloads
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
  shape_file_collection:
    type: string
    default: tiger
    doc: |
      [Collection of shapefiles](https://www2.census.gov/geo/tiger), 
      either GENZ or TIGER
  table:
    type: string
  band:
    type: string
    default: pm25
  months:
    type: int[]
  year:
    type: int
  strategy:
    type: string
    doc: "Rasterization strategy"
  ram:
    type: string
    default: 2GB
    doc: Runtime memory, available to the process
  database:
    type: File
  connection_name:
    type: string

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
      proxy: proxy
      collection: shape_file_collection
    out: [shape_files]

  process_files:
    doc: Aggregates and ingests relvant files
    run: wustl_one_file.cwl
    scatter:
      - month
    in:
      year: year
      month: months
      band: band
      table: table
      geography:  geography
      strategy: strategy
      ram: ram
      database: database
      connection_name: connection_name
      shape_files: get_shapes/shape_files
      downloads: downloads
    out:
      - aggregate_data
      - aggregate_log
      - aggregate_err
      - ingest_log
      - ingest_err

outputs:
  aggregate_data:
    type: File[]
    outputSource: process_files/aggregate_data
  aggregate_log:
    type: File[]
    outputSource: process_files/aggregate_log
  aggregate_err:
    type: File[]
    outputSource: process_files/aggregate_err

  ingest_log:
    type: File[]
    outputSource: process_files/ingest_log
  ingest_err:
    type: File[]
    outputSource: process_files/ingest_err






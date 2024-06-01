#!/usr/bin/env cwl-runner
### Workflow to aggregate and ingest one gridMET file in NetCDF format
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
  Sub-workflow that aggregates a single NetCDF file over a given
  geography (zip codes or counties) and ingest the
  aggregated data into the database

inputs:
  depends_on:
    type: Any?
  proxy:
    type: string?
  model:
    type: File
  shapes:
    type: Directory?
  geography:
    type: string
  year:
    type: string
  band:
    type: string
  domain:
    type: string
  table:
    type: string
  database:
    type: File
  connection_name:
    type: string
  dates:
    type: string?
  strategy:
    type: string
  ram:
    type: string
    default: 2GB
    doc: Runtime memory, available to the process
  months:
    type: int[]
    default: [1,2,3,4,5,6,7,8,9,10,11,12]

steps:
  download:
    run: download.cwl
    doc: Downloads data
    in:
      year: year
      band: band
      proxy: proxy
    out:
      - data
      - log
      - errors

  get_shapes:
    run: get_shapes.cwl
    doc: |
      This step downloads Shape files from a given collection (TIGER/Line or GENZ) 
      and a geography (ZCTA or Counties) from the US Census website,
      for a given year or for the closest one.

    in:
      year: year
      geo: geography
      proxy: proxy
    out: [shape_files]

  add_data:
    run: add_daily_data.cwl
    doc: Processes data
    scatter: month
    in:
      proxy: proxy
      shapes: shapes
      geography: geography
      year: year
      dates: dates
      band: band
      input: download/data
      strategy: strategy
      ram: ram
      shape_files: get_shapes/shape_files
      month: months
      registry: model
      domain: domain
      table: table
      database: database
      connection_name: connection_name
    out:
      - aggregate_log
      - data
      - aggregate_errors
      - ingest_log
      - ingest_errors


  # do not need indexing as we define indices in advance

  vacuum:
    run: vacuum.cwl
    in:
      depends_on: add_data/ingest_log
      domain: domain
      registry: model
      table: table
      database: database
      connection_name: connection_name
    out: [log, errors]

outputs:
  download_log:
    type: File?
    outputSource: download/log
  download_err:
    type: File?
    outputSource: download/errors

  add_data_aggregate_log:
    type: File[]?
    outputSource: add_data/aggregate_log
  add_data_data:
    type: File[]?
    outputSource: add_data/data
  add_data_aggregate_errors:
    type: File[]?
    outputSource: add_data/aggregate_errors
  add_data_ingest_log:
    type: File[]?
    outputSource: add_data/ingest_log
  add_data_ingest_errors:
    type: File[]
    outputSource: add_data/ingest_errors

  vacuum_log:
    type: File
    outputSource: vacuum/log
  vacuum_err:
    type: File
    outputSource: vacuum/errors

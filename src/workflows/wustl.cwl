#!/usr/bin/env cwl-runner
### Pipeline to ingest Monthly Pollution data downloaded from WashU Box

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


doc: |
  Workflow to aggregate pollution data coming in NetCDF format
  over given geographies (zip codes or counties) and ingest the
  aggregated data into the database

inputs:
  proxy:
    type: string?
    default: ""
    doc: HTTP/HTTPS Proxy if required
  shapes:
    type: Directory?
    doc: Do we even need this parameter, as we isntead downloading shapes?
  shape_file_collection:
    type: string
    default: tiger
    doc: |
      [Collection of shapefiles](https://www2.census.gov/geo/tiger), 
      either GENZ or TIGER
  downloads:
    type: Directory
    doc: Directory, containing files, downloaded and unpacked from WUSTL box
  geography:
    type: string
    doc: |
      Type of geography: zip codes or counties
      Valid values: "zip" or "county"
  years:
    type: int[]
    default: [2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]
  months:
    type: int[]
    default: [1,2,3,4,5,6,7,8,9,10,11,12]
  band:
    type: string
    default: pm25
  strategy:
    type: string
    default: downscale
    doc: "Rasterization strategy"
  ram:
    type: string
    default: 2GB
    doc: Runtime memory, available to the process
  database:
    type: File
    doc: Path to database connection file, usually database.ini
  connection_name:
    type: string
    doc: The name of the section in the database.ini file

steps:
  initdb:
    run: initdb.cwl
    doc: Ensure that database utilities are at their latest version
    in:
      database: database
      connection_name: connection_name
    out:
      - log
      - err

  make_table_name:
    doc: Given variable and geography type (zip/county) evaluates table name
    run:
      class: ExpressionTool
      inputs:
        geography:
          type: string
        band:
          type: string
      expression: "$({'table': (inputs.band + '_monthly_' + inputs.geography + '_mean')})"
      outputs:
        table:
          type: string
    in:
      geography: geography
      band: band
    out: [table]

  init_tables:
    doc: creates or recreates database tables, one for each band and geography
    run: reset.cwl
    in:
      domain:
        valueFrom: "exposures"
      database: database
      connection_name: connection_name
      table: make_table_name/table
      depends_on: initdb/log
    out:
      - log
      - errors

  process:
    doc: Downloads raw data and aggregates it over shapes and time
    scatter:
      - year
    run: wustl_one_year.cwl
    in:
      proxy: proxy
      depends_on: init_tables/log
      downloads: downloads
      geography: geography
      year: years
      months: months
      band: band
      strategy: strategy
      ram: ram
      database: database
      connection_name: connection_name
      table: make_table_name/table
      shape_file_collection: shape_file_collection
    out:
      - aggregate_data
      - aggregate_log
      - aggregate_err
      - ingest_log
      - ingest_err

  index:
    run: index.cwl
    in:
      depends_on: process/ingest_log
      domain:
        valueFrom: "exposures"
      table: make_table_name/table
      database: database
      connection_name: connection_name
    out: [log, errors]

  vacuum:
    run: vacuum.cwl
    in:
      depends_on: index/log
      domain:
        valueFrom: "exposures"
      table: make_table_name/table
      database: database
      connection_name: connection_name
    out: [log, errors]


outputs:
  data:
    type:
      type: array
      items:
        type: array
        items: [File]
    outputSource: process/aggregate_data

  aggregate_log:
    type:
      type: array
      items:
        type: array
        items: [File]
    outputSource: process/aggregate_log
  aggregate_err:
    type:
      type: array
      items:
        type: array
        items: [File]
    outputSource: process/aggregate_err

  ingest_log:
    type:
      type: array
      items:
        type: array
        items: [File]
    outputSource: process/ingest_log
  ingest_err:
    type:
      type: array
      items:
        type: array
        items: [File]
    outputSource: process/ingest_err

  reset_log:
    type: File
    outputSource: init_tables/log
  reset_err:
    type: File
    outputSource: init_tables/errors

  index_log:
    type: File
    outputSource: index/log
  index_err:
    type: File
    outputSource: index/errors

  vacuum_log:
    type: File
    outputSource: vacuum/log
  vacuum_err:
    type: File
    outputSource: vacuum/errors

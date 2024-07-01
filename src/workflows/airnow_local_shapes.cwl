#!/usr/bin/env cwl-runner
### Full AirNowProcessing Pipeline (with shapefiles on local file system)
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
class: Workflow

requirements:
  SubworkflowFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  InlineJavascriptRequirement: {}

doc: |
  This workflow downloads AirNow data from the government
  servers, introspects it to infer the database schema
  and ingests the data into the database

inputs:
  proxy:
    type: string?
    default: ""
    doc: HTTP/HTTPS Proxy if required
  api-key:
    type: string
    doc: API key for AirNow
  database:
    type: File
    doc: Path to database connection file, usually database.ini
  connection_name:
    type: string
    doc: The name of the section in the database.ini file
  from:
    type: string
    doc: Start date for downolading, in YYYY-MM-DD format
  to:
    type: string
    doc: End date for downolading, in YYYY-MM-DD format
  parameter_code:
    type: string
    doc: |
      Parameter code. Either a numeric code (e.g. 88101, 44201)
      or symbolic name (e.g. PM25, NO2).
      See more: [AQS Code List](https://www.epa.gov/aqs/aqs-code-list)
  table:
    doc: Name of the table to be created in the database
    type: string
  shapes:
    type: File[]
    secondaryFiles:
      - "^.dbf"
      - "^.shx"
      - "^.prj"
      - "^.cpg"

steps:
  download:
    run: download_airnow.cwl
    in:
      api-key: api-key
      shapes: shapes
      from: from
      to: to
      table: table
      parameter_code: parameter_code
      proxy: proxy
    out: [log, data]

  introspect:
    run: introspect.cwl
    in:
      depends_on: download/log
      input: download/data
      table: table
      output:
        valueFrom: epa.yaml
    out: [log, model]

  ingest:
    run: ingest.cwl
    doc: Uploads data into the database
    in:
      registry: introspect/model
      table: table
      input: download/data
      database: database
      connection_name: connection_name
    out: [log]

  index:
    run: index.cwl
    in:
      depends_on: ingest/log
      registry: introspect/model
      domain:
        valueFrom: "epa"
      table: table
      database: database
      connection_name: connection_name
    out: [log]

outputs:
  download_log:
    type: File
    outputSource: download/log
  ingest_log:
    type: File
    outputSource: ingest/log
  index_log:
    type: File
    outputSource: index/log
  download_data:
    type: File
    outputSource: download/data
  model:
    type: File
    outputSource: introspect/model

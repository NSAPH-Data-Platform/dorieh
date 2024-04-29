#!/usr/bin/env cwl-runner
### Downloader of gridMET Data
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
  InlineJavascriptRequirement: {}


doc: |
  This tool preprocesses gridMET to aggregate over shapes
  (zip codes or counties) and time. It produces daily mean values

inputs:
  proxy:
    type: string?
    default: ""
    doc: HTTP/HTTPS Proxy if required
  strategy:
    type: string
    default: downscale
    doc: "Rasterization strategy"
  ram:
    type: string
    default: 2GB
    doc: Runtime memory, available to the process
  shapes:
    type: Directory?
  geography:
    type: string
    doc: |
      Type of geography: zip codes or counties
  year:
    type: string
    doc: "Year to process"
  month:
    type: int?
    doc: If given, then process just one month
  band:
    type: string
    doc: |
      [Gridmet Band](https://developers.google.com/earth-engine/datasets/catalog/IDAHO_EPSCOR_GRIDMET#bands)
  dates:
    type: string?
    doc: 'dates restriction, for testing purposes only'
  input:
    type: File
    doc: "Downloaded file"
  shape_files:
    type: File[]
    doc: "Paths to shape files"
  domain:
    type: string
  table:
    type: string
  database:
    type: File
  connection_name:
    type: string
  registry:
    type: File

steps:
  aggregate:
    run: aggregate_daily.cwl
    in:
      proxy: proxy
      shapes: shapes
      geography: geography
      year: year
      dates: dates
      band: band
      input: input
      strategy: strategy
      ram: ram
      shape_files: shape_files
      month: month
    out:
      - data
      - log
      - errors

  ingest:
    run: add_data.cwl
    doc: Uploads data into the database
    in:
      registry: registry
      domain: domain
      table: table
      input: aggregate/data
      database: database
      connection_name: connection_name
    out:
      - log
      - errors


outputs:
  aggregate_log:
    type: File?
    outputSource: aggregate/log
  data:
    type: File?
    outputSource: aggregate/data
  aggregate_errors:
    type: File?
    outputSource: aggregate/errors
  ingest_log:
    type: File?
    outputSource: ingest/log
  ingest_errors:
    type: File
    outputSource: ingest/errors


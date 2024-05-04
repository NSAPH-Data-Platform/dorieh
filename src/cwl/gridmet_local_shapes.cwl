#!/usr/bin/env cwl-runner
### gridMET Pipeline
#  Copyright (c) 2021. Harvard University
#
#  Developed by Research Software Engineering,
#  Faculty of Arts and Sciences, Research Computing (FAS RC)
#  Author: Quantori LLC
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

hints:
  ResourceRequirement:
    coresMin: 24
    coresMax: 32

doc: |
  Downloads, processes gridMET data and ingests it into the database

inputs:
  proxy:
    type: string?
    default: ""
    doc: HTTP/HTTPS Proxy if required
  shapes:
    type: Directory?
  geography:
    type: string
    doc: |
      Type of geography: zip codes or counties
  years:
    type: string[]
#    default: ['1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
  bands:
    type: string[]
#    default: ['bi', 'erc', 'etr', 'fm100', 'fm1000', 'pet', 'pr', 'rmax', 'rmin', 'sph', 'srad', 'th', 'tmmn', 'tmmx', 'vpd', 'vs']
  database:
    type: File
    doc: Path to database connection file, usually database.ini
  connection_name:
    type: string
    doc: The name of the section in the database.ini file
  dates:
    type: string?
    doc: 'dates restriction, for testing purposes only'
  nc:
    type: File
  shape_files:
    type: File[]
    secondaryFiles:
      - "^.dbf"
      - "^.shx"
      - "^.prj"
      - "^.cpg"

steps:
  registry:
    run: build_gridmet_model.cwl
    doc: Writes down YAML file with the database model
    in: []
    out:
      - model
      - log
      - errors

  process:
    scatter: band
    in:
      proxy: proxy
      model: registry/model
      shapes: shapes
      geography: geography
      years: years
      dates: dates
      band: bands
      database: database
      connection_name: connection_name
      nc: nc
      shape_files: shape_files
      table:
        valueFrom: $(inputs.geography + '_' + inputs.band)

    run:
      class: Workflow
      inputs:
        proxy:
          type: string?
        model:
          type: File
        shapes:
          type: Directory?
        geography:
          type: string
        years:
          type: string[]
        band:
          type: string
        table:
          type: string
        database:
          type: File
        connection_name:
          type: string
        dates:
          type: string?
        nc:
          type: File
        shape_files:
          type: File[]

      steps:
        process:
          run: add_daily_data.cwl
          doc: Processes data
          scatter: year
          scatterMethod:  nested_crossproduct
          in:
            proxy: proxy
            shapes: shapes
            geography: geography
            year: years
            dates: dates
            band: band
            input: nc
            shape_files: shape_files
          out:
            - data
            - log

        ingest:
          run: ingest.cwl
          doc: Uploads data into the database
          in:
            registry: model
            domain:
              valueFrom: "gridmet"
            table: table
            input: process/data
            database: database
            connection_name: connection_name
          out: [log, errors]

        index:
          run: index.cwl
          in:
            depends_on: ingest/log
            registry: model
            domain:
              valueFrom: "gridmet"
            table: table
            database: database
            connection_name: connection_name
          out: [log, errors]

        vacuum:
          run: vacuum.cwl
          in:
            depends_on: index/log
            domain:
              valueFrom: "gridmet"
            registry: model
            table: table
            database: database
            connection_name: connection_name
          out: [log, errors]
      outputs:
        process_data:
          type: File[]
          outputSource: process/data
        process_log:
          type: File[]
          outputSource: process/log

        ingest_log:
          type: File
          outputSource: ingest/log
        ingest_err:
          type: File
          outputSource: ingest/errors

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
    out:
      - process_data
      - process_log
      - ingest_log
      - ingest_err
      - index_log
      - index_err
      - vacuum_log
      - vacuum_err



outputs:
  registry:
    type: File?
    outputSource: registry/model
  registry_log:
    type: File?
    outputSource: registry/log

  data:
    type:
      type: array
      items:
        type: array
        items: [File]
    outputSource: process/process_data

  process_log:
    type:
      type: array
      items:
        type: array
        items: [File]
    outputSource: process/process_log

  ingest_log:
    type: File[]
    outputSource: process/ingest_log
  ingest_err:
    type: File[]
    outputSource: process/ingest_err

  index_log:
    type: File[]
    outputSource: process/index_log
  index_err:
    type: File[]
    outputSource: process/index_err

  vacuum_log:
    type: File[]
    outputSource: process/vacuum_log
  vacuum_err:
    type: File[]
    outputSource: process/vacuum_err

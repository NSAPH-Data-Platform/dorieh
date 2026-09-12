#!/usr/bin/env cwl-runner
### Full EPA AQS Processing Pipeline
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
  ScatterFeatureRequirement: {}

doc: |
  This workflow downloads AQS data from the government
  servers, introspects it to infer the database schema
  and ingests the data into the database

  Example run:
  ```shell
  cwl-runner aqs.cwl sample_aqs_annual.yml
  ```

  See [sample_aqs_annual.yml](sample_aqs.md)

  Or

  ```shell
  cwl-runner /opt/airflow/project/epa/src/cwl/aqs.cwl --database /opt/airflow/project/database.ini --connection_name nsaph2 --agregation annual --parameter_code PM25 --table pm25_annual --proxy $HTTP_PROXY
  ```


inputs:
  proxy:
    type: string?
    default: ""
    doc: HTTP/HTTPS Proxy if required
  database:
    type: File
    doc: Path to database connection file, usually database.ini
  connection_name:
    type: string
    doc: The name of the section in the database.ini file
  aggregation:
    type: string
  parameter_code:
    type: string
    doc: |
      Parameter code. Either a numeric code (e.g. 88101, 44201)
      or symbolic name (e.g. PM25, NO2).
      See more: [AQS Code List](https://www.epa.gov/aqs/aqs-code-list)
  table:
    doc: Name of the table to be created in the database
    type: string
  years:
    type: string[]
    doc: Years to download

steps:
  initdb:
    run: initcoredb.cwl
    doc: Ensure that database utilities are at their latest version
    in:
      database: database
      connection_name: connection_name
    out:
      - log
      - err

  download:
    run: download_aqs.cwl
    scatter: year
    in:
      year: years
      aggregation: aggregation
      parameter_code: parameter_code
      proxy: proxy
    out: [data]

  expand:
    run: expand_aqs.cwl
    in:
      parameter_code: parameter_code
      input: download/data
    out: [log, data]

  introspect:
    run: introspect.cwl
    in:
      depends_on: expand/log
      input: expand/data
      table: table
      output:
        valueFrom: epa.yaml
    out: [log, model, errors]

  ingest:
    run: ingest.cwl
    doc: Uploads data into the database
    in:
      depends_on: initdb/log
      registry: introspect/model
      domain:
        valueFrom: "epa"
      table: table
      input: expand/data
      database: database
      connection_name: connection_name
    out: [log, errors]

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
    out: [log, errors]

  vacuum:
    run: vacuum.cwl
    in:
      depends_on: index/log
      registry: introspect/model
      domain:
        valueFrom: "epa"
      table: table
      database: database
      connection_name: connection_name
    out: [log, errors]

  export:
    run: export.cwl
    in:
      depends_on: ingest/log
      database: database
      connection_name: connection_name
      format:
        valueFrom: "parquet"
      table_base_name: table
      table:
        valueFrom: $('epa.' + inputs.table_base_name)
      partition:
        valueFrom: $(["year"])
      output:
        valueFrom: $('export/' + inputs.table_base_name)
    out:
      - data
      - log
      - errors


outputs:
  initdb_log:
    type: File
    outputSource: initdb/log
  expand_log:
    type: File
    outputSource: expand/log
  introspect_log:
    type: File
    outputSource: introspect/log
  ingest_log:
    type: File
    outputSource: ingest/log
  index_log:
    type: File
    outputSource: index/log
  vacuum_log:
    type: File
    outputSource: vacuum/log
  data:
    type: File
    outputSource: expand/data
  model:
    type: File
    outputSource: introspect/model
  introspect_err:
    type: File
    outputSource: introspect/errors
  ingest_err:
    type: File
    outputSource: ingest/errors
  index_err:
    type: File
    outputSource: index/errors
  vacuum_err:
    type: File
    outputSource: vacuum/errors

  export_data:
    type: ['File', 'Directory']
    outputSource: export/data
  export_log:
    type: File
    outputSource: export/log
  export_err:
    type: File
    outputSource: export/errors

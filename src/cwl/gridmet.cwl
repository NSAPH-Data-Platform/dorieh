#!/usr/bin/env cwl-runner
### Pipeline to aggregate data from Climatology Lab
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
  This workflow downloads NetCDF datasets from 
  [University of Idaho Gridded Surface Meteorological Dataset](https://www.northwestknowledge.net/metdata/data/), 
  aggregates gridded data to daily mean values over chosen geographies
  and optionally ingests it into the database.
  
  The output of the workflow are gzipped CSV files containing
  aggregated data. 
  
  Optionally, the aggregated data can be ingested into a database
  specified in the connection parameters:
  
  * `database.ini` file containing connection descriptions
  * `connection_name` a string referring to a section in the `database.ini`
     file, identifying specific connection to be used.

  The workflow can be invoked either by providing command line options 
  as in the following example:
  
      toil-cwl-runner --retryCount 1 --cleanWorkDir never \ 
          --outdir /scratch/work/exposures/outputs \ 
          --workDir /scratch/work/exposures \
          gridmet.cwl \  
          --database /opt/local/database.ini \ 
          --connection_name dorieh \ 
          --bands rmin rmax \ 
          --strategy auto \ 
          --geography zcta \ 
          --ram 8GB

  Or, by providing a YaML file (see [example](jobs/test_gridmet_job)) 
  with similar options:
  
      toil-cwl-runner --retryCount 1 --cleanWorkDir never \ 
          --outdir /scratch/work/exposures/outputs \ 
          --workDir /scratch/work/exposures \
          gridmet.cwl test_gridmet_job.yml 
  

inputs:
  proxy:
    type: string?
    default: ""
    doc: HTTP/HTTPS Proxy if required
  shapes:
    type: Directory?
    doc: Do we even need this parameter, as we instead downloading shapes?
  geography:
    type: string
    doc: |
      Type of geography: zip codes or counties
      Valid values: "zip", "zcta" or "county"
  years:
    type: string[]
    default: ['1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
  bands:
    doc: |
      University of Idaho Gridded Surface Meteorological Dataset 
      [bands](https://developers.google.com/earth-engine/datasets/catalog/IDAHO_EPSCOR_GRIDMET#bands)
    type: string[]
    # default: ['bi', 'erc', 'etr', 'fm100', 'fm1000', 'pet', 'pr', 'rmax', 'rmin', 'sph', 'srad', 'th', 'tmmn', 'tmmx', 'vpd', 'vs']
  strategy:
    type: string
    default: auto
    doc: |
      [Rasterization strategy](https://nsaph-data-platform.github.io/nsaph-platform-docs/common/gridmet/doc/strategy.html)
      used for spatial aggregation
  ram:
    type: string
    default: 2GB
    doc: |
      Runtime memory, available to the process. When aggregation
      strategy is `auto`, this value is used to calculate the optimal
      downscaling factor for the available resources. 
  database:
    type: File
    doc: Path to database connection file, usually database.ini
  connection_name:
    type: string
    doc: The name of the section in the database.ini file
  dates:
    type: string?
    doc: 'dates restriction, for testing purposes only'
  domain:
    type: string
    default: climate


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

  init_db_schema:
    doc: We need to do it because of parallel creation of tables
    run:
      class: CommandLineTool
      baseCommand: [python, -m, dorieh.platform.util.psql]
      doc: |
        This tool executes an SQL statement in the database to grant
        read privileges to NSAPH users (memebrs of group nsaph_admin)
      inputs:
        database:
          type: File
          doc: Path to database connection file, usually database.ini
          inputBinding:
            prefix: --db
        connection_name:
          type: string
          doc: The name of the section in the database.ini file
          inputBinding:
            prefix: --connection
        domain:
          type: string
          #default: climate
      arguments:
        - valueFrom: $("CREATE SCHEMA IF NOT EXISTS " + inputs.domain + ';')
          position: 3
      outputs:
        log:
          type: stdout
        err:
          type: stderr
      stderr: "schema.err"
      stdout: "schema.log"
    in:
      database: database
      connection_name: connection_name
      domain: domain
    out:
      - log
      - err

  make_registry:
    run: build_gridmet_model.cwl
    doc: Writes down YAML file with the database model
    in:
      depends_on: init_db_schema/log
      domain: domain
    out:
      - model
      - log
      - errors

  init_tables:
    doc: creates or recreates database tables, one for each band
    scatter:
      - band
    run:
      class: Workflow
      inputs:
        registry:
          type: File
        table:
          type: string
        domain:
          type: string
        database:
          type: File
        connection_name:
          type: string
      steps:
        reset:
          run: reset.cwl
          in:
            registry:  registry
            domain: domain
            database: database
            connection_name: connection_name
            table: table
          out:
            - log
            - errors
        index:
          run: index.cwl
          in:
            depends_on: reset/log
            registry: registry
            domain: domain
            table: table
            database: database
            connection_name: connection_name
          out: [log, errors]
      outputs:
        reset_log:
          type: File
          outputSource: reset/log
        reset_err:
          type: File
          outputSource: reset/errors
        index_log:
          type: File
          outputSource: index/log
        index_err:
          type: File
          outputSource: index/errors
    in:
      registry:  make_registry/model
      database: database
      connection_name: connection_name
      band: bands
      geography: geography
      domain: domain
      table:
        valueFrom: $(inputs.geography + '_' + inputs.band)
    out:
      - reset_log
      - reset_err
      - index_log
      - index_err

  process:
    run: gridmet_one_file.cwl
    doc: Downloads raw data and aggregates it over shapes and time
    scatter:
      - band
      - year
    scatterMethod: nested_crossproduct

    in:
      proxy: proxy
      depends_on: init_tables/index_log
      model: make_registry/model
      shapes: shapes
      geography: geography
      strategy: strategy
      ram: ram
      year: years
      dates: dates
      band: bands
      database: database
      connection_name: connection_name
      domain: domain
      months:
        valueFrom: $([1,2,3,4,5,6,7,8,9,10,11,12])
      table:
        valueFrom: $(inputs.geography + '_' + inputs.band)

    out:
      - download_log
      - download_err
      - add_data_aggregate_errors
      - add_data_data
      - add_data_aggregate_log
      - add_data_ingest_log
      - add_data_ingest_errors
      - vacuum_log
      - vacuum_err

outputs:
  initdb_log:
    type: File?
    outputSource: initdb/log
  initdb_err:
    type: File?
    outputSource: initdb/err

  init_schema_log:
    type: File?
    outputSource: init_db_schema/log
  init_schema_err:
    type: File?
    outputSource: init_db_schema/err

  registry:
    type: File?
    outputSource: make_registry/model
  registry_log:
    type: File?
    outputSource: make_registry/log
  registry_err:
    type: File?
    outputSource: make_registry/errors

  data:
    type:
      type: array
      items:
        type: array
        items:
          type: array
          items: [File]
    outputSource: process/add_data_data
  download_log:
    type:
      type: array
      items:
        type: array
        items: [File]
    outputSource: process/download_log
  download_err:
    type:
      type: array
      items:
        type: array
        items: [File]
    outputSource: process/download_err

  process_log:
    type:
      type: array
      items:
        type: array
        items:
          type: array
          items: [File]
    outputSource: process/add_data_aggregate_log
  process_err:
    type:
      type: array
      items:
        type: array
        items:
          type: array
          items: [File]
    outputSource: process/add_data_aggregate_errors

  ingest_log:
    type:
      type: array
      items:
        type: array
        items:
          type: array
          items: [File]
    outputSource: process/add_data_ingest_log
  ingest_err:
    type:
      type: array
      items:
        type: array
        items:
          type: array
          items: [File]
    outputSource: process/add_data_ingest_errors

  reset_log:
    type:
      type: array
      items: [File]
    outputSource: init_tables/reset_log
  reset_err:
    type:
      type: array
      items: [File]
    outputSource: init_tables/reset_err

  index_log:
    type:
      type: array
      items: [File]
    outputSource: init_tables/index_log
  index_err:
    type:
      type: array
      items: [File]
    outputSource: init_tables/index_err

  vacuum_log:
    type:
      type: array
      items:
        type: array
        items: [File]
    outputSource: process/vacuum_log
  vacuum_err:
    type:
      type: array
      items:
        type: array
        items: [File]
    outputSource: process/vacuum_err

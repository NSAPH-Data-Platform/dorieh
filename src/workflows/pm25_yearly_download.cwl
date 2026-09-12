#!/usr/bin/env cwl-runner
### Pipeline to aggregate data in NetCDF format over given geographies
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
  over given geographies (zip codes or counties) and output as 
  CSV files. This is a wrapper around actual aggregation of
  one file allowing to scatter (parallelize) the aggregation
  over years.
  
  The output of the workflow are gzipped CSV files containing
  aggregated data. 
  
  Optionally, the aggregated data can be ingested into a database
  specified in the connection parameters:
  
  * `database.ini` file containing connection descriptions
  * `connection_name`  a string referring to a section in the `database.ini`
     file, identifying specific connection to be used.

  The workflow can be invoked either by providing command line options 
  as in the following example:
  
      toil-cwl-runner --retryCount 1 --cleanWorkDir never \ 
          --outdir /scratch/work/exposures/outputs \ 
          --workDir /scratch/work/exposures \
          pm25_yearly_download.cwl \  
          --database /opt/local/database.ini \ 
          --connection_name dorieh \ 
          --downloads s3://nsaph-public/data/exposures/wustl/ \ 
          --strategy default \ 
          --geography zcta \ 
          --shape_file_collection tiger \ 
          --table pm25_annual_components_mean

  Or, by providing a YaML file (see [example](../test_exposure_job)) 
  with similar options:
  
      toil-cwl-runner --retryCount 1 --cleanWorkDir never \ 
          --outdir /scratch/work/exposures/outputs \ 
          --workDir /scratch/work/exposures \
          pm25_yearly_download.cwl test_exposure_job.yml 
  

inputs:
  proxy:
    type: string?
    default: ""
    doc: HTTP/HTTPS Proxy if required
  downloads:
    type: Directory
    doc: |
      Local or AWS bucket folder containing netCDF grid files, downloaded 
      and unpacked from Washington University in St. Louis (WUSTL) Box
      site. Annual and monthly data repositories are described in
      [WUSTL Atmospheric Composition Analysis Group](https://sites.wustl.edu/acag/datasets/surface-pm2-5/).
      
      The annual data for PM2.5 is also available in 
      a Harvard URC AWS Bucket: `s3://nsaph-public/data/exposures/wustl/`
  geography:
    type: string
    doc: |
      Type of geography: zip codes or counties
      Supported values: "zip", "zcta" or "county"
  years:
    type: int[]
    default: [2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017]
  variable:
    type: string
    default:  PM25
    doc: |
      The main variable that is being aggregated over shapes. We have tested
      the pipeline for PM25
  component:
    type: string[]
    default: [BC, NH4, NIT, OM, SO4, SOIL, SS]
    doc: |
      Optional components provided as percentages in a separate set 
      of netCDF files
  strategy:
    type: string
    default: auto
    doc: |
      Rasterization strategy, see
      [documentation](https://foromeplatform.github.io/dorieh/strategy.html)
      for the list of supported values and explanations
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
  database:
    type: File
    doc: |
      Path to database connection file, usually database.ini. 
      This argument is ignored if `connection_name` == `None`
    default:
      path: database.ini
      class: File

  connection_name:
    type: string
    doc: |
      The name of the section in the database.ini file or a literal
      `None` to skip over database ingestion step
  table:
    type: string
    doc: The name of the table to store teh aggregated data in
    default: pm25_aggregated


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

  process:
    doc: Downloads raw data and aggregates it over shapes and time
    scatter:
      - year
    run: aggregate_one_file.cwl
    in:
      proxy: proxy
      downloads: downloads
      geography: geography
      shape_file_collection: shape_file_collection
      year: years
      variable: variable
      component: component
      strategy: strategy
      ram: ram
      table: table
      depends_on: initdb/log
    out:
      - shapes
      - aggregate_data
      - consolidated_data
      - aggregate_log
      - aggregate_err
      - data_dictionary

  extract_data_dictionary:
    run:
      class: ExpressionTool
      inputs:
        yaml_files:
          type: File[]
      outputs:
        data_dictionary:
          type: File
      expression: |
        ${
          return {data_dictionary: inputs.yaml_files[0]}
        }
    in:
      yaml_files: process/data_dictionary
    out:
      - data_dictionary

  ingest:
    run: ingest.cwl
    when: $(inputs.connection_name.toLowerCase() != 'none')
    doc: Uploads data into the database
    in:
      registry: extract_data_dictionary/data_dictionary
      domain:
        valueFrom: "exposures"
      table: table
      input: process/aggregate_data
      database: database
      connection_name: connection_name
    out: [log, errors]

  index:
    run: index.cwl
    when: $(inputs.connection_name.toLowerCase() != 'none')
    in:
      depends_on: ingest/log
      registry: extract_data_dictionary/data_dictionary
      domain:
        valueFrom: "exposures"
      table: table
      database: database
      connection_name: connection_name
    out: [log, errors]

  vacuum:
    run: vacuum.cwl
    when: $(inputs.connection_name.toLowerCase() != 'none')
    in:
      depends_on: index/log
      registry: extract_data_dictionary/data_dictionary
      domain:
        valueFrom: "exposures"
      table: table
      database: database
      connection_name: connection_name
    out: [log, errors]



outputs:
  aggregate_data:
    type: File[]
    outputSource: process/aggregate_data
  data_dictionary:
    type: File
    outputSource: extract_data_dictionary/data_dictionary
    doc: Data dictionary file, in YaML format, describing output variables
  consolidated_data:
    type: File[]
    outputSource: process/consolidated_data
  shapes:
    type:
      type: array
      items:
        type: array
        items: [File]
    outputSource: process/shapes

  aggregate_log:
    type:
      type: array
      items: Any

    outputSource: process/aggregate_log
  aggregate_err:
    type: File[]
    outputSource: process/aggregate_err

  ingest_log:
    type: File
    outputSource: ingest/log
  index_log:
    type: File
    outputSource: index/log
  vacuum_log:
    type: File
    outputSource: vacuum/log
  ingest_err:
    type: File
    outputSource: ingest/errors
  index_err:
    type: File
    outputSource: index/errors
  vacuum_err:
    type: File
    outputSource: vacuum/errors

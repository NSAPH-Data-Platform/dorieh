#!/usr/bin/env cwl-runner
### Workflow to aggregate and ingest one file in NetCDF format
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
  downloads:
    type: Directory
  geography:
    type: string
  year:
    type: int
  month:
    type: int
  band:
    type: string
    default: pm25
  table:
    type: string
  shape_files:
    type: File[]
    doc: "Paths to shape files"
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
  findfile:
    doc: |
      Given input directory, variable (band), year and month,
      evaluates the exepected file name for the input data
    run:
      class: ExpressionTool
      inputs:
        downloads:
          type: Directory
        year:
          type: int
        month:
          type: int
        band:
          type: string
      expression: |
        ${
          var v = inputs.band.toUpperCase();
          var y = String(inputs.year);
          var m;
          if (inputs.month < 10) {
            m = '0' + String(inputs.month);
          } else {
            m =  String(inputs.month);
          }
          var ym = y + m;
          var f = "V4NA03_" + v + "_NA_" + ym + "_" + ym + "-RH35.nc";
          f = inputs.downloads.location + '/' + f;
          return {
            netcdf_file: {
              "class": "File",
              "location": f
            }
          };
        }
      outputs:
        netcdf_file:
          type: File
    in:
      year: year
      month: month
      band: band
      downloads: downloads
    out: [netcdf_file]

  aggregate:
    doc: Aggregate data over geographies
    run: aggregate_wustl.cwl
    in:
      strategy: strategy
      ram: ram
      band:
        valueFrom: $([inputs.sband])
      sband: band
      geography: geography
      netcdf_data: findfile/netcdf_file
      shape_files: shape_files
    out:
      - log
      - errors
      - csv_data

  ingest:
    doc: Ingests the aggregated data into the database
    run: add_data.cwl
    in:
      table: table
      input: aggregate/csv_data
      database: database
      connection_name: connection_name
      domain:
        valueFrom: "exposures"
    out: [log, errors]

outputs:
  aggregate_data:
    type: File?
    outputSource: aggregate/csv_data
  aggregate_log:
    type: File?
    outputSource: aggregate/log
  aggregate_err:
    type: File
    outputSource: aggregate/errors

  ingest_log:
    type: File?
    outputSource: ingest/log
  ingest_err:
    type: File
    outputSource: ingest/errors






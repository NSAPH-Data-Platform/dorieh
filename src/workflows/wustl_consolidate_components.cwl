#!/usr/bin/env cwl-runner
###
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
class: CommandLineTool
baseCommand: [python, -mdorieh.rasters.netCDF_components_consolidator]

requirements:
  InlineJavascriptRequirement: {}
  ResourceRequirement:
    # coresMin: 1
    coresMax: 4
    outdirMin: 3072


doc: |
  Given a NetCDF file with absolute values (e.g., for PM25) and a set of 
  NetCDF files containing percentage values for individual components,  
  this tool consolidates all data into a single NetCDF file with both
  percentages and absolute values for all components.


hints:
  DockerRequirement:
    dockerPull: forome/dorieh

inputs:
  abs_values:
    type: File[]
    doc: "Path to downloaded file with absolute values"
    inputBinding:
      prefix: --input
  components:
    type: File[]
    doc: "Paths to component files"
    inputBinding:
      prefix: --components

arguments:
  - valueFrom: "."
    prefix: --output

outputs:
  log:
    type: File?
    outputBinding:
      glob: "*.log"
  consolidated_data:
    type: File
    outputBinding:
      glob:
        - "*.tif*"
        - "**/*.tif*"
    doc: |
      The output NetCDF file, containing absolute values for the given
      components
  errors:
    type: stderr

stderr: $("consolidate-" + inputs.abs_values.nameroot + ".err")

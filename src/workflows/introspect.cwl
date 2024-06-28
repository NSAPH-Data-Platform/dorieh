#!/usr/bin/env cwl-runner
### Introspector for downloaded data file
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
baseCommand: [python, -m, dorieh.epa.registry]

doc: |
  This tool examines a directory with downlaoded
  EPA data and generates a table defintion



hints:
  DockerRequirement:
    dockerPull: forome/dorieh

inputs:
  input:
    type: File
    inputBinding:
      prefix: --data
    doc: |
      A path the downloaded data file
  output:
    type: string
    doc: A path to a file name with EPA data model
    inputBinding:
      prefix: --output
  table:
    type: string
    doc: the name of the table to be created
    inputBinding:
      prefix: --table
  depends_on:
    type: File?
    doc: a special field used to enforce dependencies and execution order

outputs:
  log:
    type: File?
    outputBinding:
      glob: "*.log"
  model:
    type: File?
    outputBinding:
      glob: "*.yaml"
  errors:
    type: stderr

stderr: introspect.err


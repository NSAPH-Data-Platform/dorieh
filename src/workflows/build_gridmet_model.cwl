#!/usr/bin/env cwl-runner
### Model YAML Writer
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
baseCommand: [python, -m, dorieh.rasters.registry]

doc: |
  This tool writes the data model for gridMET data.



hints:
  DockerRequirement:
    dockerPull: forome/dorieh

inputs:
  output:
    type: string
    default: "gridmet.yaml"
    doc: A path to a file name with resulting data model
    inputBinding:
      position: 1
  domain:
    type: string?
    inputBinding:
      position: 2
  depends_on:
    type: File?
    doc: a special field used to enforce dependencies and execution order

outputs:
  log:
    type: File?
    outputBinding:
      glob: "registry*.log"
  model:
    type: File?
    outputBinding:
      glob: "*.yaml"
  errors:
    type: stderr

stderr: registry.err

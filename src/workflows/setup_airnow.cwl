#!/usr/bin/env cwl-runner
### Prepare environment for AirNow
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
baseCommand: [python, -m, dorieh.epa.airnow_setup]
requirements:
  InlineJavascriptRequirement: {}
  NetworkAccess:
    networkAccess: True

doc: |
  This tool prepares environemnt for AirNow download
  It checks that AirNow API key is provided and installs
  zip and county shape files if necessary


hints:
  DockerRequirement:
    dockerPull: forome/dorieh

inputs:
  api-key:
    type: string
    inputBinding:
      position: 1
  shape_dir:
    type: Directory?
    inputBinding:
      position: 2

outputs:
  shapes:
    type: File[]
    outputBinding:
      glob: "shapes/*.shp"
  log:
    type: stdout

stdout: setup.log

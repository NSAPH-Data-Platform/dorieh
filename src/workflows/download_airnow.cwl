#!/usr/bin/env cwl-runner
### Downloader of AirNow Data
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
baseCommand: [python, -m, dorieh.epa.airnow]
requirements:
  InlineJavascriptRequirement: {}
  NetworkAccess:
    networkAccess: True
  EnvVarRequirement:
    envDef:
      HTTPS_PROXY: $(inputs.proxy)
      HTTP_PROXY: $(inputs.proxy)

doc: |
  This tool downloads AirNow data from EPA website

# -p pm25 --dest airnow_pm25.json.gz --from 2020-12-25 --to 2020-12-31 --qc

hints:
  DockerRequirement:
    dockerPull: forome/dorieh

inputs:
  proxy:
    type: string?
    default: ""
    doc: HTTP/HTTPS Proxy if required
  parameter_code:
    type: string
    doc: |
      Parameter code. Either a numeric code (e.g. 88101, 44201)
      or symbolic name (e.g. PM25, NO2).
      See more: [AQS Code List](https://www.epa.gov/aqs/aqs-code-list)
    inputBinding:
      prefix: --parameters
  from:
    type: string
    doc: Start date for downolading, in YYYY-MM-DD format
    inputBinding:
      prefix: --from
  to:
    type: string
    doc: End date for downolading, in YYYY-MM-DD format
    inputBinding:
      prefix: --to
  shapes:
    type: File[]
    inputBinding:
      prefix: --shapes
    secondaryFiles:
      - "^.dbf"
      - "^.shx"
      - "^.prj"
      - "^.cpg"
  table:
    type: string
    doc: the name of the table to be created
  api-key:
    type: string?
    inputBinding:
      prefix: --api_key

arguments:
    - valueFrom: "--qc"
    - valueFrom: $(inputs.table + ".json.gz")
      prefix: --destination


outputs:
  log:
    type: File
    outputBinding:
      glob: "*.log"
  data:
    type: File
    outputBinding:
      glob: "*.json*"

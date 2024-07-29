#!/usr/bin/env cwl-runner
### Downloader of AQS Data
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
baseCommand: [wget]

requirements:
  InlineJavascriptRequirement: {}
  ResourceRequirement:
    coresMin: 0.5
  NetworkAccess:
    networkAccess: True
  EnvVarRequirement:
    envDef:
      HTTP_PROXY: "$('proxy' in inputs? inputs.proxy: null)"
      HTTPS_PROXY: "$('proxy' in inputs? inputs.proxy: null)"
      NO_PROXY: "localhost,127.0.0.1,172.17.0.1"

doc: |
  This tool downloads AQS data from EPA website

inputs:
  aggregation:
    type: string
    doc: "Aggregation type: annual or daily"
  parameter_code:
    type: string
    doc: |
      Parameter code. Either a numeric code (e.g. 88101, 44201)
      or symbolic name (e.g. PM25, NO2).
      See more: [AQS Code List](https://www.epa.gov/aqs/aqs-code-list)
  year:
    type: string
    doc: Year to download
  proxy:
    type: string
    doc: Proxy for connection

arguments:
  - position: 1
    valueFrom: $("https_proxy=" + inputs.proxy)
    prefix: -e
  - position: 2
    valueFrom: |
      ${
        if (inputs.aggregation == "annual") {
            return "https://aqs.epa.gov/aqsweb/airdata/annual_conc_by_monitor_" + inputs.year + ".zip";
        } else {
            var parameters = {"NO2": 42602, "OZONE": 44201, "PM25": 88101, "MIN_TEMP": 68103, "MAX_TEMP": 68104};
            var parameter = parameters[inputs.parameter_code] || inputs.parameter_code;

            return "https://aqs.epa.gov/aqsweb/airdata/daily_" + parameter + "_" + inputs.year + ".zip";
        }
      }

outputs:
  data:
    type: File
    outputBinding:
      glob: "*.*"

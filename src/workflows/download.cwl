#!/usr/bin/env cwl-runner
### Downloader of gridMET Data
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
  This tool downloads gridMET data from Atmospheric Composition Analysis Group



hints:
  DockerRequirement:
    dockerPull: forome/dorieh

inputs:
  proxy:
    type: string?
    default: ""
    doc: HTTP/HTTPS Proxy if required
  year:
    type: string
    doc: "Year to process"
  band:
    type: string
    doc: |
      [Gridmet Band](https://developers.google.com/earth-engine/datasets/catalog/IDAHO_EPSCOR_GRIDMET#bands)

arguments:
  - position: 1
    valueFrom: "-d"
  - position: 2
    valueFrom: $("-e https_proxy=" + inputs.proxy)
  - position: 3
    valueFrom: |
      ${
          var base = "https://www.northwestknowledge.net/metdata/data/";
          return base + inputs.band + "_" + inputs.year + ".nc";
      }

outputs:
  log:
    type: File?
    outputBinding:
      glob: "*.log"
  data:
    type: File?
    outputBinding:
      glob: "*.nc"
  errors:
    type: stderr

stderr:  $("wget-" + inputs.band + "-" + inputs.year + ".err")

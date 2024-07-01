#!/usr/bin/env cwl-runner
### Downloads Shape files from US Census website for a given year or the closest one
#  Copyright (c) 2021. Harvard University
#
#  Developed by Research Software Engineering,
#  Faculty of Arts and Sciences, Research Computing (FAS RC)
#  Author: Quantori LLC
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
baseCommand: [python, -m, dorieh.gis.shapes_downloader]

requirements:
  ResourceRequirement:
    coresMin: 1
  NetworkAccess:
    networkAccess: True
  EnvVarRequirement:
    envDef:
      HTTP_PROXY: "$('proxy' in inputs? inputs.proxy: null)"
      HTTPS_PROXY: "$('proxy' in inputs? inputs.proxy: null)"
      NO_PROXY: "localhost,127.0.0.1,172.17.0.1"


doc: |
  This tool downloads Shape files from a given collection (TIGER/Line or GENZ) 
  and a geography (ZCTA or Counties) from the US Census website,
  for a given year or for the closest one.


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
    doc: Calendar year, for which we are downloading shape file
    inputBinding:
      prefix: --year
  geo:
    type: string
    doc: geography type, zip, zcta or county
    inputBinding:
      prefix: --geography
  collection:
    type: string
    default: tiger
    doc: |
      [Collection of shapefiles](https://www2.census.gov/geo/tiger), 
      either GENZ or TIGER
    inputBinding:
      prefix: --collection

outputs:
  shape_files:
    type: File[]
    outputBinding:
      glob: "*.shp"
    secondaryFiles:
      - "^.dbf"
      - "^.shx"
      - "^.prj"
      - "^.cpg"

#!/usr/bin/env cwl-runner
### gridMET Pipeline
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
class: Workflow

requirements:
  SubworkflowFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  InlineJavascriptRequirement: {}
  ScatterFeatureRequirement: {}
  MultipleInputFeatureRequirement: {}

doc: |
  Downloads and processes gridMET data (no database ingestion)

inputs:
  proxy:
    type: string?
    default: ""
    doc: HTTP/HTTPS Proxy if required
  shapes:
    type: Directory
  geography:
    type: string
    doc: |
      Type of geography: zip codes or counties
  years:
    type: string[]
    default: ['1999:2008', '2011:2021']
  bands:
    type: string[]
    default: ['rmax', 'rmin', 'sph', 'srad', 'th', 'tmmn', 'tmmx']


steps:
  process:
    scatter: band
    in:
      proxy: proxy
      shapes: shapes
      geography: geography
      years: years
      band: bands

    run:
      class: Workflow
      inputs:
        proxy:
          type: string?
        shapes:
          type: Directory
        geography:
          type: string
        years:
          type: string[]
        band:
          type: string
      steps:
        download:
          run: download.cwl
          doc: Downloads and processes data
          scatter: year
          scatterMethod:  nested_crossproduct
          in:
            proxy: proxy
            shapes: shapes
            geography: geography
            year: years
            band: band
          out:
            - data
            - log
            - errors
      outputs:
        data:
          type: File[]
          outputSource: download/data
        download_log:
          type: File[]
          outputSource: download/log
        download_err:
          type: File[]
          outputSource: download/errors

    out:
      - data
      - download_log
      - download_err

outputs:
  data:
    type:
      type: array
      items:
        type: array
        items: [File]
    outputSource: process/data
  download_log:
    type:
      type: array
      items:
        type: array
        items: [File]
    outputSource: process/download_log
  download_err:
    type:
      type: array
      items:
        type: array
        items: [File]
    outputSource: process/download_err


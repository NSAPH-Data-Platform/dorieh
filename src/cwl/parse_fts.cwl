#!/usr/bin/env cwl-runner
### FTS Parser
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
baseCommand: [python, -m, cms.registry]

doc: |
  This tool examines a directory with raw CMS data, looking
  for File Transfer Summary (FTS) files. It examnines each
  FTS file under directory (recursively) and creates a unified
  data model for input raw CMS data. If any FTS files for
  different years are incompatible with one another, a
  warning is reported. However, so far we found that all years
  are compatible.


inputs:
  input:
    type: Directory
    inputBinding:
      prefix: --input
    doc: |
      A path to directory, containing unpacked CMS
      files. The tool will recursively look in subdirectories
      for FTS files
  output:
    type: string
    default: "cms.yaml"
    doc: A path to a file name with resulting data model
    inputBinding:
      prefix: --output

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

stderr: parse_fts.err

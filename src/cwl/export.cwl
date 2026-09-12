#!/usr/bin/env cwl-runner
### Export a table or a query result to a file system
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
baseCommand: [python, -m, dorieh.platform.util.pg_export]
requirements:
  InlineJavascriptRequirement: {}
  NetworkAccess:
    networkAccess: True

doc: |
  This tool builds all indices for the specified table.
  Log file displays real-time progress of building indices


inputs:
  table:
    type: string?
    doc: the name of the table
    inputBinding:
      prefix: --table
  sql:
    type: string?
    doc: SQL query
    inputBinding:
      prefix: --sql
  partition:
    type: string[]?
    doc: List of columns to be used for partitioning
    inputBinding:
      prefix: --partition
  output:
    type: string
    doc: the name of the newly created file or directory
    inputBinding:
      prefix: --output
  format:
    type: string
    doc: Format of the export, one of jsonl, parquet, csv, hdf5
    inputBinding:
      prefix: --format
  database:
    type: File
    doc: Path to database connection file, usually database.ini
    inputBinding:
      prefix: --db
  connection_name:
    type: string
    doc: The name of the section in the database.ini file
    inputBinding:
      prefix: --connection
  depends_on:
    type: Any?
    doc: a special field used to enforce dependencies and execution order



outputs:
  data:
    type:
      - File
      - Directory
    outputBinding:
      glob: $(inputs.output + "*")
  log:
    type: File
    outputBinding:
      glob: "*.log"
  errors:
    type: stderr

stderr:  $("export-" + inputs.table + ".err")


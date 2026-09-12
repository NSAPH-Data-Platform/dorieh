### Display Dorieh platform version
#  Copyright (c) 2022. Harvard University
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
baseCommand: [python, -m, dorieh.platform.loader.monitor]

requirements:
  InlineJavascriptRequirement: {}
  NetworkAccess:
    networkAccess: True

hints:
  DockerRequirement:
    dockerPull: forome/dorieh


doc: |
  This tool prints the DBMS activity statistics, 
  like currently running processes and some details about each process.

inputs:
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

outputs: {}

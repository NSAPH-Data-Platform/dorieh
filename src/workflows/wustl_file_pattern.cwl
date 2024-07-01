#!/usr/bin/env cwl-runner
### Expression evaluator to format a file name for pollution files downloaded from WashU
#  Copyright (c) 2021-2023. Harvard University
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
class: ExpressionTool

requirements:
  StepInputExpressionRequirement: {}
  InlineJavascriptRequirement: {}

doc: |
  Given input directory, variable (band), year and month,
  evaluates the expected file name for the input data

inputs:
  downloads:
    type: Directory
  year:
    type: int
  variables:
    type: string[]

expression: |
  ${
    var files = [];
    var i;
    for (i in inputs.variables) {
      var v = inputs.variables[i].toUpperCase();
      var y = String(inputs.year);
      var f;
      if (v == 'PM25') {
        f = "V4NA03_" + v + "_NA_" + y + "01_" + y + "12-RH35.nc";
      } else {
        if (y == '2017') {
          f = "GWRwSPEC.HEI_" + v + "p_NA_" + y + "01_" + y + "12-wrtSPECtotal.nc"
        } else {
          f = "GWRwSPEC_" + v + "p_NA_" + y + "01_" + y + "12-wrtSPECtotal.nc"
        };
      };
      f = inputs.downloads.location + '/' + f;
      files.push({
        "class": "File",
        "location": f
      });
    };
    return {
      netcdf_files: files
    }
  }

outputs:
  netcdf_files:
    type: File[]

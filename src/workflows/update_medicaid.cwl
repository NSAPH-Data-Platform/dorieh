#!/usr/bin/env cwl-runner
### Full Medicaid Processing Pipeline
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

doc: |
  This workflow prcoesses already ingested Medicaid data
  See [documentation](../Medicaid.md) for detailed
  information.

inputs:
  database:
    type: File
    doc: Path to database connection file, usually database.ini
  connection_name:
    type: string
    doc: The name of the section in the database.ini file
  registry:
    type: File

steps:
  index_ps:
    run: index.cwl
    in:
      registry:  registry
      domain:
        valueFrom: "cms"
      table:
        valueFrom: "ps"
      database: database
      connection_name: connection_name
      incremental:
        valueFrom: $(true)
    out: [log, errors]

  vacuum_ps:
    run: vacuum.cwl
    in:
      depends_on: index_ps/log
      registry:  registry
      domain:
        valueFrom: "cms"
      table:
        valueFrom: "ps"
      database: database
      connection_name: connection_name
    out: [log, errors]

  create_beneficiaries:
    run: matview.cwl
    doc: Creates `Beneficiaries` Table
    in:
      depends_on: vacuum_ps/log
      table:
        valueFrom: "beneficiaries"
      database: database
      connection_name: connection_name
      incremental:
        valueFrom: $(true)
    out:
      - create_log
      - index_log
      - vacuum_log
      - create_err
      - index_err
      - vacuum_err

  create_monthly_view:
    run: matview.cwl
    doc: Creates internally used `Monthly View`
    in:
      depends_on: create_beneficiaries/vacuum_log
      table:
        valueFrom: "monthly"
      database: database
      connection_name: connection_name
      incremental:
        valueFrom: $(true)
    out:
      - create_log
      - index_log
      - vacuum_log
      - create_err
      - index_err
      - vacuum_err

  create_enrollments:
    run: matview.cwl
    doc: Creates `Enrollment` Table
    in:
      depends_on: create_monthly_view/vacuum_log
      table:
        valueFrom: "enrollments"
      database: database
      connection_name: connection_name
      incremental:
        valueFrom: $(true)
    out:
      - create_log
      - index_log
      - vacuum_log
      - create_err
      - index_err
      - vacuum_err

  create_eligibility:
    run: matview.cwl
    doc: Creates `Eligibility` Table
    in:
      depends_on: create_enrollments/vacuum_log
      table:
        valueFrom: "eligibility"
      database: database
      connection_name: connection_name
      incremental:
        valueFrom: $(true)
    out:
      - create_log
      - index_log
      - vacuum_log
      - create_err
      - index_err
      - vacuum_err


outputs:
  ps_index_log:
    type: File
    outputSource: index_ps/log
  ps_vacuum_log:
    type: File
    outputSource: vacuum_ps/log
  ben_create_log:
    type: File
    outputSource: create_beneficiaries/create_log
  ben_index_log:
    type: File
    outputSource: create_beneficiaries/index_log
  ben_vacuum_log:
    type: File
    outputSource: create_beneficiaries/vacuum_log
  mnth_create_log:
    type: File
    outputSource: create_monthly_view/create_log
  mnth_index_log:
    type: File
    outputSource: create_monthly_view/index_log
  mnth_vacuum_log:
    type: File
    outputSource: create_monthly_view/vacuum_log
  enrlm_create_log:
    type: File
    outputSource: create_enrollments/create_log
  enrlm_index_log:
    type: File
    outputSource: create_enrollments/index_log
  enrlm_vacuum_log:
    type: File
    outputSource: create_enrollments/vacuum_log
  elgb_create_log:
    type: File
    outputSource: create_eligibility/create_log
  elgb_index_log:
    type: File
    outputSource: create_eligibility/index_log
  elgb_vacuum_log:
    type: File
    outputSource: create_eligibility/vacuum_log

  ps_index_err:
    type: File
    outputSource: index_ps/errors
  ps_vacuum_err:
    type: File
    outputSource: vacuum_ps/errors
  ben_create_err:
    type: File
    outputSource: create_beneficiaries/create_err
  ben_index_err:
    type: File
    outputSource: create_beneficiaries/index_err
  ben_vacuum_err:
    type: File
    outputSource: create_beneficiaries/vacuum_err
  mnth_create_err:
    type: File
    outputSource: create_monthly_view/create_err
  mnth_index_err:
    type: File
    outputSource: create_monthly_view/index_err
  mnth_vacuum_err:
    type: File
    outputSource: create_monthly_view/vacuum_err
  enrlm_create_err:
    type: File
    outputSource: create_enrollments/create_err
  enrlm_index_err:
    type: File
    outputSource: create_enrollments/index_err
  enrlm_vacuum_err:
    type: File
    outputSource: create_enrollments/vacuum_err
  elgb_create_err:
    type: File
    outputSource: create_eligibility/create_err
  elgb_index_err:
    type: File
    outputSource: create_eligibility/index_err
  elgb_vacuum_err:
    type: File
    outputSource: create_eligibility/vacuum_err

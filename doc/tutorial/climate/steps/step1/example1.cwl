#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: Workflow

requirements:
  SubworkflowFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  InlineJavascriptRequirement: {}
  ScatterFeatureRequirement: {}
  MultipleInputFeatureRequirement: {}
  NetworkAccess:
    networkAccess: True

inputs: {}

steps:
  download:
    run: https://raw.githubusercontent.com/ForomePlatform/dorieh/main/src/cwl/download.cwl

  aggregate:
    run: https://raw.githubusercontent.com/ForomePlatform/dorieh/main/src/cwl/aggregate_daily.cwl

outputs: {}

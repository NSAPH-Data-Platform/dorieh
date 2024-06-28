#!/usr/bin/env cwl-runner
### Test harness for gridmet.cwl

cwlVersion: v1.2
class: Workflow

requirements:
  InlineJavascriptRequirement: {}
  MultipleInputFeatureRequirement: {}
  ScatterFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  SubworkflowFeatureRequirement: {}


# All inputs of original pipeline, remove what is not needed
inputs:
  bands:
    doc: "University of Idaho Gridded Surface Meteorological Dataset \n[bands](https://developers.google.com/earth-engine/datasets/catalog/IDAHO_EPSCOR_GRIDMET#bands)\n"
    type: string[]
  connection_name:
    doc: The name of the section in the database.ini file
    type: string
  database:
    doc: Path to database connection file, usually database.ini
    type: File
  dates:
    doc: dates restriction, for testing purposes only
    type: string?
  domain:
    default: climate
    type: string
  geography:
    doc: 'Type of geography: zip codes or counties

      Valid values: "zip", "zcta" or "county"

      '
    type: string
  proxy:
    default: ''
    doc: HTTP/HTTPS Proxy if required
    type: string?
  ram:
    default: 2GB
    doc: Runtime memory, available to the process
    type: string
  shapes:
    doc: Do we even need this parameter, as we instead downloading shapes?
    type: Directory?
  strategy:
    default: auto
    doc: Rasterization strategy
    type: string
  test_script:
    doc: File containing SQL test script
    type: File[]
  years:
    default:
    - '1999'
    - '2000'
    - '2001'
    - '2002'
    - '2003'
    - '2004'
    - '2005'
    - '2006'
    - '2007'
    - '2008'
    - '2009'
    - '2010'
    - '2011'
    - '2012'
    - '2013'
    - '2014'
    - '2015'
    - '2016'
    - '2017'
    - '2018'
    - '2019'
    - '2020'
    type: string[]


steps:
  execute:
    run: gridmet.cwl
    in:
      proxy: proxy
      shapes: shapes
      geography: geography
      years: years
      bands: bands
      strategy: strategy
      ram: ram
      database: database
      connection_name: connection_name
      dates: dates
      domain: domain
    out:
      - registry
      - registry_log
      - registry_err
      - data
      - download_log
      - download_err
      - process_log
      - process_err
      - ingest_log
      - ingest_err
      - reset_log
      - reset_err
      - index_log
      - index_err
      - vacuum_log
      - vacuum_err

  verify:
    run: run_test.cwl
    in:
      database: database
      connection_name: connection_name
      script: test_script
      depends_on: execute/vacuum_err
    out:
      - log
      - errors

outputs:
## Generated by nsaph/util/cwl_collect_outputs.py from gridmet.cwl:
  execute_registry:
    type: File?
    outputSource: execute/registry
  execute_registry_log:
    type: File?
    outputSource: execute/registry_log
  execute_registry_err:
    type: File?
    outputSource: execute/registry_err
  execute_data:
    type: {'type': 'array', 'items': {'type': 'array', 'items': {'type': 'array', 'items': ['File']}}}
    outputSource: execute/data
  execute_download_log:
    type: {'type': 'array', 'items': {'type': 'array', 'items': ['File']}}
    outputSource: execute/download_log
  execute_download_err:
    type: {'type': 'array', 'items': {'type': 'array', 'items': ['File']}}
    outputSource: execute/download_err
  execute_process_log:
    type: {'type': 'array', 'items': {'type': 'array', 'items': {'type': 'array', 'items': ['File']}}}
    outputSource: execute/process_log
  execute_process_err:
    type: {'type': 'array', 'items': {'type': 'array', 'items': {'type': 'array', 'items': ['File']}}}
    outputSource: execute/process_err
  execute_ingest_log:
    type: {'type': 'array', 'items': {'type': 'array', 'items': {'type': 'array', 'items': ['File']}}}
    outputSource: execute/ingest_log
  execute_ingest_err:
    type: {'type': 'array', 'items': {'type': 'array', 'items': {'type': 'array', 'items': ['File']}}}
    outputSource: execute/ingest_err
  execute_reset_log:
    type: {'type': 'array', 'items': ['File']}
    outputSource: execute/reset_log
  execute_reset_err:
    type: {'type': 'array', 'items': ['File']}
    outputSource: execute/reset_err
  execute_index_log:
    type: {'type': 'array', 'items': ['File']}
    outputSource: execute/index_log
  execute_index_err:
    type: {'type': 'array', 'items': ['File']}
    outputSource: execute/index_err
  execute_vacuum_log:
    type: {'type': 'array', 'items': {'type': 'array', 'items': ['File']}}
    outputSource: execute/vacuum_log
  execute_vacuum_err:
    type: {'type': 'array', 'items': {'type': 'array', 'items': ['File']}}
    outputSource: execute/vacuum_err
## Generated by nsaph/util/cwl_collect_outputs.py from run_test.cwl:
  verify_log:
    type: File
    outputSource: verify/log
  verify_errors:
    type: File
    outputSource: verify/errors

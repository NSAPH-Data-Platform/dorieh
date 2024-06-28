#!/usr/bin/env cwl-runner

cwlVersion: v1.1
class: Workflow

requirements:
  SubworkflowFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  InlineJavascriptRequirement: {}
  ScatterFeatureRequirement: {}
  
inputs:
  database:
    type: File
    doc: Path to database connection file, usually database.ini
  connection_name:
    type: string
    doc: The name of the section in the database.ini file
  registry: File
  data_files: File[]

steps:
  store:
    run:
      class: Workflow
      inputs:
        db:
          type: File
        connection: 
          type: string
        schema:
          type: File
        data:
          type: File
        table:
          type: string
      outputs:
        ingest_log:
          type: File
          outputSource: ingest/log
        index_log:
          type: File
          outputSource: index/log
        vacuum_log:
          type: File
          outputSource: vacuum/log
        ingest_err:
          type: File
          outputSource: ingest/errors
        index_err:
          type: File
          outputSource: index/errors
        vacuum_err:
          type: File
          outputSource: vacuum/errors
      steps:
        ingest:
          run: ingest.cwl
          doc: Uploads data into the database
          in:
            registry: schema
            domain:
              valueFrom: "census"
            table: table
            input: data
            database: db
            connection_name: connection
          out: [log, errors]
        index:
          run: index.cwl
          in:
            depends_on: ingest/log
            registry: schema
            domain:
              valueFrom: "census"
            table: table
            database: db
            connection_name: connection
          out: [log, errors]
        vacuum:
          run: vacuum.cwl
          in:
            depends_on: index/log
            domain:
              valueFrom: "census"
            registry: schema
            table: table
            database: db
            connection_name: connection
          out: [log, errors]
    scatter: data
    in:
      data: data_files
      db: database
      connection: connection_name
      schema: registry
      table:
        valueFrom: $(inputs.data.nameroot)
    out:
      - ingest_log
      - index_log
      - vacuum_log
      - ingest_err
      - index_err
      - vacuum_err

outputs:
  ingest_log:
    type: File[]
    outputSource: store/ingest_log
  index_log:
    type: File[]
    outputSource: store/index_log
  vacuum_log:
    type: File[]
    outputSource: store/vacuum_log
  ingest_errors:
    type: File[]
    outputSource: store/ingest_err
  index_errors:
    type: File[]
    outputSource: store/index_err
  vacuum_errors:
    type: File[]
    outputSource: store/vacuum_err


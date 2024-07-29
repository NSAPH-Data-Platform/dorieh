#!/usr/bin/env cwl-runner

cwlVersion: v1.1
class: Workflow

requirements:
  SubworkflowFeatureRequirement: {}
  StepInputExpressionRequirement: {}



hints:
  DockerRequirement:
    dockerPull: forome/dorieh

inputs:
  api_key: string # API Key for the Census API
  http_proxy:
    type: string
    default: ""
  var_file:  # YML File specifying the census variables
    type: File
  geometry: string # Census geometry to use
  years: string # Years to download census for, written <min_year>:<max_year>
  interpolate_years: string  # Years to interpolate census over, written <min_year>:<max_year>
  log: string # name of the main log file
  state: string? # state fips code, if you want to download only a single state
  county: string? # county fips code, if you want to download only a single county, requires state
  density_vars: string[] # List of variables to calculate area density for
  assemble_pkl: string # pkl file to store results of initial download
  interpolate_pkl: string # pkl file to store object with interpolated data
  density_interp_pkl: string # pkl file to store object with interpolated data and calculated densities
  density_no_interp_pkl: string # pkl file to store object with uninterpolated data and calculated densities
  interp_out: string # csv file to store output with interpolated data
  interp_tablename: string # table name for interpolated data
  interp_schema: string # File name for interpolated data schema (.yml)
  no_interp_out: string #csv file to store uninterpolated data in
  no_interp_tablename: string # table name for uninterpolated data
  no_interp_schema: string # File name for uninterpolated data schema (.yml)
  qc_file: File # YAML File specifying QC
  interp_qc_log: string # Place to log QC for interpolated data
  no_interp_qc_log: string # Place to log QC for uninterpolated data
  database:
    type: File
    doc: Path to database connection file, usually database.ini
  connection_name:
    type: string
    doc: The name of the section in the database.ini file
  table:
    type: string

outputs:
  assemble_pkl:
    type: File
    outputSource: assemble/pkl
  log:
    type: File
    outputSource: make_log/log
  interp_pkl:
    type: File
    outputSource: interpolate/pkl
  density_no_interp_pkl:
    type: File
    outputSource: no_interp_density/pkl
  density_interp_pkl:
    type: File
    outputSource: interp_density/pkl
  interp_qc_log:
    type: File
    outputSource: interp_qc/qc_log
  no_interp_qc_log:
    type: File
    outputSource: no_interp_qc/qc_log
  interp_data:
    type: File[]
    outputSource: write_interp/data
  interp_schema:
    type: File
    outputSource: write_interp/schema
  no_interp_data:
    type: File[]
    outputSource: write_no_interp/data
  no_interp_schema:
    type: File
    outputSource: write_no_interp/schema
  ingest_log:
    type: File
    outputSource: ingest/log
  index_log:
    type: File
    outputSource: index/log
  vacuum_log:
    type: File
    outputSource: vacuum/log
  ingest_errors:
    type: File
    outputSource: ingest/errors
  index_errors:
    type: File
    outputSource: index/errors
  vacuum_errors:
    type: File
    outputSource: vacuum/errors

steps:
  make_log:
    run:
      class: CommandLineTool
      baseCommand: touch
      inputs:
        log:
          type: string
          inputBinding:
            position: 1
      outputs:
        log:
          type: File
          outputBinding:
            glob: $(inputs.log)
    in:
      log: log
    out: [log]

  assemble: # Download and calculate census variables
    run: census_assemble.cwl
    in:
      api_key: api_key
      http_proxy: http_proxy
      var_file: var_file
      geometry: geometry
      years: years
      log: make_log/log
      pkl_file: assemble_pkl
      state: state
      county: county
    out: [pkl]
  interpolate: # Interpolate data for missing years
    run: census_interpolate.cwl
    in:
      interpolate: interpolate_years
      log:
        source: make_log/log
      in_pkl:
        source: assemble/pkl
      out_pkl: interpolate_pkl
    out: [pkl]
  no_interp_density: # Calculate densities for uninterpolated data
    run: census_density.cwl
    in:
      http_proxy: http_proxy
      densities: density_vars
      log: make_log/log
      in_pkl: assemble/pkl
      out_pkl: density_no_interp_pkl
    out: [pkl]
  interp_density:  # Calculate densities for interpolated data
    run: census_density.cwl
    in:
      http_proxy: http_proxy
      densities: density_vars
      log: make_log/log
      in_pkl: interpolate/pkl
      out_pkl: density_interp_pkl
    out: [pkl]
  no_interp_qc:
    run: census_qc.cwl
    in:
      log: make_log/log
      in_pkl: no_interp_density/pkl
      qc_file: qc_file
      qc_log: no_interp_qc_log
    out: [qc_log]
  interp_qc:
    run: census_qc.cwl
    in:
      log: make_log/log
      in_pkl: interp_density/pkl
      qc_file: qc_file
      qc_log: interp_qc_log
    out: [qc_log]
  write_interp:
    run: census_write.cwl
    in:
      log: make_log/log
      in_pkl: interp_density/pkl
      out_file: interp_out
      schema_name: interp_schema
      table_name: interp_tablename
    out: [data, schema]
  write_no_interp:
    run: census_write.cwl
    in:
      log: make_log/log
      in_pkl: no_interp_density/pkl
      out_file: no_interp_out
      schema_name: no_interp_schema
      table_name: no_interp_tablename
    out: [data, schema]
  ingest:
    run: ingest.cwl
    doc: Uploads data into the database
    in:
      registry: write_interp/schema
      table: table
      input: write_interp/data
      database: database
      connection_name: connection_name
      domain:
        valueFrom: "census"
    out: [log, errors]
  index:
    run: index.cwl
    in:
      depends_on: ingest/log
      registry: write_interp/schema
      domain:
        valueFrom: "census"
      table: table
      database: database
      connection_name: connection_name
    out: [log, errors]
  vacuum:
    run: vacuum.cwl
    in:
      depends_on: index/log
      domain:
        valueFrom: "census"
      registry: write_interp/schema
      table: table
      database: database
      connection_name: connection_name
    out: [log, errors]

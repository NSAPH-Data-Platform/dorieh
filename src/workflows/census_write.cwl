#! cwl-runner

cwlVersion: v1.1
class: CommandLineTool
baseCommand: [python, -m, census.write_data]


hints:
  DockerRequirement:
    dockerPull: forome/dorieh

inputs:
  log:
    type: File
    default:
      class: File
      location: census.log
    inputBinding:
      prefix: --log
  in_pkl:
    type: File
    default:
      class: File
      location: census.pkl
    inputBinding:
      prefix: --in_pkl
  out_file:
    type: string
    default: "census.csv"
    inputBinding:
      prefix: --out_file
  schema_name:
    type: string
    default: "census_schema.yml"
    inputBinding:
      prefix: --schema_name
  table_name:
    type: string?
    inputBinding:
      prefix: --table_name

outputs:
  data:
    type: File[]
    outputBinding:
      glob: $(inputs.out_file)
  schema:
    type: File
    outputBinding:
      glob: $(inputs.schema_name)

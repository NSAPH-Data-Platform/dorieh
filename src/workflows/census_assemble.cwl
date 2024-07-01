#! cwl-runner

cwlVersion: v1.2
class: CommandLineTool
baseCommand: [python, -m, census.cli]
requirements:
  EnvVarRequirement:
    envDef:
      GET_CENSUS_API_KEY: $(inputs.api_key)
      HTTPS_PROXY: $(inputs.http_proxy)
      HTTP_PROXY: $(inputs.http_proxy)
  NetworkAccess:
    networkAccess: true


hints:
  DockerRequirement:
    dockerPull: forome/dorieh

inputs:
  http_proxy:
    type: string
    default: ""
  api_key:
    type: string
  var_file:
    type: File
    inputBinding:
      prefix: --var_file
  geometry:
    type: string
    inputBinding:
      prefix: --geometry
  years:
    type: string
    default: "1999:2019"
    inputBinding:
      prefix: --years
  log:
    type: File
    default:
      class: File
      location: census.log
    inputBinding:
      prefix: --log
  pkl_file:
    type: string
    default: "census.pkl"
    inputBinding:
      prefix: --pkl_file
  state:
    type: string?
    inputBinding:
      prefix: --state
  county:
    type: string?
    inputBinding:
      prefix: --county

arguments:
  - prefix: --out
    valueFrom: "out.csv"

outputs:
  pkl:
    type: File
    outputBinding:
      glob: $(inputs.pkl_file)

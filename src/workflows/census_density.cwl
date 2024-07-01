#! cwl-runner

cwlVersion: v1.1
class: CommandLineTool
baseCommand: [python, -m, census.calculate_density]
requirements:
  EnvVarRequirement:
    envDef:
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
  densities:
    type: string[]
    default: ["population"]
    inputBinding:
      prefix: -d
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
  out_pkl:
    type: string
    default: "census_densities.pkl"
    inputBinding:
      prefix: --out_pkl

outputs:
  pkl:
    type: File
    outputBinding:
      glob: $(inputs.out_pkl)

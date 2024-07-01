#! cwl-runner

cwlVersion: v1.1
class: CommandLineTool
baseCommand: [python, -m, census.interpolate_data]


hints:
  DockerRequirement:
    dockerPull: forome/dorieh

inputs:
  interpolate:
    type: string
    default: "1999:2019"
    inputBinding:
      prefix: -i
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
    default: "census_interpolated.pkl"
    inputBinding:
      prefix: --out_pkl

outputs:
  pkl:
    type: File
    outputBinding:
      glob: $(inputs.out_pkl)

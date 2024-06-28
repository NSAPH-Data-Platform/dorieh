cwlVersion: v1.1
class: CommandLineTool
baseCommand: [python, -m, census.do_qc]


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
  qc_file:
    type: File
    default:
      class: File
      location: census_qc.yml
    inputBinding:
      prefix: --qc_file
  qc_log:
    type: string
    default: census_qc.log
    inputBinding:
      prefix: --qc_log

outputs:
  qc_log:
    type: File
    outputBinding:
      glob: $(inputs.qc_log)

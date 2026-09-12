#  Copyright (c) 2024. Harvard University
#
#  Developed by Research Software Engineering,
#  Harvard University Research Computing and Data (RCD) Services.
#
#  Author: Michael A Bouzinier
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#           http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

"""
Script to add the following block to all CWL Tools:
    hints:
      DockerRequirement:
        dockerPull: forome/dorieh
"""
import glob
import os.path
import shutil
from pathlib import Path


def main(rtype = "hints"):
    pp = list(Path(__file__).parents)
    root = pp[3]
    pattern = os.path.join(root, "cwl", "*.cwl")
    scripts = glob.glob(pattern, recursive=False)
    outdir = os.path.join(root, "workflows")
    if not os.path.isdir(outdir):
        os.mkdir(outdir)
    for script in scripts:
        tool = script.startswith("test_")
        with open(script, "rt") as f:
            lines = [l for l in f]
            for line in lines:
                if "class: CommandLineTool" in line:
                    tool = True
                    break
            if not tool:
                shutil.copy(script, outdir)
                continue
            idx = -1
            for i in range(len(lines)):
                line = lines[i]
                if line.startswith(rtype):
                    idx = i + 1
                    break
            if idx < 0:
                for i in range(len(lines)):
                    line = lines[i]
                    if line.startswith("inputs:"):
                        lines.insert(i, "\n")
                        lines.insert(i+1, rtype + ":\n")
                        idx = i + 2
                        break
            if idx < 0:
                raise ValueError("Failed to find insertion point")
            lines.insert(idx, "  DockerRequirement:\n")
            lines.insert(idx+1, "    dockerPull: forome/dorieh\n")
            lines.insert(idx+2, "\n")
        with open(os.path.join(outdir, os.path.basename(script)), "wt") as o:
            o.writelines(lines)
    return


if __name__ == '__main__':
    main()

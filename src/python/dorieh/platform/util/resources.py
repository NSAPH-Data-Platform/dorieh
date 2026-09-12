#  Copyright (c) 2021. Harvard University
#
#  Developed by Research Software Engineering,
#  Faculty of Arts and Sciences, Research Computing (FAS RC)
#  Author: Michael A Bouzinier
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import glob
import os
import sys
from pathlib import Path
from typing import Dict

from dorieh.version import PACKAGE_NAME


def get_resource_dir() -> str:
    pp = list(Path(__file__).parents)
    idx = -1
    for i in range(len(pp)):
        d = pp[i].name
        if d == PACKAGE_NAME:
            idx = i
            break
    if idx < 0:
        idx = 3
    if pp[idx+1].name == "python" and pp[idx+2].name == "src":
        idx += 3
    root = pp[idx]
    return os.path.join(root, "resources")


def name2path(name: str) -> str:
    return os.path.join(*(name.split('.')))


def get_resources(name: str, verbose=False) -> Dict[str, str]:
    rel_path = name2path(name)
    dirs = [get_resource_dir()] + [
        os.path.join(d, "dorieh", "resources")
        for d in sys.path
    ]
    for d in dirs:
        rpath = os.path.join(d, rel_path + "*")
        if verbose:
            print(rpath)
        resources = glob.glob(rpath, recursive=False)
        if resources:
            return {
                '.'.join(os.path.basename(r).split('.')[1:]): r
                for r in resources
            }
    return {}


if __name__ == '__main__':
    print(get_resources("public.us_iso"))

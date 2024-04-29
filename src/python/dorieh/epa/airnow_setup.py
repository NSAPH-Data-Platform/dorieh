"""
Prepares workspace for AirNow pipeline

In particular, installs zip code and county shape files
"""

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

from typing import List
import sys
import os
import yaml

from dorieh.platform.util.shapes import install


def setup(args: List[str]):
    f = ".airnow.yaml"
    api_key = "api key"
    shapes = "shapes"
    if os.path.isfile(f):
        cfg = yaml.safe_load(f)
    else:
        cfg = dict()
    if api_key not in cfg:
        if len(args) < 1:
            raise ValueError("No AirNow API Key is provided")
    if len(sys.argv) > 0:
        cfg[api_key] = args[0]
    if shapes in cfg:
        for shape in cfg[shapes]:
            if not os.path.isfile(shape):
                raise ValueError("Shape file {} does not exist.".format(shape))
    else:
        dest = "shapes"
        shps = install(dest)
        cfg[shapes] = shps
        # [os.path.abspath(shape) for shape in shps]
    with open(f, "wt") as out:
        yaml.safe_dump(cfg, out)
    print("All Done")


if __name__ == '__main__':
    setup(sys.argv[1:])

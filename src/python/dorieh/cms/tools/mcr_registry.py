#  Copyright (c) 2022. Harvard University
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

"""
Common content for the Medicare data model YAML file
"""

import os
import yaml


class MedicareRegistry:
    def __init__(self, registry_path: str):
        self.registry_path = registry_path
        self.registry = None
        self.domain = "cms"
        if not os.path.isfile(self.registry_path):
            self.init_registry()
        else:
            self.read_registry()
        return

    def init_registry(self):
        self.registry = {
            self.domain: {
                "reference": "",
                "schema": self.domain,
                "index": "explicit",
                "quoting": 3,
                "header": False,
                "tables": {
                }
            }
        }
        return

    def read_registry(self):
        with open(self.registry_path) as f:
            self.registry = yaml.safe_load(f)
        return

    def save(self):
        with open(self.registry_path, "wt") as f:
            yaml.dump(self.registry, f)
        return


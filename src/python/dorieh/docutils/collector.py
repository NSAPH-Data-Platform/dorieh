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

m_template = """:orphan:

..
    autogenerated
    
The {name} Module
============================================================================

.. automodule:: {module}
   :members:
   :undoc-members:

"""


class ModuleCollector:
    def __init__(self, destination: str = "doc/members", pattern="**/*.py", template=m_template):
        self.dest = destination
        self.pattern = pattern
        self.template = template

    def collect(self, source_path: str):
        if not os.path.isdir(self.dest):
            os.makedirs(self.dest, exist_ok=True)
        modules = glob.glob(os.path.join(source_path, self.pattern), recursive=True)
        for module in modules:
            name = os.path.basename(module)
            name, _ = os.path.splitext(name)
            if name.startswith("_"):
                continue
            target = name + ".md"
            target = os.path.join(self.dest, target)
            if os.path.exists(target):
                continue
            target = name + ".rst"
            target = os.path.join(self.dest, target)
            if os.path.exists(target):
                with open(target) as f:
                    lines = [line for line in f][:2]
                    if lines[0].strip() != '..' or lines[1].strip() != "autogenerated":
                        continue
            x, _ = os.path.splitext(os.path.relpath(module, source_path))
            x = x.replace('/', '.')
            content = self.template.format(name=name, module=x)
            with open(target, "wt") as f:
                f.write(content)
        return


def main():
    if len(sys.argv) > 2:
        collector = ModuleCollector(sys.argv[2])
    else:
        collector = ModuleCollector()
    collector.collect(sys.argv[1])


if __name__ == '__main__':
    main()

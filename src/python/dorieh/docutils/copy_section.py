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

import os
import sys
from typing import List


def get_header_level(line: str) -> int:
    for i in range(len(line)):
        if line[i] != '#':
            return i
    return -1


def read_section(source: str, section: str) -> List[str]:
    content: List[str] = []
    inside = False
    level = None
    with open(source, "rt") as f:
        for line in f:
            if not line.startswith('#'):
                if inside:
                    content.append(line)
                continue
            lh = get_header_level(line)
            if not inside:
                header = line[lh:].strip()
                if header.lower() != section.lower():
                    continue
                level = lh
                inside = True
                continue
            if lh <= level:
                break

    return content


def insert_section(source: str, to: str, project: str = None):
    if project is None:
        project = os.path.basename(os.path.dirname(source))
    with open(to, "rt") as f:
        content = [line for line in f]
    start = None
    end = None
    section = None
    end_of_section = None
    for l1, line in enumerate(content):
        if not line.startswith("<!--"):
            continue
        statement = line[4:].strip().lower()
        if start is None:
            if statement.startswith("section"):
                tokens = statement.split()
                if len(tokens) < 3:
                    continue
                try:
                    n = tokens.index("from")
                except ValueError:
                    n = len(tokens)
                if project.lower() != tokens[n + 1].lower():
                    continue
                section = ' '.join(tokens[1:n])
                start = l1
                end_of_section = "<!-- end of section {} from {} -->\n".format(section, project)
                continue
        if line == end_of_section:
            end = l1 + 1
            break
    if start is None:
        raise ValueError(f"Not found: copy {project} from {source} to {to}")
    section_content = read_section(source, section)
    with open(to, "wt") as f:
        for line in content[: start + 1]:
            f.write(line)
        f.write("\n")
        for line in section_content:
            f.write(line)
        f.write(end_of_section)
        if end is None:
            end = start + 2
        for line in content[end:]:
            f.write(line)
    return


def main():
    if len(sys.argv) > 3:
        prj = sys.argv[3]
    else:
        prj = None
    insert_section(sys.argv[1], sys.argv[2], prj)


if __name__ == '__main__':
    main()

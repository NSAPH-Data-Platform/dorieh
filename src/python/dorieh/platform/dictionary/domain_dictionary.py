#  Copyright (c) 2024.  Harvard University
#
#   Developed by Research Software Engineering,
#   Harvard University Research Computing and Data (RCD) Services.
#
#   Author: Michael A Bouzinier
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#
import argparse
import math
import os
import sys
from enum import Enum
from typing import Dict, List

from dorieh.platform.dictionary import RenderMode
from dorieh.platform.dictionary.element import HTML, qstr, attrs2string, create_graph_envelop, PANDOC
from dorieh.platform.dictionary.tables import Table, Relation
from dorieh.utils.io_utils import as_dict
from dorieh.platform.data_model.domain import Domain


class DomainDict:
    def __init__(self, of: str, options: Dict):
        self.tables: Dict[str, Table] = dict()
        self.relations: List[Relation] = []
        self.of = of
        self.basedir = os.path.dirname(os.path.abspath(of))
        self.options = options
        self.link = True # self.options.get("fmt") in ["svg"]
        self.mode = RenderMode(options["mode"])

    def add(self, path):
        yml = as_dict(path)
        for d in yml:
            print("Processing: " + d)
            domain = Domain(name=d, spec=path)
            domain.init()
            schema = domain.schema
            for t in yml[d]["tables"]:
                Table(schema, t, domain, self)

    def list(self):
        print("Tables")
        for t in self.tables:
            print("\t" + str(self.tables[t]))
        print("Relations")
        for r in self.relations:
            print("\t" + str(r))

    def is_top(self, t: str):
        return not self.tables[t].get_predecessors()

    def print_node(self, out, t: str, indent: int):
        table = self.tables[t]
        node_id = qstr(table)
        attrs = dict()
        if self.link:
            f = os.path.join(self.basedir, "tables", t + ".md")
            table.markdown(f)
            attrs["URL"] = qstr(os.path.join("tables", t + ".html"))
            attrs["target"] = "_blank"
        space = ''.join('\t' for _ in range(indent))
        print(f"{space}{node_id} [{attrs2string(attrs)}];", file=out)

    def print_top_nodes(self, out):
        print("// Tables with raw (original) data", file=out)
        print(file=out)
        tables = [t for t in self.tables if self.is_top(t)]
        nn = len(tables)
        n = max(round(math.sqrt(nn)), 3)
        i = 0
        m = None
        while i < nn:
            print("\t{ rank = same; ", file=out)
            nodes = []
            for j in range(i, i + n):
                if j >= nn:
                    break
                t = tables[j]
                nodes.append(qstr(self.tables[t]))
                self.print_node(out, t, 2)
            print("\t}", file=out)
            if m:
                s = " ".join(nodes)
                print(f"\t{m} -> {{ {s} }} [ style = invis ];", file=out)
            idx = min((int(i + n / 2)), nn - 1)
            m = qstr(self.tables[tables[idx]])
            i += n
        print(file=out)

    def print_other_nodes(self, out):
        print("// Tables with derived (processed) data", file=out)
        for t in self.tables:
            if not self.is_top(t):
                self.print_node(out, t, 1)
        print(file=out)

    def to_dot(self, out = sys.stdout):
        print("digraph {", file=out)
        print("\tnodesep = 0.5;  // even node distribution", file=out)
        print('\tsize = "25,100";  // graph size in inches', file=out)
        self.print_top_nodes(out)
        self.print_other_nodes(out)
        for r in self.relations:
            node1 = qstr(r.x)
            node2 = qstr(r.y)
            attrs = r.as_edge_attr()
            alist = [f'{key}={attrs[key]}' for key in attrs]
            astring = ','.join(alist)
            print(f"\t{node1} -> {node2} [{astring}];", file=out)
        print("}", file=out)

    def html(self, of: str, svg = None):
        if svg is None:
            return
        block = HTML.format(
            title = f"Table Lineage Diagram",
            body = self.html_body(svg)
        )
        with open(of, "wt") as out:
            print(block, file=out)

    @staticmethod
    def html_body(svg):
        body = f'<object data="{svg}" type="image/svg+xml"></object>'
        return body

    def write_markdown(self, content: str, of: str):
        with open(of, "wt") as out:
            print(content, file=out)
        if self.mode == RenderMode.standalone:
            fhtml = os.path.splitext(of)[0] + ".html"
            os.system(f"{PANDOC} --from markdown  --to html {of} > {fhtml}")

    def link_ext(self):
        if self.mode == RenderMode.standalone:
            return "html"
        return "md"

    def markdown(self, of: str, svg=None):
        title = "# Table Lineage Diagram\n"
        body = "\n"

        if svg:
            if self.mode == RenderMode.standalone:
                body += self.html_body(svg)
            elif self.mode == RenderMode.sphinx:
                target = create_graph_envelop(of, "Table Lineage SVG Diagram", svg)
                body += self.table_toctree([target + ".md"])
                body += "\n"
                body += f"\n```{{figure}} {svg}\n"
                body += ":align: center\n"
                body += ":alt: Table Lineage Diagram\n"
                body += f":target: {target}.html\n"
                body += "\n"
                body += "Diagram illustrating data flow during transformations\n"
                body += "\n"
                body += "```\n\n"
        self.write_markdown(f"{title}\n{body}", of)

    def table_toctree(self, extra: List[str] = None) -> str:
        text = "\n```{toctree}\n"
        text += "---\n"
        text += "maxdepth: 1\n"
        text += "hidden:\n"
        text += "---\n"
        if extra:
            for target in extra:
                text += f"{target}\n"
        for t in sorted(self.tables):
            tname = self.tables[t].qualified_name
            text += f"tables/{tname}.md\n"
        text += "```\n\n"
        return text

    def table_list(self, of: str):
        title = "# Alphabetic list of all tables\n"
        body = "\n"
        for t in sorted(self.tables):
            tname = self.tables[t].qualified_name
            body += f"1. [{tname}](tables/{tname}.{self.link_ext()})\n"

        self.write_markdown(f"{title}\n{body}", of)

    def column_list(self, of: str):
        title = "# Alphabetic list of all columns in all tables\n"
        body = "\n"
        columns = dict()
        for t in self.tables:
            table = self.tables[t]
            tname = table.qualified_name
            for c in table.columns:
                if c in columns:
                    tset = columns[c]
                else:
                    tset = set()
                    columns[c] = tset
                tset.add(tname)

        body +=  "|  Column | Tables                    |\n"
        body +=  "|  ------ | ------------------------- |\n"
        ext = self.link_ext()
        for c in sorted(columns):
            tset = columns[c]
            tables = []
            for t in sorted(tset):
                tables.append(f"[{t}](tables/{t}/{c}.{ext})")
            row = ' <br/>'.join(tables)
            body += f"| {c}     | {row}\n"

        self.write_markdown(f"{title}\n{body}", of)

    def generate_graphs(self):
        fmt = self.options.get("fmt")
        generate_image = fmt and fmt != "none"
        tdir = os.path.join(self.basedir, "tables")
        lod = LOD[self.options.get("lod")]
        if not os.path.isdir(tdir):
            os.mkdir(tdir)
        with open(self.of, "w") as graph:
            self.to_dot(graph)
        self.table_list("table-list.md")
        self.column_list("column-list.md")
        if generate_image:
            os.system(f"dot -T {fmt} -O {self.of}")
            if fmt == "svg":
                svg = os.path.basename(self.of + ".svg")
                self.markdown(self.of + ".md", svg)
        if lod != LOD.none:
            n = 0
            for t in self.tables:
                d = os.path.join(tdir, t)
                if not os.path.isdir(d):
                    os.mkdir(d)
                table = self.tables[t]
                for c in table.columns:
                    column = table.columns[c]
                    basename = os.path.join(d, c)
                    if lod == LOD.min and not column.predecessors:
                        column.markdown(basename + ".md", svg=None)
                        continue
                    f = basename + ".dot"
                    with open(f, "w") as graph:
                        table.column_lineage_to_dot(c, graph)
                    if generate_image:
                        of = f"{basename}.{fmt}"
                        os.system(f"dot -T{fmt} -o{of} {f}")
                        if fmt == "svg":
                             # pass just the file name: the .svg is a sibling
                             # of the .md, and document references must stay
                             # relative (see the table-level case above)
                             column.markdown(basename + ".md",
                                             svg=os.path.basename(of))
                        n += 1
                        if (n % 10) == 0:
                            print('*', end='')
                            if (n % 300) == 0:
                                print()
                                print(t)
        return


class LOD(Enum):
    """
    Level of details to include in the generated pages
    """

    full = "full"
    none = "none"
    min = "min"


def parse_args() -> Dict:
    parser = argparse.ArgumentParser (
        description="Generate lineage information for specified domain"
    )
    parser.add_argument("yaml",
                        help="Paths to YaML files with domain definitions",
                        nargs='+')
    parser.add_argument("--fmt", "-f",
                        help="Format of generated image, if 'none', "
                             "then no image is generated",
                        default="none",
                        choices=["none","png","gif","ps2","svg","cmapx","jpeg"],
                        required=False)
    parser.add_argument("--lod",
                        help="Level of details: none (no column lineage), min (derived columns only), full (all columns)",
                        default="none",
                        choices=[s.value for s in LOD])
    parser.add_argument("--mode",
                        help="Documentation generation mode",
                        default=RenderMode.standalone.value,
                        choices=[s.value for s in RenderMode])
    parser.add_argument("--output", "--of", "-o",
                        help="with Table-level data lineage diagram",
                        default="tables.dot",
                        required=False)
    args = parser.parse_args()
    return vars(args)


if __name__ == '__main__':
    # YaML files must be added in correct order
    opts = parse_args()
    dd = DomainDict(opts["output"], opts)
    for a in opts["yaml"]:
        dd.add(a)
    dd.list()
    dd.generate_graphs()


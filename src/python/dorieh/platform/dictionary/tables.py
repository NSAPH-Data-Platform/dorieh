#  Copyright (c) 2023. Harvard University
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
Module to create list of tables from the Domain Data Model
"""
import math
import os
import re
from typing import Dict, Optional, List, Set
import html
import sqlparse

from dorieh.platform.data_model.domain import Domain
from dorieh.platform.dictionary import RenderMode
from dorieh.platform.dictionary.columns import Column
from dorieh.platform.dictionary.element import HTML, DataModelElement, Graph, fqn, qstr, \
    attrs2string, add_row, start_table, add_html_row, end_table, add_header_row, \
    hr, start_invisible_row, end_invisible_row, PANDOC


class Table(DataModelElement):
    def __init__(self, schema: str, name: str, domain: Domain, domain_dict):
        self.name = name
        self.schema = schema
        self.qualified_name = fqn(self.schema, self.name)
        super().__init__(domain.find(self.qualified_name))
        print("Adding: " + fqn(schema, name))
        self.domain = domain
        self.domain_dict = domain_dict
        self.domain_dict.tables[fqn(schema, name)] = self
        self.aggregation:Optional[Aggregation] = None
        self.union:Optional[Union] = None
        self.join:Optional[Join] = None
        self.parent = None
        self.type: str = "Table"
        self.master = None
        self.mode = domain_dict.mode
        create_block = None
        if "create" in self.block:
            create_block:Dict[str, Dict] = self.block["create"]
            self.aggregation = self.get_aggregation(schema, name, create_block)
            if "type" in create_block:
                self.type = str(create_block["type"])
            if "from" in create_block:
                from_block = create_block["from"]
                if self.aggregation is None:
                    if isinstance(from_block, list):
                        self.union = Union(schema, from_block, self.domain_dict)
                    elif isinstance(from_block, str):
                        if "join" in from_block:
                            self.join = Join(schema, from_block, self.domain_dict)
                        else:
                            tname = fqn(schema, from_block)
                            self.master = self.domain_dict.tables[tname]
        if "children" in self.block:
            children_block = self.block["children"]
            assert isinstance(children_block, dict)
            for child in children_block:
                child_table = Table(schema, child, self.domain,
                                    self.domain_dict)
                child_table.parent = self
                relation = Relation("parent-child", self, child_table)
                self.domain_dict.relations.append(relation)
        if self.aggregation is not None:
            relation = Relation(
                "aggregation",
                self.aggregation.parent,
                self,
                self.aggregation.on
            )
        elif self.parent is not None:
            relation = Relation("parent-child", self.parent, self)
        elif self.master is not None:
            relation = Relation("transformation", self.master, self)
        elif self.join is not None:
            for t in self.join.tables:
                relation = Relation("join", t, self, self.join.on)
                self.domain_dict.relations.append(relation)
            relation = None
        elif self.union is not None:
            for t in self.union.tables:
                relation = Relation("union", t, self)
                self.domain_dict.relations.append(relation)
            relation = None
        else:
            relation = None
        if relation is not None:
            self.domain_dict.relations.append(relation)
        self.columns = dict()
        if "columns" in self.block:
            columns_block = self.block["columns"]
            for column_block in columns_block:
                cblocks = Column.expand_macro1(column_block)
                for cblock in cblocks:
                    column = Column(self.qualified_name, cblock, self.mode, self.describe_column_type)
                    self.columns[column.name.lower()] = column
        if self.master is not None and create_block and "select" in create_block:
            self.add_master_columns()
        self.all_predecessors = None
        self.base_predecessors = None

    def add_master_columns(self):
        identifiers = Domain.get_select_from(self.block)
        if not identifiers:
            return
        for identifier in identifiers:
            if isinstance(identifier, sqlparse.sql.Identifier):
                c = identifier.get_name()
                if c in self.master.columns:
                    self.add_column_from_master(c)
                else:
                    self.add_column_from_sql(identifier)
            elif identifier.ttype[0] == "Wildcard":
                for c in self.master.columns:
                    self.add_column_from_master(c)

    def add_column_from_master(self, c: str):
        p_column = self.master.columns[c]
        column_block = {c: p_column.block}
        column = Column(self.qualified_name, column_block, self.mode, self.describe_column_type)
        column.copied = True
        self.columns[column.name.lower()] = column

    def add_column_from_sql(self, identifier: sqlparse.sql.Identifier):
        c = identifier.get_name()
        column = Column(self.qualified_name, {c: None}, self.mode, self.describe_column_type)
        column.expression = [identifier.value]
        column.copied = False
        identifiers = self.get_source_columns(identifier)
        column.predecessors.update(identifiers)
        self.columns[column.name.lower()] = column

    def get_source_columns(self, identifier: sqlparse.sql.Identifier) -> Set[str]:
        identifiers = set()
        for t in identifier.tokens:
            if t.is_keyword and t.value.lower() == "as":
                break
            if isinstance(t, sqlparse.sql.Identifier) or t.is_group:
                tname = t.get_name()
                if tname in self.master.columns:
                    identifiers.add(tname)
                elif len(t.tokens) > 1:
                    identifiers.update(self.get_source_columns(t))
        return identifiers

    def get_aggregation(self, schema: str, name: str, create_block: dict):
        if "group by" not in create_block:
            return None
        group_by_block :Dict[str, Dict] = create_block["group by"]
        assert isinstance(group_by_block, list)
        parent = create_block["from"]
        assert isinstance(parent, str)
        return Aggregation(schema, name, parent, group_by_block, self.domain_dict)

    def __str__(self) -> str:
        return self.type + " " + self.qualified_name

    def __eq__(self, __value):
        if isinstance(__value, Table):
            if self.name == __value.name and self.schema == __value.schema:
                return True
        return False

    def is_downstream(self, predecessor: str):
        if predecessor not in self.domain_dict.tables:
            raise ValueError(f"Unknown requirement {predecessor}")
        t = self.domain_dict.tables[predecessor]
        for r in self.domain_dict.relations:
            if r.x == t and r.y == self:
                return True
        return False

    def add_predecessors_for_column(self, c: str, lst: List):
        for t in self.columns[c.lower()].requires:
            if self.is_downstream(t):
                continue
            table = self.domain_dict.tables[t]
            relation = Relation("custom-select", table, self)
            self.domain_dict.relations.append(relation)
            lst.append(relation)
        return

    def get_predecessors(self) -> List:
        if self.base_predecessors is None:
            self.base_predecessors = []
            for relation in self.domain_dict.relations:
                if relation.y == self:
                    self.base_predecessors.append(relation)
            self.all_predecessors = []
            self.all_predecessors.extend(self.base_predecessors)
            for c in self.columns:
                self.add_predecessors_for_column(c, self.all_predecessors)
        return self.all_predecessors

    def get_predecessors_for_column(self, column: str) -> List:
        if self.base_predecessors is None:
            self.get_predecessors()
        predecessors = []
        predecessors.extend(self.base_predecessors)
        self.add_predecessors_for_column(column, predecessors)
        return predecessors

    def get_column_links(self, column: Column) -> List:
        pc = column.predecessors
        pt = self.get_predecessors_for_column(column.name)
        links = []
        for c in pc:
            c = c.lower()
            for r in pt:
                t = r.x
                if c in t.columns:
                    link = ColumnLink(r, t.columns[c], column)
                    links.append(link)
        if not links:
            for r in pt:
                t = r.x
                if column.name in t.columns:
                    link = ColumnLink(r, t.columns[column.name], column)
                    links.append(link)

        return links

    def calculate_column_lineage(self, column: Column, graph: Graph, recursion):
        links = self.get_column_links(column)

        if len(links) > 5 and recursion > 0:
            node_id = column.qualified_name + "_parent"
            width = 3 + math.log(len(links), 2)
            minlen = 2
            text = column.to_dot(
                node_id = qstr(node_id),
                node_label=qstr(f"{len(links)} incoming links (columns)"),
                attributes={
                    "shape": '"cylinder"',
                    "fillcolor": '"yellow"',
                    "style": '"filled"',
                    "minlen": minlen,
                    "width": 3,
                    "height": 1.5
                }
            )
            graph.add_node(node_id, text)
            graph.add_edge(GenericLink(node_id, column.qualified_name, width))
            return 

        if len(links) > 3:
            group = "parent_" + column.qualified_name
        else:
            group = None

        for link in links:
            graph.add_edge(link)
            parent = qstr(link.x.qualified_name)
            graph.add_node(parent, repr(link.x), group)
            link.relation.x.calculate_column_lineage(link.x, graph, recursion + 1)
        return

    def column_lineage_to_dot(self, column_name: str, out):
        column = self.columns[column_name]
        graph = Graph()
        graph.add_node(qstr(column.qualified_name), repr(column))
        self.calculate_column_lineage(column, graph, 0)
        graph.print(indent=1, file=out)

    def describe_column_type(self, column: Column):
        if column.column_type:
            return column.column_type
        if column.copied:
            return "copied"
        if column.expression:
            return "computed"
        if self.aggregation:
            if column.name in self.aggregation.columns:
                return "grouping"
            else:
                return "aggregated"
        if column.is_transformed():
            return "transformed"
        return ""

    def describe(self, format: str = 'html', basedir: str = '') -> str:
        if format == 'html':
            return self.describe_html(basedir)
        return self.describe_markdown(basedir)

    def describe_html(self, basedir: str = "") -> str:
        fmt = 'html'
        text = start_table(border=0, format=fmt)
        text += start_invisible_row(format=fmt)
        text += start_table(border=2, format=fmt)
        header = f'<FONT POINT-SIZE="20"><b>{self.type}: {self.qualified_name}</b></FONT>'
        text += add_row([header], format=fmt)

        if self.reference:
            text += add_row([f'<i>For more information see: {self.reference}</i>'], format=fmt)
        if self.description and "text" in self.description:
            value = html.escape(self.description["text"])
            text += add_row([value], format=fmt)
        if self.parent:
            name = self.parent.qualified_name
            text += add_row([f"Child table of {self.link_to_table(name, fmt)}"], format=fmt)
        if self.aggregation:
            name = self.aggregation.parent.qualified_name
            text += add_row([f"Aggregated from {self.link_to_table(name, fmt)} on {self.aggregation.on}"], format=fmt)
        if self.master:
            name = self.master.qualified_name
            text += add_row([f"Transformed from {self.link_to_table(name, fmt)}"], format=fmt)
        elif self.join:
            name = self.join.sql
            text += add_row([f"Join of tables: {name}"], format=fmt)
        if "primary_key" in self.block:
            pk = self.block["primary_key"]
            pk_text = ", ".join(pk)
            text += add_row([f"Primary Key: {pk_text}"], format=fmt)
        text += end_table(format=fmt)
        text += end_invisible_row(format=fmt)
        text += hr(format=fmt)
        text += start_invisible_row(format=fmt)
        text += start_table(border=2, format=fmt)
        text += add_header_row(["Column Name", "Column Type", "Datatype"], format=fmt)

        for c in sorted(self.columns):
            column = self.columns[c]
            text += add_row([
                self.link_to_column(column.name, basedir, fmt),
                self.describe_column_type(column),
                column.datatype
            ], format=fmt)
        text += end_table(format=fmt)
        text += end_invisible_row(format=fmt)
        text += end_table(format=fmt)
        return text

    def columns_toctree(self) -> str:
        text = "\n```{toctree}\n"
        text += "---\n"
        text += "maxdepth: 1\n"
        text += "hidden:\n"
        text += "---\n"
        for c in sorted(self.columns):
            text += f"{self.qualified_name}/{c}.md\n"
        text += "```\n\n"
        return text

    def describe_markdown(self, basedir: str = "") -> str:
        fmt = 'markdown'
        text = f"## Overview for {self.qualified_name}\n\n"
        if self.mode == RenderMode.sphinx:
            text += self.columns_toctree()
            text += "\n"

        if self.reference:
            text += f"*For more information see: {self.reference}*\n\n"
        if self.description and "text" in self.description:
            text += f"{self.description['text']}\n\n"
        if self.parent:
            name = self.parent.qualified_name
            text += f"Child table of {self.link_to_table(name, fmt)}\n\n"
        if self.aggregation:
            name = self.aggregation.parent.qualified_name
            text += f"Aggregated from {self.link_to_table(name, fmt)} on {self.aggregation.on}\n\n"
        if self.master:
            name = self.master.qualified_name
            text += f"Transformed from {self.link_to_table(name, fmt)}\n\n"
        elif self.join:
            name = self.join.sql
            text += f"Join of tables: {name}\n\n"
        if "primary_key" in self.block:
            pk = self.block["primary_key"]
            pk_text = ", ".join(pk)
            text += f"Primary Key: {pk_text}\n\n"

        sql = self.domain.ddl_by_table.get(self.qualified_name)
        sql = [l for l in sql if l != f"-- {self.qualified_name} skipped;"]
        # The provenance COMMENT embeds the URL Dorieh was installed from;
        # for a local checkout that is a machine-specific file:// path.
        # It belongs in the database it describes, but not in generated
        # documentation, hence it is redacted at display time only.
        sql = [
            re.sub(r"file:///[^\s\"']+", "file://<local checkout>", l)
            for l in sql
        ]
        if sql:
            text += "\n<details>\n\n"
            text += "<summary>SQL/DDL Statement</summary>\n\n"
            text += "```sql\n"
            for line in sql:
                text += line + '\n'
            text += "```\n"
            text += "\n</details>\n\n"

        text += hr(format=fmt)
        text += "## Columns:\n\n"
        text += add_header_row(["Column Name", "Column Type", "Datatype"], format=fmt)

        for c in sorted(self.columns):
            column = self.columns[c]
            text += add_row([
                self.link_to_column(column.name.lower(), basedir, fmt),
                self.describe_column_type(column),
                column.datatype
            ], format=fmt)
        text += "\n"
        return text

    def link_to_table(self, name: str, format: str = 'html') -> str:
        ext = "md" if (self.mode == RenderMode.sphinx) and format == "markdown" else "html"
        if format == 'markdown':
            return f"[{name}]({name}.{ext})"
        ref = f"{name}.{ext}"
        return f'<a href="{ref}">{name}</a>'

    def link_to_column(self, name: str, basedir: str, format: str = 'html') -> str:
        ext = "md" if (self.mode == RenderMode.sphinx) and format == "markdown" else "html"
        if format == 'markdown':
            cpath = f'{basedir}/{name}.{ext}'
            return f"[{name}]({cpath})"
        cpath = f'{basedir}/{name}.html'
        return f'<a href="{cpath}">{name}</a>'

    def html(self, of: str, svg=None):
        fmt = 'html'
        body = self.describe(basedir=self.qualified_name, format=fmt)
        if svg:
            body += hr(format=fmt)
            body += f'<object data="{svg}" type="image/svg+xml"></object>'
        block = HTML.format(
            title = f"Table {self.qualified_name}",
            body = body
        )
        with open(of, "wt") as out:
            print(block, file=out)

    def markdown(self, of: str, svg=None):
        fmt = 'markdown'
        body = self.describe(basedir=self.qualified_name, format=fmt)
        if svg:
            body += hr(format=fmt)
            body += f'<object data="{svg}" type="image/svg+xml"></object>'
        block = f"# {self.type.capitalize()} {self.qualified_name}\n\n{body}"
        with open(of, "wt") as out:
            print(block, file=out)
        if self.mode == RenderMode.standalone:
            fhtml = os.path.splitext(of)[0] + ".html"
            os.system(f"{PANDOC} --from markdown  --to html {of} > {fhtml}")


class Aggregation:
    def __init__(self, schema: str, name: str, parent: str, columns: List, domain_dict):
        self.domain_dict = domain_dict
        self.table = self.domain_dict.tables[fqn(schema, name)]
        if '.' not in parent:
            parent = fqn(schema, parent)
        self.parent = self.domain_dict.tables[parent]
        self.columns = columns
        self.on = "On " + ", ".join(self.columns)


class Union:
    def __init__(self, schema: str, tables: List[str], domain_dict):
        self.domain_dict = domain_dict
        self.tables = []
        for t in tables:
            if '.' not in t:
                t = fqn(schema, t)
            pattern = re.compile(t.replace('*', ".*"))
            for t2 in self.domain_dict.tables:
                if pattern.fullmatch(t2):
                    self.tables.append(self.domain_dict.tables[t2])
        return


class Join:
    def __init__(self, schema: str, s: str, domain_dict):
        self.domain_dict = domain_dict
        self.sql = s
        natural_join = "natural" in s
        s = s.lower()
        for keyword in ["natural", "left", "right", "full"]:
            s = s.replace(keyword, '')
        i = s.find("on")
        if i > 0:
            s = s[:i]
            self.on = s[i:]
        elif natural_join:
            self.on = "natural"
        else:
            self.on = None
        tables = s.split("join")
        self.tables = []
        for table in tables:
            table = table.strip()
            if '.' not in table:
                table = fqn(schema, table)
            self.tables.append(self.domain_dict.tables[table])
        return


class Relation:
    def __init__(self, reltype: str, x: Table, y: Table, data = None):
        self.type = reltype
        self.x = x
        self.y = y
        self.data = data

    def label(self):
        return self.data if self.data is not None else ''

    def as_edge_attr(self) -> Dict:
        attrs = dict()
        if self.data is None:
            attrs["label"] = '\t' + qstr(self.type)
        else:
            attrs["label"] = f'"\t{self.type} {self.label()}"'
        if self.type == "aggregation":
            attrs["penwidth"] = 5
            attrs["color"] = "blue"
        elif self.type == "union":
            attrs["penwidth"] = 2
            attrs["color"] = "chocolate"
        elif self.type == "parent-child":
            attrs["penwidth"] = 2
            attrs["color"] = "darkorchid"
        elif self.type == "custom-select":
            attrs["penwidth"] = 1
            attrs["color"] = "chartreuse"
        else:
            attrs["penwidth"] = 1
            attrs["color"] = "black"
        return attrs

    def __str__(self) -> str:
        data = self.label()
        return f'{self.type}: {str(self.x)} => {str(self.y)} {data}'


class ColumnLink:
    def __init__(self, r: Relation, x: Column, y: Column):
        self.relation = r
        self.x: Column = x
        self.y: Column = y

    def to_dot(self):
        node1 = qstr(self.x.qualified_name)
        node2 = qstr(self.y.qualified_name)
        attrs = self.relation.as_edge_attr()
        if self.y.copied:
            attrs["label"] = "Copied"
        elif "transformation" in attrs["label"]:
            attrs["label"] = attrs["label"].replace("transformation", "  Transformed")
        elif "aggregation" in attrs["label"]:
            attrs["label"] = attrs["label"].replace("aggregation", "  Aggregated")
        attrs["labelfloat"] = True
        return f"\t{node1} -> {node2} [{attrs2string(attrs)}];"

    def __str__(self):
        return f"{self.x.qualified_name} -> {self.y.qualified_name}"

    def __repr__(self):
        return self.to_dot()


class GenericLink:
    def __init__(self, node1, node2, width = 5.0):
        self.node1 = node1
        self.node2 = node2
        self.width = width

    def to_dot(self):
        attrs = dict()
        attrs["penwidth"] = self.width
        attrs["color"] = "goldenrod"
        return f"\t{qstr(self.node1)} -> {qstr(self.node2)} [{attrs2string(attrs)}];"

    def __str__(self):
        return f"{self.node1} -> {self.node2}"

    def __repr__(self):
        return self.to_dot()

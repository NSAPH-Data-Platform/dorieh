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
from typing import List, Tuple

SQL_TABLE_COLUMNS = """
SELECT
    COLUMN_NAME
FROM 
    information_schema.columns
WHERE 
    TABLE_SCHEMA = '{schema}' 
    AND TABLE_NAME = '{table}'

"""


SQL_SCHEMA_TABLES = """
SELECT 
    table_schema||'.'||TABLE_NAME 
FROM 
    information_schema.tables
WHERE 
    table_schema = '{schema}'

"""

class QueryBuilder:
    def __init__(self, connection):
        self.connection = connection
        self.tables: List[str] = []
        self.select: List[str] = []

    def add_table(self, table: str):
        self.tables.append(table)
        self.select.extend(self.get_columns(table))
        return self

    @staticmethod
    def is_quoted(s) -> bool:
        return len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'")

    @classmethod
    def unquote(cls, s):
        if cls.is_quoted(s):
            return s[1:-1]
        return s

    @staticmethod
    def quote(s):
        return f'"{s}"'

    @classmethod
    def split(cls, fqn:str) -> Tuple[str, ...]:
        tt = fqn.split('.')
        return tuple(tt)

    @classmethod
    def quote_column(cls, table: str, column: str) -> str:
        if cls.is_quoted(table):
            column = cls.quote(column)
        return f"{table}.{column}"

    def get_columns(self, table_fqn: str) -> List[str]:
        schema, table = self.split(table_fqn)
        sql = SQL_TABLE_COLUMNS.format(schema=self.unquote(schema), table=self.unquote(table))
        with (self.connection.cursor()) as cursor:
            cursor.execute(sql)
            columns = [self.quote_column(table, r[0]) for r in cursor]
        return columns

    def query(self) -> str:
        sql = "SELECT\n"
        sql += ",\n\t".join(self.select)
        sql += "\nFROM\n\t"
        sql += ", ".join(self.tables)
        return sql

    def clear(self):
        self.tables.clear()
        self.select.clear()
        return self

    @classmethod
    def get_tables(cls, connection, schema: str):
        with (connection.cursor()) as cursor:
            cursor.execute(SQL_SCHEMA_TABLES.format(schema=schema))
            tables = [r[0] for r in cursor]
        return tables



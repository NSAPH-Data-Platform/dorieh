#  Copyright (c) 2021. Harvard University
#
#  Developed by Research Software Engineering,
#  Faculty of Arts and Sciences, Research Computing (FAS RC)
#  Author: Eugene Pokidov
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

from typing import Iterable, List, Literal

Alignment = Literal['left', 'right', 'center']


class MDCreator:
    def __init__(self, file_name: str):
        self.file = open(file_name, 'w')

    def save(self):
        self.file.close()

    def add_header(self, text: str, level: int):
        prefix = '#' * level
        self.file.write(f'{prefix} {text}\n\n')

    def add_text(self, text: str):
        self.file.write(f'{text}\n\n')

    def add_table(self, data: Iterable[Iterable[str]], align: Alignment = 'left', first_row_is_header: bool = True):
        column_widths = self._calculate_column_widths(data)

        lines = []
        for row_num, data_row in enumerate(data):
            line = '| '
            for col_num, data_column in enumerate(data_row):
                column_width = column_widths[col_num]
                line += str(data_column).ljust(column_width) + ' | '

            lines.append(line)

            if row_num == 0 and first_row_is_header:
                line = self._get_header_separator(column_widths, align)
                lines.append(line)

        self.file.write('\n'.join(lines) + '\n\n')

    @staticmethod
    def _get_header_separator(column_widths: List[int], align: Alignment) -> str:
        line = '|'
        for column_width in column_widths:
            if align == 'left':
                line += ':' + '-' * (column_width + 1) + '|'
            elif align == 'right':
                line += '-' * (column_width + 1) + ':|'
            elif align == 'center':
                line += ':' + '-' * column_width + ':|'

        return line

    @staticmethod
    def _calculate_column_widths(data: Iterable[Iterable[str]]) -> List[int]:
        return list(map(len, map(lambda column: max(column, key=len), zip(*data))))

    def add_image(self, image_file_path: str):
        self.file.write(f'![]({image_file_path})\n\n')

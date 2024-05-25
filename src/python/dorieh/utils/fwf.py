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
A reader for fixed width files (FWF) produced by SAS providing the same
interface as `CSV reader <https://docs.python.org/3/library/csv.html>`_.

Each record is returned
in a way similar to the standard CSV reader, either as a list of objects
or as a dictionary, where keys are column headers.

To read the file, the application mus supply a list of columns.
If a file is produced by SAS the columns are usually described in File
Transfer Summary (FTS) file. However, FTS files are non-standard,
therefore a universal parser for FTS files is not feasible to supply.
"""

import logging
import os
from typing import List, Tuple
from dateutil import parser as date_parser
from dateutil.parser import ParserError


class FWFColumn:
    """A class describing a column of a fixed width (FWF) file"""

    def __init__(self, order: int, name: str, type: str, start: int,
                 width: Tuple[int,int]):
        self.name = name
        '''Name (header) of the column'''

        self.type = type
        '''Type of the column. Supported types: NUM, CHAR, DATE '''

        self.ord = order
        '''Ordinal number for the column'''

        self.start = start
        '''Starting position for the column (in bytes)'''

        self.length = width[0]
        '''Length of the column (in bytes)'''

        self.end = self.start + self.length
        '''Ending  position for the column (in bytes)'''

        self.d = width[1]
        '''Scale of the column for floating point numbers '''

    def __str__(self) -> str:
        return "{}:[{:d}-{:d}]".format(self.name,
                                       self.start,
                                       self.start + self.length
        )


class FWFMeta:
    """Metadata for the FWF file"""

    def __init__(self, path: str, record_len: int,
                 columns: List[FWFColumn],
                 number_of_rows=None, size=None):
        self.rlen = record_len
        """Record length, i.e. the length in bytes of the block for one record"""

        self.ncol = len(columns)
        '''Number of columns'''

        self.nrows = number_of_rows
        '''Number of rows, if given in the file descriptor (can be None)'''

        self.size =  os.path.getsize(path)
        '''File size in bytes'''

        if (size is not None) and (self.size != size):
            #assert self.size == size
            logging.warning("Size mismatch: expected: {:,}; actual: {:,}"
                            .format(size, self.size))
        self.path = path
        '''Physical path to the file on the file system'''

        self.columns = columns
        '''A list of FWFColumn instances, describing each column'''

        return


class FWFReader:
    """
    Fixed width files (FWF) reader. Returns records in the same way
    as standard CSV reader. Can return each record as either a list of values or
    a dictionary with column headers as keys.

    """

    def __init__(self, meta: FWFMeta, ret_dict: bool = False):
        """
        Constructor

        :param meta: an instance of FWFMeta
        :param ret_dict: boolean value, denoting whether to return each record
            as a dictionary
            
        """

        self.metadata = meta
        self.name = self.metadata.path
        self.input = None
        self.rdict = ret_dict
        self.line = 0
        self.data= None
        self.good_lines = 0
        '''Number of successfully read records'''

        self.bad_lines = 0
        '''Number of records that have failed parsing'''

        self.nb = 1000
        self.nr = 0
        self.b = 0
        self.record_start_pos = 0
        self.eof_len = None

    def column_names(self) -> List[str]:
        return [c.name for c in self.metadata.columns]

    def open(self):
        if self.input is not None:
            return
        if self.eof_len is None:
            with open(self.metadata.path, "rb") as f:
                b = f.read(self.metadata.rlen)
                self.eof_len = 0
                while f.read(1)[0] in [10, 13]:
                    self.eof_len += 1
        self.input = open(self.metadata.path, "rb")

    def close(self):
        if self.input is not None:
            self.input.close()
        return

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def validate(self):
        pass

    def __str__(self):
        return super().__str__() + ": " + self.metadata.path

    def read_record(self):
        i1 = self.record_start_pos + self.metadata.rlen
        data = self.data[self.record_start_pos:i1]
        while i1 < len(self.data) and self.data[i1] in [10, 13]:
            i1 += 1
        self.record_start_pos = i1
        exception_count = 0
        pieces = []
        n = len(self.metadata.columns)
        for c in self.metadata.columns:
            try:
                pieces.append(data[c.start:c.end])
            except:
                raise
        record = []
        for i in range(n):
            column = self.metadata.columns[i]
            s = pieces[i].decode("utf-8")
            try:
                if column.type == "NUM" and not column.d:
                    val = s.strip()
                    if val:
                        record.append(int(val))
                    else:
                        record.append(None)
                elif column.type == "DATE":
                    v = s.strip()
                    if v:
                        try:
                            record.append(date_parser.parse(v))
                        except ParserError as x:
                            logging.error(
                                "DateParser: Invalid date '{}':" 
                                "{}:{:d}: {}[{:d}]: - {}".format(
                                    v,
                                    self.name,
                                    self.line, column.name, column.ord,
                                    str(x)
                                )
                            )
                            record.append(None)
                    else:
                        record.append(None)
                else:
                    record.append(s)
            except Exception as x:
                logging.exception("{:d}: {}[{:d}]: - {}".format(
                    self.line, column.name, column.ord, str(x))
                )
                record.append(s)
                exception_count += 1
                if exception_count > 3:
                    logging.error(data)
                    raise FTSParseException("Too many exceptions", column.start)
        return record

    def next(self):
        if self.data is None or self.b >= self.nr:
            rlen = self.metadata.rlen + self.eof_len
            # +2 for '\r\n'
            self.data = self.input.read(rlen * self.nb)
            if len(self.data) == 0:
                raise StopIteration()
            self.nr = len(self.data) / rlen
            self.b = 0
            self.record_start_pos = 0
        try:
            self.line += 1
            self.b += 1
            record = self.read_record()
            self.good_lines += 1
        except FTSParseException as x:
            logging.exception("Line = " + str(self.line) + ':' + str(x.pos))
            self.bad_lines += 1
            self.on_parse_exception()
            return None
        except AssertionError as x:
            logging.exception("Line = " + str(self.line))
            self.bad_lines += 1
            self.on_parse_exception()
            return None
        if self.rdict:
            record = {
                self.metadata.columns[i].name:
                    record[i] for i in range(self.metadata.ncol)
            }
        return record

    def on_parse_exception(self):
        pass


class FTSParseException(Exception):
    """Exception raised when a record cannot be parsed"""

    def __init__(self, msg:str, pos:int):
        super(FTSParseException, self).__init__(msg, pos)
        self.pos = pos



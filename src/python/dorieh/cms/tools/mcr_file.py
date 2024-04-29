"""
Module used for converting CMS DAT files to CSV
"""

#  Copyright (c) 2021-2022. Harvard University
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

import datetime
import glob
import gzip
import os
import shutil
import traceback
from collections import OrderedDict
from typing import List

from dateutil import parser as date_parser
import csv


def log(s):
    with open("run.log", "at") as w:
        w.write(str(s) + '\n')


def width(s:str):
    if '.' in s:
        x = s.split('.')
        return (int(x[0]), int(x[1]))
    return (int(s), None)


class MedparParseException(Exception):
    """
    Exception raised if data in a DAT file cannot be parsed
    """

    def __init__(self, msg:str, pos:int):
        super(MedparParseException, self).__init__(msg, pos)
        self.pos = pos


class ColumnAttribute:
    """
    Attribute of a column as described in the FTS file
    """

    def __init__(self, start:int, end:int, conv):
        self.start = start
        self.end = end
        self.conv = conv

    def arg(self, line:str):
        try:
            return self.conv(line[self.start:self.end].strip())
        except:
            pass


class ColumnDef:
    """
    Column definition as described in the FTS file
    """

    def __init__(self, pattern):
        fields = pattern.split(' ')
        assert len(fields) == 7
        self.attributes = []
        i = 0
        c = 0
        for i in range(0, len(fields)):
            l = len(fields[i])
            if i in [0, 4]:
                f = int
            elif i in [5]:
                f = width
            else:
                f = str
            self.attributes.append(ColumnAttribute(c, c+l, f))
            c += l + 1

    def read(self, line):
        attrs = [a.arg(line) for a in self.attributes]
        return Column(*attrs)


class Column:
    """
    Class representing column metadata required for generating
    database schema
    """

    def __init__(self, ord:int, long_name:str, short_name:str, type:str, start:int, width, desc:str):
        self.name = short_name
        self.long_name = long_name
        self.type = type
        self.ord = ord
        self.start = start - 1
        self.length = width[0]
        self.end = self.start + self.length
        self.desc = desc
        self.d = width[1]

    def __str__(self) -> str:
        return "{}: [{}]".format(super().__str__(), self.name)


class MedicareFile:
    """
    Class to manipulate a single CMS DAT file
    """

    def __init__(self, dir_path: str, name: str,
                 year:str = None, dest:str = None):
        self.dir = dir_path
        if dest:
            if not os.path.exists(dest):
                os.makedirs(dest, exist_ok=True)
            self.dest = dest
        else:
            self.dest = self.dir
        self.name = os.path.join(self.dir, name)
        self.fts = '.'.join([self.name, "fts"])
        self.csv = os.path.join(self.dest, '.'.join([name, "csv.gz"]))
        if not os.path.isfile(self.fts):
            raise Exception("Not found: " + self.fts)

        pattern = "{}*.dat".format(name)
        self.dat = glob.glob(os.path.join(self.dir, pattern))

        self.line_length = None
        self.metadata = dict()
        self.columns = OrderedDict()
        self.init()
        block_size = self.metadata["Exact File Record Length (Bytes in Variable Block)"]
        block_size = block_size.strip()
        if ',' in block_size:
            print("[{}] Stripping commas: {}".format(self.fts, block_size))
            block_size = block_size.replace(',','')
        self.block_size = int(block_size)
        if not year:
            year = name[-4:]
        self.year = year

    def init(self):
        with open(self.fts) as fts:
            lines = [line for line in fts]
            for i in range(0, len(lines)):
                line = lines[i]
                if line.startswith('---') and '------------------' in line:
                    break
                if ':' in line:
                    x = line.split(':', 1)
                    self.metadata[x[0]] = x[1]

            cdef = ColumnDef(line)
            while i < len(lines) - 1:
                i += 1
                line = lines[i]
                if 'End of Document' in line:
                    break
                if not line.strip():
                    break
                if line.startswith("Note:"):
                    break
                column = cdef.read(line)
                self.columns[column.name] = column

    def read_record(self, data, ln) -> List:
        """
        Reads one record from DAT file

        :param data: a slice of raw data from DAT file
        :param ln:  line number, used for reporting
        :return: Record data as list
        """

        exception_count = 0
        pieces = {}
        for name in self.columns:
            column = self.columns[name]
            pieces[name] = data[column.start:column.end]
        record = []
        for name in self.columns:
            column = self.columns[name]
            s = pieces[name].decode("utf-8")
            try:
                if column.type == "NUM" and not column.d:
                    val = s.strip()
                    if val:
                        record.append(int(val))
                    else:
                        record.append(None)
                elif column.type == "DATE":
                    if s.strip():
                        record.append(date_parser.parse(s))
                    else:
                        record.append(None)
                else:
                    record.append(s)
            except Exception as x:
                log("{:d}: {}[{:d}]: - {}".format(
                    ln, column.name, column.ord, str(x))
                )
                record.append(s)
                exception_count += 1
                if exception_count > 3:
                    log(data)
                    raise MedparParseException("Too meany exceptions", column.start)
        return record

    def validate(self, record):
        """
        Asserts that the given record is consistent with
        the file from which it is read. 

        :param record: Record
        :return:   None
        """

        yc = None
        if "BENE_ENROLLMT_REF_YR" in self.columns:
            yc = "BENE_ENROLLMT_REF_YR"
        if "MEDPAR_YR_NUM" in self.columns:
            yc = "MEDPAR_YR_NUM"
        if yc is None:
            raise AssertionError("Year column was not found in FTS")
        assert record[self.columns[yc].ord - 1] == self.year

    def count_lines_in_source(self):
        """
        Counts number of lines in the original DAT file

        :return: number of lines
        """

        lines = 0
        blocks = 0
        bts = 0
        t1 = datetime.datetime.now()
        t0 = t1
        for dat in self.dat:
            print("{}: {}".format(t0.isoformat(), dat))
            counter = 0
            with open(dat, "rb") as source:
                while source.readable():
                    chunk = source.read(1024*1024)
                    if len(chunk) < 1:
                        break
                    blocks += 1
                    bts += len(chunk)
                    n = chunk.count(b'\n')
                    counter += n
                    t2 = datetime.datetime.now()
                    elapsed = t2 - t1
                    if elapsed > datetime.timedelta(minutes=10):
                        t1 = t2
                        print(
                            (
                                "{} running for {}. Blocks = {:,}, lines = {:,}"
                                + ", bytes = {:,}"
                            ).format(dat, str(t2 - t0), blocks, counter, bts)
                        )
                print("{}: {:d}".format(os.path.basename(dat), counter))
            lines += counter
        print("{}[Total]: {:d}".format(self.name, lines))
        return lines

    def count_lines_in_dest(self):
        """
        Counts number of lines in the resulting CSV file

        :return: number of lines
        """

        lines = 0
        if not os.path.isfile(self.csv):
            return 0
        with gzip.open(self.csv, "rt") as out:
            for _ in out:
                lines += 1
        print("{}: {:d}".format(self.csv, lines))
        return lines

    def status(self) -> str:
        """
        Checks if a given DAT file has been successfully converted to CSV

        :return: Value of the status of the conversion
        """

        try:
            if not os.path.isfile(self.csv):
                return "NONE"
            l2 = self.count_lines_in_dest()
            if l2 < 1:
                return "EMPTY"
            l1 = self.count_lines_in_source()
            if l1 != l2:
                return "MISMATCH: {:d}=>{:d}".format(l1, l2)
            return "READY"
        except Exception as x:
            print(self.fts)
            traceback.print_exception(type(x), x, None)
            return "ERROR: " + str(x)

    def status_message(self):
        """
        Checks if a given DAT file has been successfully converted to CSV

        :return: Message, containing the status of the conversion
        """

        return "{}: {}".format(self.fts, self.status())

    def export(self):
        """
        Performs actual conversion
        """

        if self.dir != self.dest:
            shutil.copy(self.fts, self.dest)
        t1 = datetime.datetime.now()
        t0 = t1
        with gzip.open(self.csv, "wt") as out:
            writer = csv.writer(out, quoting=csv.QUOTE_MINIMAL, delimiter='\t')
            for dat in self.dat:
                print(dat)
                counter = 0
                good = 0
                bad_lines = 0
                remainder = b''
                with open(dat, "rb") as source:
                    while source.readable():
                        l = self.block_size - len(remainder) + 100
                        block = remainder + source.read(l)
                        if len(block) < self.block_size:
                            break
                        idx = self.block_size
                        try:
                            record = self.read_record(block[:idx], counter)
                            self.validate(record)
                            writer.writerow(record)
                            good += 1
                        except MedparParseException as x:
                            log("Line = " + str(counter) + ':' + str(x.pos))
                            bad_lines += 1
                            log(x)
                            for idx in range(x.pos, self.block_size):
                                if block[idx] in [10, 13]:
                                    break
                        except AssertionError as x:
                            log("Line = " + str(counter))
                            bad_lines += 1
                            log(x)
                        while idx < len(block) and block[idx] in [10, 13]:
                            idx += 1
                        remainder = block[idx:]
                        block = None
                        counter += 1
                        if (counter%100000) == 0:
                            t2 = datetime.datetime.now()
                            t1 = t2
                            print("{}[{}]: {:,}/{:,}/{:,}".format(
                                dat, str(t2 - t0),
                                counter, good, bad_lines
                            ))
                print("{} processed. Bad lines: {:,}"
                      .format(self.fts, bad_lines))

    def info(self):
        """
        Prints info about the DAT file (metadata) to standard output
        """

        for s in [
            "Columns in File",
            "Exact File Record Length (Bytes in Variable Block)"
        ]:
            print("{}: {}".format(s, self.metadata[s]))

        for name in self.columns:
            c = self.columns[name]
            print("{:d} - {} - {} - {:d}".format(c.ord, c.name, c.type, c.start))


if __name__ == '__main__':
    m = MedicareFile(os.curdir, "medpar_all_file_res000017155_req007087_2015")
    m.info()
    m.export()

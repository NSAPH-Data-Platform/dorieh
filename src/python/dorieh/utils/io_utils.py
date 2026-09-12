#  Copyright (c) 2021-2024.  Harvard University
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

import codecs
import csv
import datetime
import fsspec
import glob
import gzip
import io
import json
import logging
import os
import tarfile
import tempfile
import zipfile
from datetime import datetime, timezone
from typing import IO, List, Tuple, Callable
from abc import ABC, abstractmethod

import requests
import yaml
from dateutil.parser import parse
from requests.models import Response


logger = logging.getLogger(__name__)
HEADERS = {'User-Agent': 'NSAPH Data warehouse app; https://github.com/ForomePlatform'}


def sizeof_fmt(num, suffix="B") -> str:
    if num is None:
        return "Unknown"
    units = ["", "K", "M", "G", "T", "P"]
    for unit in units:
        if unit == units[-1]:
            fmt = f"{num:.1f}"
        else:
            fmt = f"{num:3.1f}"
        if abs(num) < 1024.0 or unit == units[-1]:
            return fmt + f"{unit}{suffix}"
        num /= 1024.0
    return "Error calculating size"


class DownloadTask:
    def __init__(self, destination: str, urls: List = None, metadata = None):
        self.destination = destination
        if urls:
            self.urls = urls
        else:
            self.urls = []
        self.metadata = metadata

    def add_url(self, url: str):
        self.urls.append(url)

    def reset(self):
        os.remove(self.destination)

    def __str__(self):
        dest = os.path.abspath(self.destination)
        if len(self.urls) == 1:
            return "{} ==> {}".format(self.urls[0], dest)
        return "[{:d}]==> {}".format(len(self.urls), dest)

    def is_up_to_date(self, is_transformed: bool = True):
        if len(self.urls) == 1 and not is_transformed:
            return is_downloaded(self.urls[0], self.destination)
        for url in self.urls:
            if not is_downloaded(url, self.destination, 1000):
                return False
        return True


def as_stream(url: str, extension: str = ".csv", params = None, mode = None):
    """
    Returns the content of URL as a stream. In case the content is in zip
    format (excluding gzip) creates a temporary file

    :param mode: optional parameter to specify desirable mode: text or binary.
         Possible values: 't' or 'b'
    :param params: Optional. A dictionary, list of tuples or bytes
         to send as a query string.
    :param url: URL
    :param extension: optional, when the content is zip-encoded, the extension
        of the zip entry to return
    :return: Content of the URL or a zip entry
    """

    response = requests.get(url, stream=True, params=params)
    check_http_response(response)
    raw = response.raw
    if url.lower().endswith(".zip"):
        tfile = tempfile.TemporaryFile()
        download(url, tfile)
        tfile.seek(0)
        zfile = zipfile.ZipFile(tfile)
        entries = [
            e for e in zfile.namelist() if e.endswith(extension)
        ]
        assert len(entries) == 1
        stream = io.TextIOWrapper(zfile.open(entries[0]))
    else:
        if mode == 't':
            stream = io.TextIOWrapper(raw)
        else:
            stream = raw
    return stream


def as_content(url: str, params = None, mode = None):
    """
    Returns byte or text block with URL content

    :param url: URL
    :param params: Optional. A dictionary, list of tuples or bytes
         to send as a query string.
    :param mode: optional parameter to specify desirable return format:
         text or binary. Possible values: 't' or 'b', default is binary
    :return:  Content of the URL
    """

    response = requests.get(url, params=params)
    check_http_response(response)
    if mode == 't':
        return response.text
    return response.content


def as_csv_reader(url: str, mode = None) -> csv.DictReader:
    """
    An utility method to return the CSV content of the URL as CSVReader

    :param url: URL
    :return: an instance of csv.DictReader
    """
    stream = as_stream(url, mode=mode)
    reader = csv.DictReader(stream, quotechar='"', delimiter=',',
        quoting=csv.QUOTE_NONNUMERIC, skipinitialspace=True)
    return reader


def file_as_stream(filename: str, extension: str = ".csv", mode=None):
    """
    Returns the content of file as a stream. In case the content is in zip
    format (excluding gzip) creates a temporary file

    :param mode: optional parameter to specify desirable mode: text or binary.
         Possible values: 't' or 'b'
    :param filename: path to file
    :param extension: optional, when the content is zip-encoded, the extension
        of the zip entry to return
    :return: Content of the file or a zip entry
    """
    if filename.lower().endswith(".zip"):
        zfile = zipfile.ZipFile(filename)
        entries = [
            e for e in zfile.namelist() if e.endswith(extension)
        ]
        if len(entries) == 1:
            entry = entries[0]
        else:
            base_name, _ = os.path.splitext(os.path.basename(filename))
            entry = base_name + extension
            if entry not in entries:
                raise AssertionError(f"File {filename} should either contain a single entry or contain {entry}")
        stream = io.TextIOWrapper(zfile.open(entry))

    else:
        try:
            raw = open(filename, "b").read()
        except IOError as e:
            logger.exception("Cannot read %s: %s", filename, e)
            raise

        if mode == 't':
            stream = io.TextIOWrapper(raw)
        else:
            stream = raw

    return stream


def file_as_csv_reader(filename: str):
    """
    An utility method to return the CSV content of the file as CSVReader

    :param filename: path to file
    :return: an instance of csv.DictReader
    """
    stream = file_as_stream(filename)
    reader = csv.DictReader(
        stream, quotechar='"', delimiter=',',
        quoting=csv.QUOTE_NONNUMERIC, skipinitialspace=True,
    )
    return reader


def fopen(path: str, mode: str):
    """
    A wrapper to open various types of files

    :param path: Path to file
    :param mode: Opening mode
    :return: file-like object
    """
    if isinstance(path, io.BufferedReader):
        return codecs.getreader("utf-8")(path)
    lpath = path.lower()
    # if lpath.startswith("http")
    if lpath.endswith(".gz"):
        #return io.TextIOWrapper(gzip.open(path, mode))
        return gzip.open(path, mode)
    if 'b' in mode:
        return open(path, mode)
    return fsspec.open(path, mode, encoding="utf-8")


def check_http_response(r: Response):
    """
    An internal method raises an exception of HTTP response is not OK

    :param r: Response
    :return: nothing, raises an exception if response is not OK
    """
    if not r.ok:
        reason = r.reason
        if not reason:
            reason = r.content
        msg = "{}: HTTP Response {:d}; Reason: {}".format(
            r.url, r.status_code, reason
        )
        raise Exception(msg)


def download(url: str, to: IO):
    """A utility method to download large binary data to a file-like object"""
    response = requests.get(url, stream=True, headers=HEADERS)
    check_http_response(response)
    for chunk in response.iter_content(chunk_size=1048576):
        to.write(chunk)
        print('#', end='')
    print('.', end=' ')
    return


def is_downloaded(url: str, target: str, check_size: int = 0) -> bool:
    """
    Checks if the same data has already been downloaded

    :param check_size: Use default value (0) if target size should be equal
        to source size. If several urls are combined when downloaded
        then specify a positive integer to check that destination file
        size is greater than the specified value. Specifying negative
        value will disable size check
    :param url: URL with data
    :param target: Destination of the downloads
    :return: True if the destination file exists and is newer than
        URL content
    """
    if os.path.isfile(target):
        response = requests.head(url, allow_redirects=True)
        check_http_response(response)
        headers = response.headers
        remote_size = int(headers.get('content-length', 0))
        remote_date = parse(headers.get('Last-Modified', 0))
        stat = os.stat(target)
        local_size = stat.st_size
        local_date = datetime.fromtimestamp(stat.st_mtime, timezone.utc)
        date_check = local_date >= remote_date
        if check_size == 0:
            size_check = local_size == remote_size
        else:
            size_check = local_size > check_size
        return date_check and size_check
    return False


def write_csv(reader: csv.DictReader,
              writer: csv.DictWriter,
              transformer=None,
              filter=None,
              write_header: bool = True):
    """
    Rewrites the CSV content optionally transforming and
    filtering rows

    :param transformer: An optional callable that tranmsforms a row in place
    :param reader: Input data as an instance of csv.DictReader
    :param writer: Output source should be provided as csv.DictWriter
    :param filter: Optionally, a callable function returning True
        for rows that should be written to the output and False for those
        that should be omitted
    :param write_header: whether to first write header row
    :return: Nothing
    """
    counter = 0
    if write_header:
        writer.writeheader()
    for row in reader:
        if transformer:
            transformer(row)
        if (not filter) or filter(row):
            writer.writerow(row)
        counter += 1
        if (counter % 10000) == 0:
            print("*", end="")
    print()


def count_lines(f):
    with fopen(f, "r") as x:
        return sum(1 for line in x)


class Collector(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def writerow(self, data: List):
        pass

    def flush(self):
        pass


class CSVWriter(Collector):
    def __init__(self, out_stream):
        super().__init__()
        self.out = out_stream
        self.writer = csv.writer(out_stream,
                                 delimiter=',',
                                 quoting=csv.QUOTE_NONE)

    def writerow(self, row: List):
        self.writer.writerow(row)

    def flush(self):
        self.out.flush()


class ListCollector(Collector):
    def __init__(self):
        super().__init__()
        self.collection = []

    def writerow(self, data: List):
        self.collection.append(data)

    def get_result(self):
        return self.collection


def as_dict(json_or_yaml_file: str) -> dict:
    if isinstance(json_or_yaml_file, str) and os.path.isfile(json_or_yaml_file):
        with open(json_or_yaml_file) as f:
            ff = json_or_yaml_file.lower()
            if ff.endswith(".json"):
                content = json.load(f)
            elif ff.endswith(".yml") or ff.endswith(".yaml"):
                content = yaml.safe_load(f)
            else:
                raise Exception("Unsupported format for user request: {}"
                                .format(json_or_yaml_file) +
                                ". Supported formats are: JSON, YAML")
    elif isinstance(json_or_yaml_file, dict):
        content = json_or_yaml_file
    else:
        t = str(type(json_or_yaml_file))
        raise Exception("Unsupported type of the specification: {}".format(t))
    return content



def basename(path):
    """
    Returns a name without extension of a file or an
    archive entry

    :param path: a path to a file or archive entry
    :return: base name without full path or extension
    """

    if isinstance(path, tarfile.TarInfo):
        full_name = path.name
    else:
        full_name = str(path)
    name, _ = os.path.splitext(os.path.basename(full_name))
    return name


def is_readme(name: str) -> bool:
    """
    Checks if a file is a documentation file
    This method is used to extract some metadata from documentation
    provided as markDOwn files

    :param name:
    :return:
    """

    name = name.lower()
    if name.endswith(".md"):
        return True
    if name.startswith("readme"):
        return True
    if name.startswith("read.me"):
        return True
    if "readme" in name:
        return True
    return False


def get_entries(path: str) -> Tuple[List,Callable]:
    """
    Returns a list of entries in an archive or files in
    a directory

    :param path: path to a directory or an archive
    :return: Tuple with the list of entry names and a method
        to open these entries for reading

    """

    if path.endswith(".tar") or path.endswith(".tgz") or path.endswith(
            ".tar.gz"):
        tfile = tarfile.open(path)
        entries = [
            e for e in tfile.getmembers()
                if e.isfile() and not is_readme(e.name)
        ]
        f = lambda e: codecs.getreader("utf-8")(tfile.extractfile(e))
    elif path.endswith(".zip"):
        zfile = zipfile.ZipFile(path)
        entries = [
            e for e in zfile.namelist() if not is_readme(e)
        ]
        f = lambda e: io.TextIOWrapper(zfile.open(e))
    elif os.path.isdir(path):
        entries = [
            filename for filename in glob.iglob(
                os.path.join(path, '**', '**'),
                recursive=True
            )
            if os.path.isfile(filename) and not is_readme(filename)
        ]
        f = lambda e: fopen(e, "rt")
    elif os.path.isfile(path):
        entries = [path]
        f = lambda e: fopen(e, "rt")
    else:
        entries = [path]
        f = lambda e: e
    return entries, f


def get_readme(path:str):
    """
    Looks for a README file in the specified path
    :param path: a path to a folder or an archive
    :return: a file that is possibly a README file
    """

    encoding = "utf-8"
    if path.endswith(".tar") or path.endswith(".tgz") or path.endswith(
            ".tar.gz"):
        tfile = tarfile.open(path, encoding=encoding)
        readmes = [
            tfile.extractfile(e).read().decode(encoding) for e in tfile.getmembers()
                if e.isfile() and is_readme(e.name)
        ]
    elif path.endswith(".zip"):
        zfile = zipfile.ZipFile(path)
        readmes = [
            io.TextIOWrapper(zfile.open(e)).read()
                    for e in zfile.namelist() if is_readme(e)
        ]
    elif os.path.isdir(path):
        files = os.listdir(path)
        readmes = [f for f in files if is_readme(f)]
    else:
        readmes = None
    if readmes:
        return readmes[0]
    return None


def is_dir(path: str) -> bool:
    """
    Determine if a certain path specification refers
        to a collection of files or a single entry.
        Examples of collections are folders (directories)
        and archives

    :param path: path specification
    :return: True if specification refers to a collection of files
    """

    return (path.endswith(".tar")
            or path.endswith(".tgz")
            or path.endswith(".tar.gz")
            or path.endswith(".zip")
            or os.path.isdir(path)
    )


def is_yaml_or_json(path: str) -> bool:
    path = path.lower()
    for ext in [".yml", ".yaml", ".json"]:
        if path.endswith(ext) or path.endswith(ext + ".gz"):
            return True
    return  False


### R Dependencies

try:
    from rpy2.robjects import DataFrame, NA_Logical, NA_Real, NA_Integer, \
        NA_Character, NA_Complex
    from dorieh.utils.pyfst import vector2list, FSTReader

    def fst2csv(path: str, buffer_size = 10000):
        if not path.endswith(".fst"):
            raise Exception("Unknown format of file " + path)
        name = path[:-4]
        dest = name + ".csv.gz"
        n = 0
        t0 = datetime.now()
        with FSTReader(path, returns_mapping=True) as reader, fopen(dest, "wt") as output:
            writer = csv.DictWriter(output, reader.columns, quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            width = len(reader.columns)
            for row in reader:
                writer.writerow(row)
                n += 1
                if (n % buffer_size) == 0:
                    t2 = datetime.now()
                    rate = n / (t2 - t0).seconds
                    logging.info("Read {}: {:d} x {:d}; {} {:f} rows/sec".format(path, n, width, str(t2-t0), rate))
        logger.info("Complete. Total read {}: {:d} x {:d}".format(path, width, n))
        return


    def dataframe2csv(df: DataFrame, dest: str, append: bool):
        t0 = datetime.datetime.now()
        columns = {
            df.colnames[c]: vector2list(df[c]) for c in range(df.ncol)
        }
        t1 = datetime.datetime.now()

        if append:
            mode = "at"
        else:
            mode = "wt"
        with fopen(dest, mode) as output:
            writer = csv.DictWriter(output, columns, quoting=csv.QUOTE_NONNUMERIC)
            if not append:
                writer.writeheader()
            for r in range(df.nrow):
                row = {
                    column: columns[column][r] for column in columns
                }
                writer.writerow(row)
        t2 = datetime.datetime.now()
        print("{} + {} = {}".format(str(t1-t0), str(t2-t1), str(t2-t0)))
        return

    R_NA_values = [
        NA_Logical,
        NA_Real,
        NA_Integer,
        NA_Character,
        NA_Complex,
        str(NA_Logical),
        str(NA_Real),
        str(NA_Integer),
        str(NA_Character),
        str(NA_Complex)
    ]


except:
    R_NA_values= []

class SpecialValues:
    NA = "NA"
    NaN = "NaN"

    @classmethod
    def is_missing(cls, v) -> bool:
        try:
            if v is None:
                return True
            return v in [
                cls.NA,
                cls.NaN,
            ]   + R_NA_values
        except:
            logging.error("Value: " + str(v))
            raise

    @classmethod
    def is_untyped(cls, v) -> bool:
        if not v:
            return True
        return cls.is_missing(v) or v in ['0']


class CSVFileWrapper():
    """
    A wrapper around CSV reader that does:

    * Counts characters and line read
    * Logging of the progress of the file being read
    * Performs on-the-fly replacement of null and special
      values
    """

    def __init__(self, file_like_object, sep = ',', null_replacement = SpecialValues.NA):
        self.file_like_object = file_like_object
        self.sep = sep
        self.null_replacement = null_replacement
        self.empty_string = self.sep + self.sep
        self.null_string = self.sep + self.null_replacement + sep
        self.empty_string_eol = self.sep + '\n'
        self.null_string_eol = self.sep + self.null_replacement + '\n'
        self.l = len(sep)
        self.remainder = ""
        self.line_number = 0
        self.last_printed_line_number = 0
        self.chars = 0

    def __getattr__(self, called_method):
        if called_method == "readline":
            return self._readline
        if called_method == "read":
            return self._read
        return getattr(self.file_like_object, called_method)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.file_like_object.close()

    def _replace_empty(self, s: str):
        while self.empty_string in s:
            s = s.replace(self.empty_string, self.null_string)
        s = s.replace(self.empty_string_eol, self.null_string_eol)
        return s

    def _readline(self):
        line = self.file_like_object.readline()
        self.line_number += 1
        self.chars += len(line)
        return self._replace_empty(line)

    def _read(self, size, *args, **keyargs):
        if (len(self.remainder) < size):
            raw_buffer = self.file_like_object.read(size, *args, **keyargs)
            buffer = raw_buffer
            while buffer[-self.l:] == self.sep:
                next_char = self.file_like_object.read(self.l)
                buffer += next_char
            buffer = self._replace_empty(buffer)
        else:
            raw_buffer = ""
            buffer = raw_buffer
        if self.remainder:
            buffer = self.remainder + buffer
            self.remainder = ""

        if len(buffer) > size:
            self.remainder = buffer[size - len(buffer):]
            result = buffer[0:size]
        else:
            result = buffer

        self.chars += len(result)
        nl = result.count('\n')
        self.line_number += nl
        t = datetime.datetime.now()
        if (self.line_number - self.last_printed_line_number) > 1000000:
            if self.chars > 1000000000:
                c = "{:7.2f}G".format(self.chars/1000000000.0)
            elif self.chars > 1000000:
                c = "{:6.2f}M".format(self.chars/1000000.0)
            else:
                c = str(self.chars)
            dt = datetime.datetime.now() - t
            t = datetime.datetime.now()
            logging.info("{}: Processed {:,}/{} lines/chars [{}]"
                  .format(str(t), self.line_number, c, str(dt)))
            self.last_printed_line_number = self.line_number
        return result



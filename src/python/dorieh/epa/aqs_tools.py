"""
Python module to download EPA AQS Data hosted at https://www.epa.gov/aqs

The module can be used as a library of functions
to be called from other python scripts.

The data is downloaded from https://aqs.epa.gov/aqsweb/airdata/download_files.html

The tool adds a column containing a uniquely generated Monitor Key

Probably the only method useful to external user is :func:`download_aqs_data`

"""

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

import csv
import logging
from typing import List, Dict
import os

from dorieh.epa import STATE_CODE, COUNTY_CODE, \
    SITE_NUM, PARAMETER_CODE, MONITOR, RECORD, add_record_num
from dorieh.epa.aqs_ds_def import AQSContext, Parameter, Aggregation
from dorieh.utils.io_utils import as_csv_reader, fopen, write_csv, \
    DownloadTask

BASE_AQS_EPA_URL = "https://aqs.epa.gov/aqsweb/airdata/"
ANNUAL_URI = "annual_conc_by_monitor_{year}.zip"
DAILY_URI = "daily_{parameter}_{year}.zip"
MONITOR_FORMAT = "{state}{county:03d}-{site:04d}"


def transfer(reader: csv.DictReader, writer: csv.DictWriter, flt=None,
             header: bool = True):
    """
    Specific for EPA AQS Data

    Rewrites the CSV content adding Monitor Key and optionally
    filtering rows by a provided list of parameter codes

    :param reader: Input data as an instance of csv.DictReader
    :param writer: Output source should be provided as csv.DictWriter
    :param flt: Optionally, a callable function returning True
        for rows that should be written to the output and False for those
        that should be omitted
    :param header: whether to first write header row
    :return: Nothing
    """
    write_csv(reader, writer, transformer=add_more_columns, filter=flt,
              write_header=header)


def add_more_columns(row: Dict):
    add_monitor_key(row)
    add_record_key(row)


record_index = 0


def add_monitor_key(row: Dict):
    """
    Internal method to generate and add unique Monitor Key

    :param row: a row of AQS CSV file
    :return: Nothing, modifies the given row in place
    """

    monitor = MONITOR_FORMAT.format(state = row[STATE_CODE],
                                    county = int(row[COUNTY_CODE]),
                                    site = int(row[SITE_NUM]))
    row[MONITOR] = monitor


def add_record_key(row: Dict):
    global record_index
    record_index += 1
    add_record_num(row, record_index)


def download_data(task: DownloadTask):
    """
    A utility method to download the content of given URL to the given file

    :param url: Source URL
    :param target: Target file path
    :param parameters: An optional list of EPA AQS Parameter codes to include
        in the output
    :param append: whether to append to an existing file
    :return: Nothing
    """

    target = task.destination
    parameters = task.metadata

    write_header = True
    for url in task.urls:
        print("{} => {}".format(url, target))
        with fopen(target, "at") as ostream:
            attempt = 0
            while True:
                try:
                    reader = as_csv_reader(url)
                    break
                except Exception:
                    attempt += 1
                    if attempt > 3:
                        raise
                    logging.exception("Attempt {:d}: Error downloading {}".
                                      format(attempt, url))
            fieldnames = list(reader.fieldnames)
            fieldnames.append(MONITOR)
            fieldnames.append(RECORD)
            writer = csv.DictWriter(ostream, fieldnames, quotechar='"',
                                    delimiter=',',
                                    quoting=csv.QUOTE_NONNUMERIC)
            if parameters:
                flt = lambda row: int(row[PARAMETER_CODE]) in parameters
            else:
                flt = None
            transfer(reader, writer, flt, write_header)
            write_header = False


def destination_path(destination: str, path: str) -> str:
    """
    A utility method to construct destination file path

    :param destination: Destination directory
    :param path: Source path in URL
    :return: Path on a file system
    """
    return os.path.join(destination, path.replace(".zip", ".csv.gz"))


def collect_annual_downloads(destination: str, path: str,
                             contiguous_year_segment: List,
                             parameters: List) -> DownloadTask:
    """
    A utility method to collect all URLs that should be downloaded for a given
    list of years and EPA AQS parameters

    :param destination: Destination directory for downloads
    :param path: path element
    :param contiguous_year_segment: a list of contiguous years taht can be
        saved in the same file
    :param parameters: List of EPA AQS Parameter codes
    :param downloads: The resulting collection of downloads that have to
        be performed
    :return: downloads list
    """
    if not parameters:
        target = destination_path(destination, path)
    else:
        f = path[:-4] + '_' + '_'.join(map(str, parameters)) + ".csv.gz"
        target = os.path.join(destination, f)

    pp = [int(p) for p in parameters]
    task = DownloadTask(target, metadata=pp)
    for year in contiguous_year_segment:
        task.add_url(BASE_AQS_EPA_URL + ANNUAL_URI.format(year=year))
    return task

def collect_daily_downloads(destination: str, ylabel: str,
                            contiguous_year_segment: List,
                            parameter) -> DownloadTask:
    """
    A utility method to collect all URLs that should be downloaded for a given
    list of years and EPA AQS parameters

    :param destination: Destination directory for downloads
    :param ylabel: a label to use for years in the destination path
    :param contiguous_year_segment: a list of contiguous years taht can be
        saved in the same file
    :param parameters: List of EPA AQS Parameter codes
    :param downloads: The resulting collection of downloads that have to
        be performed
    :return: downloads list
    """
    if isinstance(parameter, Parameter) or parameter in Parameter.values():
        p = Parameter(parameter)
    else:
        p = int(parameter)
    path = DAILY_URI.format(parameter=p, year=ylabel)
    target = destination_path(destination, path)

    task = DownloadTask(target)
    base_url = BASE_AQS_EPA_URL + DAILY_URI.format(parameter=int(parameter),
                                                   year="{year}")
    for year in contiguous_year_segment:
        task.add_url(base_url.format(year=year))
    return task


def collect_aqs_download_tasks (context: AQSContext):
    """
    Main entry into the library

    :param aggregation: Type of time aggregation: annual or daily
    :param years: a list of years to include, if None - then all
        years are included
    :param destination: Destination Directory
    :param parameters: List of EPA AQS Parameter codes. For annual
        aggregation can be empty, in which case all data is downloaded.
        Required for daily aggregation. Can contain either integer codes, or
        mnemonic instanced of Parameter Enum or both.
    :param merge_years:
    :return:
    """

    parameters = context.parameters
    if context.aggregation == Aggregation.DAILY:
        assert len(parameters) > 0

    years = sorted(context.years)
    segment = [years[0]]
    contiguous_years = [segment]
    for i in range(1, len(years)):
        if context.merge_years and years[i-1] == years[i] - 1:
            segment.append(years[i])
        else:
            segment = [years[i]]
            contiguous_years.append(segment)

    if parameters:
        parameters = sorted(parameters)

    downloads = []
    for segment in contiguous_years:
        if len(segment) == 1:
            y = str(segment[0])
        else:
            y = "{}-{}".format(segment[0], segment[-1])

        if context.aggregation == Aggregation.ANNUAL:
            path = ANNUAL_URI.format(year=y)
            task = collect_annual_downloads(context.destination, path, segment,
                                            parameters)
            downloads.append(task)
        elif context.aggregation == Aggregation.DAILY:
            for parameter in parameters:
                task = collect_daily_downloads(context.destination, y, segment,
                                               parameter)
                downloads.append(task)
    return downloads



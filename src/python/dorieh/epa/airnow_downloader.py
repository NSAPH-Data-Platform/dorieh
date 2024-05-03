"""
Toolkit and API for downloading AirNow
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
import json
import logging
import math
import os
import time
from datetime import timedelta, datetime, date
from pathlib import Path
from typing import List, Union, Dict

import pandas
import yaml

from dorieh.epa import add_record_num, MONITOR
from dorieh.epa.airnow_ds_def import AirNowContext
from dorieh.gis.annotator import GISAnnotator
from dorieh.utils.qc import Tester
from dorieh.utils.io_utils import fopen, as_content


class AirNowDownloader:
    """
    Main class to download AirNow data
    """

    SITE = "FullAQSCode"
    VALUE = "Value"
    MONITOR_FORMAT = "{state}-{fips:05d}-{site}"
    AQI = "AQI"
    GIS_COLUMNS = ["ZCTA", "STATE", "FIPS5", "STATEFP", "COUNTYFP", "COUNTY", "STUSPS"]
    bbox = "-140.58788,20.634217,-60.119132,60.453505"

    format_csv = "text/csv"
    format_json = "application/json"
    datatype = "b"
    verbose = 1
    max_attempts = 5
    time_to_sleep_between_attempts = 10
    url = "https://www.airnowapi.org/aq/data/"

    @staticmethod
    def get_config(key: str):
        candidates = [
            ".airnow.yaml",
            ".airnow.json",
            os.path.expanduser(".airnow.yaml"),
            os.path.expanduser(".airnow.json")
        ]
        for f in candidates:
            if os.path.exists(f):
                with open(f) as fp:
                    if f.endswith("yaml"):
                        content = yaml.safe_load(fp)
                    elif f.endswith(".json"):
                        content = json.load(fp)
                    else:
                        raise Exception(f)
                value = content[key]
                logging.info("AirNow {} has been found in {}".format(key, f))
                return value
        return None

    @staticmethod
    def look_for_api_key():
        key = os.getenv('AIRNOWKEY', None)
        if key:
            logging.info("AirNow API Key has been found in the environment")
            return key
        key = AirNowDownloader.get_config("api key")
        if key:
            return key
        raise Exception("AirNow API Key was not found")

    def __init__(self,
                 target: str = None,
                 parameter: str = None,
                 api_key: str = None,
                 qc = None,
                 context: AirNowContext = None):
        """
        Constructor.

        :param target: File name, where downloaded data is saved.
            If file name includes substring ".json", then the data is saved in
            JSON format, otherwise it is saved as CSV. If target is not
            specified (None), then the data is not saved to file but is
            returned to the caller. The latter mode is useful for testing.
        :param parameter: Comma-separated list of parameters to download.
            In practice because of AirNow API limitations, if more than
            one parameter is specified, a runtime error will occur.
            Possible values:
                - Ozone (O3, ozone)
                - PM2.5 (pm25)
                - PM10 (pm10)
                - CO (co)
                - NO2 (no2)
                - SO2 (so2)

        :param api_key: Optional API Key to use with AirNow api. If not
            specified, then it is searched in a file named `.airnow.yaml`
            or `.airnow.json` first in working directory and then in user's
            home directory

        """

        self.record_index = 0
        self.options = dict()
        self.options["bbox"] = self.bbox
        self.options["format"] = self.format_json
        self.options["datatype"] = self.datatype
        self.options["verbose"] = self.verbose
        if parameter is not None:
            self.options["parameters"] = parameter
        else:
            self.options["parameters"] = context.parameters
        if target is not None:
            self.target = target
        else:
            self.target = context.destination
        if api_key is None:
            api_key = context.api_key
        if api_key is None:
            api_key = self.look_for_api_key()
        self.options["api_key"] = api_key
        if context.shapes:
            shapes = context.shapes
        else:
            shapes = self.get_config("shapes")
        if not shapes:
            raise Exception("Shape files are not specified")
        self.annotator = GISAnnotator(shapes, self.GIS_COLUMNS)
        self.sites = dict()
        self.columns = None
        self.qc = qc
        self.header_written = False
        if parameter == "pm25":
            self.t_int = [("00", "23:59")]
        else:
            self.t_int = [("00", "11:59"), ("12:00", "23:59")]
        self._states = dict()

    def reset(self):
        if os.path.exists(self.target):
            os.remove(self.target)
        self.columns = None

    def get_content(self, options):
        attempts = 0
        content = None
        while True:
            try:
                content = as_content(self.url, params=options, mode='t')
                break
            except Exception as x:
                attempts += 1
                if attempts < self.max_attempts:
                    logging.warning(str(x))
                    time.sleep(self.time_to_sleep_between_attempts * attempts)
                    continue
                raise
        return content

    @staticmethod
    def merge(contents: List[str]) -> str:
        content = []
        for c in contents:
            content.extend(json.loads(c))
        return json.dumps(content)

    def download(self, requested_date) -> Union[List[dict], str]:
        """
        Download data for a date

        :param requested_date:  date to be downloaded
        :return: If target has been specified, then this method returns
            the target file name, otherwise it returns a list of dictionaries
            where each dictionary is structured as JSON, with column names
            serving as keys
        """

        is_json = ".json" in self.target
        options = dict(self.options)
        contents = []
        for interval in self.t_int:
            options["startdate"] = str(requested_date) + 't' + interval[0]
            options["enddate"] = str(requested_date) + 't' + interval[1]
            logging.debug("Requesting AirNowAPI data... Date = " + str(requested_date))
            contents.append(self.get_content(options))
        if len(contents) > 1:
            content = self.merge(contents)
        else:
            content = contents[0]
        rows = self.process(content)
        if not rows:
            raise Exception("Empty response for " + str(requested_date))
        if self.target is None:
            return rows
        with fopen(self.target, "at") as output:
            if is_json:
                for row in rows:
                    json.dump(row, output)
                    output.write('\n')
            else:
                if not self.header_written:
                    self.write_csv_header(rows[0])
                    self.header_written = True
                self.dump_csv(output, rows)
        return self.target

    @staticmethod
    def dump_csv(output, rows):
        """
        Internal method used by download
        Dumps rows as CSV file

        """

        row = rows[0]
        writer = csv.DictWriter(output, row.keys(), delimiter=',',
                                quoting=csv.QUOTE_NONNUMERIC)
        writer.writerows(rows)

    def write_csv_header(self, row):
        """
        Internal method used by download
        Writes CSV file ehader

        """

        with fopen(self.target, "wt") as output:
            writer = csv.DictWriter(output, row.keys(), delimiter=',',
                                    quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()

    def process(self, content: str) -> List[dict]:
        """
        Internal method

        Aggregates hourly data into day's averages and joins with geographic
        information such as state, county, zip code.

        :param content: Raw content received from AirNow API call
            see: https://docs.airnowapi.org/Data/docs
        :return: List of dictinaries, where each row is represented as a
            dictionary, with column names serving as keys
        """

        df = pandas.read_json(content)
        agg = {
            c: "mean" if c in [self.VALUE, self.AQI]
                                else "first"
            for c in df.columns if c != self.SITE
        }
        aggregated = df.groupby(self.SITE).agg(agg).reset_index()
        self.check_sites(aggregated)
        if self.qc:
            self.do_qc(df)
        data = []
        for _, row in aggregated.iterrows():
            record = row.to_dict()
            site = record[self.SITE]
            record.update(self.sites[site])
            self.record_index += 1
            add_record_num(record, self.record_index)
            self.add_monitor_key(record)
            data.append(record)
        return data

    @classmethod
    def add_monitor_key(cls, record: Dict):
        state = record["STATE"]
        if not state:
            state = "__"
        fips5 = record["FIPS5"]
        if not fips5:
            fips5 = 0
        site = record[cls.SITE]
        if isinstance(site, int):
            site = "{:09d}".format(site)
        monitor = cls.MONITOR_FORMAT.format(
            state = state,
            fips = int(fips5),
            site = site)
        record[MONITOR] = monitor

    def do_qc(self, df: pandas.DataFrame):
        src = Path(__file__).parents[1]
        qc = os.path.join(src, "qc", "tests.yaml")
        tester = Tester("AirNow", qc)
        tester.check(df)

    def check_sites(self, df: pandas.DataFrame):
        sites = df[self.SITE]
        new_monitors = {m for m in sites if m not in self.sites}
        if not new_monitors:
            return
        x = "Longitude"
        y = "Latitude"
        sites = df[[self.SITE, x, y]]
        sites = sites[sites[self.SITE].isin(new_monitors)]
        annotated = self.annotator.join(sites, x = x, y = y)
        for _, site in annotated.iterrows():
            row = {
                key: site[key] if not (
                        isinstance(site[key], float) and math.isnan(site[key])
                ) else None
                for key in self.GIS_COLUMNS
            }

            row[self.SITE] = site[self.SITE]
            self.sites[site[self.SITE]] = row
        return

    def download_range(self, start_date, end_date = datetime.now().date()):
        """
        Downloads data for a range of dates. To invoke this method the
        application must have specified a target file

        :param start_date: First date in the range to download (inclusive)
        :param end_date: Last date in the range to download (inclusive)
        """

        assert self.target, "Range downloading is only supported when target " \
                            "file is specified "
        dt = start_date
        year = dt.year
        month = dt.month
        logging.info("Starting download from: " + str(dt))
        while True:
            t = datetime.now()
            self.download(dt)
            if dt >= end_date:
                break
            dt += timedelta(days = 1)
            if dt.month != month:
                logging.info("{:d}-{:d}".format(year, month))
            month = dt.month
            year = dt.year
            elapsed = datetime.now() - t
            if elapsed.total_seconds() < 7.2:
                time.sleep(7.2 - elapsed.total_seconds())
        logging.info("Download complete. Last downloaded date: {}".format(str(dt)))


def test():
    downloader = AirNowDownloader("airnow_no2.json.gz", "no2")
    downloader.reset()
    downloader.download_range(date(2019,9,1), date(2019,12,31))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test()

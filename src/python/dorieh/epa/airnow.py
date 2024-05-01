"""
Python module to download EPA AirNow Data using WebServices API

https://docs.airnowapi.org/webservices

AirNow contains real-time up-to-date pollution data but is less reliable
than AQS

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

import logging
import os
from datetime import datetime

from dorieh.epa.airnow_downloader import AirNowDownloader
from dorieh.epa.airnow_ds_def import AirNowContext
from dorieh.platform import init_logging


class AirNow:
    """
    Main class
    """

    def __init__(self, context: AirNowContext = None):
        init_logging()
        if not context:
            context = AirNowContext(__doc__)
        self.context = context
        if self.context.destination is None:
            self.context.destination = os.curdir
        if self.context.shapes:
            for f in self.context.shapes:
                if not os.path.isfile(f):
                    raise ValueError(f)
        self.start = datetime.strptime(context.start_date, "%Y-%m-%d").date()
        self.end = datetime.strptime(context.end_date, "%Y-%m-%d").date()
        self.downloader = AirNowDownloader(context=self.context)

    def download(self):
        if self.context.reset:
            self.downloader.reset()
        self.downloader.download_range(self.start, self.end)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    downloader = AirNow()
    downloader.download()

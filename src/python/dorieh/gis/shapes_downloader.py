"""
A command line utility to download shapefiles

For details, see: `GISDownloader <downloader.html>`_
"""

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

import argparse

from dorieh.gis.constants import Geography
from dorieh.gis.downloader import GISDownloader, CensusShapeCollection


def download_shapes(year, geography: str, source: CensusShapeCollection):
    if geography == Geography.county.value:
        GISDownloader.download_county(year)
    elif geography == Geography.zip.value:
        raise ValueError("No known URL for zip code shapes. Consider using ZCTA or ESRI zip shape files.")
    elif geography == Geography.zcta.value:
        GISDownloader.download_zcta(source, year)
    elif geography == Geography.all.value:
        GISDownloader.download_shapes(source, year)
    else:
        raise ValueError("Unknown geography: " + geography)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", "-y", dest="year", type=int, required=True, help="Year")
    ap.add_argument("--geography", "--geo", "-g", required=True,
                    help="One of: " + ", ".join([
                        v.value for v in Geography
                    ])
                    )
    ap.add_argument("--collection", "-c", required=True,
                    help="One of: " + ", ".join([
                        v.value for v in CensusShapeCollection
                    ])
                    )
    args = ap.parse_args()
    c = {v.value: v for v in CensusShapeCollection}[args.collection]

    download_shapes(year=args.year, geography=args.geography, source=c)

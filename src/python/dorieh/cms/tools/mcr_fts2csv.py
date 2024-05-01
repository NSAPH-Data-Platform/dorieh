"""
Simple converter for CMS Medicare Fixed Width Format (FWF) files to CSV.
DOes not do any validation.
"""


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
import csv
import datetime
import gzip
import os
import sys

from dorieh.cms.fts2yaml import MedicareFTS, mcr_type
from dorieh.utils.fwf import FWFReader


def convert(fts_path: str):
    f, ext = os.path.splitext(fts_path)
    basedir, fname = os.path.split(f)
    t = mcr_type(fname)
    dat_path = f + ".dat"
    csv_path = f + ".csv.gz"

    fts = MedicareFTS(t).init(fts_path)
    t0 = datetime.datetime.now()
    with FWFReader(fts.to_fwf_meta(dat_path)) as reader,\
        gzip.open(csv_path, "wt") as out:
        writer = csv.writer(out)
        n = 0
        for record in reader:
            writer.writerow(record)
            n += 1
            if (n % 100000) == 0:
                print("{:,}: {}".format(n, str(datetime.datetime.now() - t0)))
    return


if __name__ == '__main__':
    convert(sys.argv[1])

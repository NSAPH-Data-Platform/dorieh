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
Abstract class to look for and process Medicare files from 1999 to 2010

These files are semi-processed files. For each year we have a denominator
(or patient summary, or enrollment) file and an inpatient admissions file.

Files are in SAS 7BDAT format.
"""


import glob
import logging

from abc import ABC, abstractmethod

import os

from typing import List


class MedicareSAS(ABC):
    """
    Abstract class to look for and process Medicare files from 1999 to 2010
    in SAS 7BDAT format
    """

    def __init__(self, root_dir:str = '.'):
        self.root_dir = root_dir

    def traverse(self, pattern: str):
        if isinstance(self.root_dir, list):
            dirs = self.root_dir
        else:
            dirs = [self.root_dir]
        files: List[str] = []
        for d in dirs:
            files.extend(glob.glob(os.path.join(d, pattern), recursive=True))
        for f in files:
            if f.endswith(".sas7bdat"):
                self.handle_sas_file(f)
            else:
                raise ValueError("Not implemented: " + f)
        return

    def handle_sas_file(self, f: str):
        basedir, fname = os.path.split(f)
        ydir, basedir = os.path.split(basedir)
        ydir = os.path.basename(ydir)
        if ydir not in fname:
            if "all_file" in fname and ydir.isdigit():
                logging.warning("No year: " + f)
            else:
                raise ValueError("Ambiguous year for " + f)
        year = int(ydir)
        if basedir == "denominator":
            table = "mcr_bene_{:d}".format(year)
        elif basedir == "inpatient":
            table = "mcr_ip_{:d}".format(year)
        else:
            raise ValueError("Unrecognized directory name for " + f)
        self.handle(table, f, basedir, year)
        return

    @abstractmethod
    def handle(self, table: str, file_path: str, file_type: str, year: int):
        pass

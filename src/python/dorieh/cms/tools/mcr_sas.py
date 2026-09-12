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
Abstract base class for processing semi-structured Medicare SAS files (1999–2010).

This class provides common traversal and filename-parsing logic to identify and
process Medicare data files stored in the SAS 7BDAT format.

These files are partially preprocessed and typically include:

Denominator (patient/enrollment) files
Inpatient admissions files
Subclasses must implement the abstract handle() method to specify file handling logic.

Typical usage:
- :class:~dorieh.cms.tools.sas_loader.SASLoader for data ingestion
- :class:~dorieh.cms.tools.sas_introspector.SASIntrospector for metadata extraction"""


import glob
import logging

from abc import ABC, abstractmethod

import os

from typing import List


class MedicareSAS(ABC):
    """
    Abstract base class for locating and processing Medicare SAS 7BDAT files
    in a specified directory

    This class handles:
    - Recursively locating SAS files matching given patterns
    - Determining file type and year from directory structure
    - Invoking subclass-defined logic for each discovered file

    Subclasses must implement:
        - handle(table, file_path, file_type, year): method to process each file.

    Attributes:
        root_dir (str or List[str]): Directory or list of directories containing data files.

    """

    def __init__(self, root_dir:str = '.'):
        """
        Initialize the MedicareSAS base class.

        Args:
            root_dir (str or List[str]): Root directory (or directories) containing SAS files.
                This can be a single directory as a string or a list of directories.
        """

        self.root_dir = root_dir

    def traverse(self, pattern: str):
        """
        Search for SAS files that match a glob-style pattern and process them.

        Uses recursive glob search from the root_dir(s), filtering by .sas7bdat extension,
        and passes matching files to self.handle_sas_file().

        Args:
            pattern (str): File search pattern (e.g., "[1-2]*/*/*.sas7bdat").
        """

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
        """
        Analyze the SAS file path to extract file type and year,
        then delegate the processing to subclass-defined handle() method.

        Args:
            f (str): Full path to the .sas7bdat file.

        Raises:
            ValueError: If file path does not contain a recognizable year or type.
        """

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
        """
        Abstract method to handle a single SAS 7BDAT file.

        This must be implemented by any subclass of MedicareSAS, and
        should define how a given SAS dataset is processed.

        Concrete classes override it to either generata database schema
        or perform data loading

        Args:
            table (str): Name of the table or logical target in the system.
            file_path (str): Full file path to the SAS file.
            file_type (str): Subtype or directory name used to classify the file (e.g., "inpatient", "denominator").
            year (int): Parsed year value inferred from directory name.
        """

        pass

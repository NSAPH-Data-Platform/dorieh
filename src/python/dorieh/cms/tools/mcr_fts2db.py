"""
Raw Data Loader for Medicare files provided by ResDac.
NSAPH Medicare pipeline uses this module for years 2011 and later.

This module defines a command-line utility to ingest raw Medicare data
delivered in File Transfer Summary (FTS) and fixed-width data (DAT) format,
as provided by ResDAC for years 2011 and later.

Overview:

Searches recursively for all FTS (``*.fts``) files under specified input path(s).
Parses each FTS file using the :class:`~dorieh.cms.fts2yaml.MedicareFTS` parser.
Determines the appropriate database schema and metadata for the associated ``*.dat`` or ``*.csv.gz`` file.
Loads data into the database using :class:`~dorieh.cms.mcr_data_loader.MedicareDataLoader`
for ``.dat`` files or a generic :class:`~dorieh.platform.loader.data_loader.DataLoader` for CSV files.
Applies indexing and VACUUM optimization after insertion

Usage Notes:

This loader requires that data be organized into year-based subfolders. For example: ``my_data/medicare/2018/*.fts``
The name of the parent directory of the FTS file must be a 4-digit year (e.g., 2011, 2018).
This requirement applies to both the data and FTS file location to establish table naming conventions correctly.
Key Components:

:class:`MedicareLoader` — orchestrates ingestion logic;
:class:`~dorieh.cms.mcr_data_loader.MedicareDataLoader` — fixed-width reader-based data loader;
:class:`~dorieh.platform.loader.data_loader.DataLoader` — generic CSV reader-based loader.


See also:

:doc:`/members/fts2yaml` — for metadata extraction from FTS;
:doc:`/members/mcr_data_loader` — for Medicare file reading;
:doc:`/members/medicare_yaml` — for generated schema definition.
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
import copy
import glob
import logging
import os
from typing import List

from dorieh.platform import init_logging
from dorieh.platform.loader.index_builder import IndexBuilder

from dorieh.cms.mcr_data_loader import MedicareDataLoader
from dorieh.cms.registry import Registry

from dorieh.cms.create_schema_config import CMSSchema

from dorieh.cms.fts2yaml import mcr_type
from dorieh.platform.loader.data_loader import DataLoader

from dorieh.platform.loader import LoaderConfig
from dorieh.platform.loader.vacuum import Vacuum


class MedicareLoader:
    """
    High-level loader for raw Medicare data files provided by ResDac, using FTS and DAT.

    The loader walks the input directory to locate all ``*.fts`` (File Transfer Summary) files,
    and for each one:

    - Parses its metadata and adds to the schema registry (YAML)
    - Identifies corresponding ``*.dat`` or ``*.csv.gz`` data files
    - Uses :class:`~dorieh.cms.mcr_data_loader.MedicareDataLoader` to load FWF files
        or :class:`~dorieh.platform.loader.data_loader.DataLoader` for CSV files
    - Applies schema-specific indexing and vacuum optimization

    This loader is compatible with ETL processing of Medicare data for 2011 and later.

    """

    @classmethod
    def process(cls):
        loader = MedicareLoader()
        loader.traverse(loader.pattern)

    def __init__(self):
        """
        Initializes MedicareLoader object with default CMS domain context.

        Sets the input pattern and prepares the LoaderConfig context, including
        root directory, flags like incremental/sloppy, and path normalization.
        """

        self.pattern = "**/*.fts"
        self.context = LoaderConfig(__doc__)
        self.context.domain = "cms"
        self.context.set_empty_args()
        self.root_dir=self.context.data
        self.context.data = [
            os.path.dirname(f) if os.path.isfile(f) else f
            for f in self.context.data
        ]
        if not self.context.incremental and not self.context.sloppy:
            self.context.reset = True
        return

    def traverse(self, pattern: str):
        """
        Searches directories recursively using the given pattern to find all FTS files.
        For each matching file, initiates schema inference and data ingestion via handle().

        :param pattern:    pattern (str): Glob pattern to match files (e.g., ``**/*.fts``)
        :return:
        """

        if isinstance(self.root_dir, list):
            dirs = self.root_dir
        else:
            dirs = [self.root_dir]
        files: List[str] = []
        for d in dirs:
            if os.path.isfile(d):
                files.append(d)
            else:
                files.extend(glob.glob(os.path.join(d, pattern), recursive=True))
        if len(files) == 0:
            self.handle_empty()
        for f in files:
            try:
                self.handle(f)
            except Exception as x:
                logging.exception("Error handling {}. Ignoring.".format(str(f)))
        return

    def handle_empty(self):
        """
        Handles the case where no FTS files are found.

        Creates an empty registry file (if not already present) and logs a message.
        """
        
        init_logging()
        logging.info("No files to process")
        if not os.path.exists(self.context.registry):
            with open(self.context.registry, "a") as r:
                r.write("# Empty\n")
        return 

    def handle(self, fts_path: str):
        """
        Loads a Medicare FTS/DAT or FTS/CSV pair into the database.

        - Extracts the year based on the immediate parent directory of the FTS file
        - Determines the file type from FTS file name
        - Updates the schema registry
        - Dispatches to the appropriate loader (.dat or .csv.gz)

        :param fts_path:  Full path to an FTS metadata file.

        Raises:
        ValueError: If year could not be inferred or data file is missing.
        """

        basedir, fname = os.path.split(fts_path)
        _, ydir = os.path.split(basedir)
        try:
            year = int(ydir)
        except:
            raise ValueError(
                "Immediate parent directory '{}' of {} was expected to be named"
                + " as 4 digit year (YYYY), e.g. 2011 or 2018"
                .format(ydir, fts_path)
            )
        f, ext = os.path.splitext(fts_path)
        ttype = mcr_type(fname)
        ctxt = CMSSchema(None,
                         path=self.context.registry,
                         inpt=fts_path,
                         tp= "medicare",
                         reset=False)
        reg = Registry(ctxt)
        reg.update()
        context = copy.deepcopy(self.context)
        context.table = "{}_{:d}".format(ttype, year)

        if os.path.isfile(f + ".csv.gz"):
            loader = self.loader_for_csv(context, f + ".csv.gz")
        elif glob.glob("{}*.dat".format(f)):  #os.path.isfile(f + ".dat"):
            loader = self.loader_for_fwf(context, fts_path)
        else:
            raise ValueError("Data file was not found: " + f)
        if self.context.dryrun:
            print("Dry run: " + fts_path)
        else:
            loader.run()
            IndexBuilder(context).run()
            Vacuum(context).run()

    @staticmethod
    def loader_for_csv(context: LoaderConfig, data_path: str) -> DataLoader:
        """
        Creates a generic DataLoader for a delimited CSV (usually .csv.gz) file.
        
        :param context:   Configuration object with metadata and paths
        :param data_path:   Path to the input CSV file
        :return:   Configured loader for tab-delimited CSV
        """

        context.pattern = [os.path.join("**", os.path.basename(data_path))]
        loader = DataLoader(context)
        loader.csv_delimiter = '\t'
        return loader

    @staticmethod
    def loader_for_fwf(context: LoaderConfig, fts_path: str) -> DataLoader:
        """
        Creates a MedicareDataLoader instance for a FTS/DAT file pair.

        :param context:  Configuration object with metadata and paths
        :param fts_path:  Path to the associated FTS metadata file
        :return: Loader ready to ingest fixed-width records
        """

        context.data = [fts_path]
        loader = MedicareDataLoader(context)
        return loader


if __name__ == '__main__':
    MedicareLoader.process()

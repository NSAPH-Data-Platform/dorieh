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
import glob
import os
from typing import List, Tuple, Any, Callable

from dorieh.cms.fts2yaml import mcr_type, MedicareFTS
from dorieh.platform.loader.data_loader import DataLoader
from dorieh.utils.fwf import FWFReader
from dorieh.utils.io_utils import fopen


class MedicareDataLoader(DataLoader):
    """
    MedicareDataLoader is a specialized subclass of :class:`~dorieh.platform.loader.data_loader.DataLoader`
    that handles ingestion of raw Medicare CMS files accompanied by FTS (File Transfer Summary) metadata.

    This loader is designed to read data using file specifications included in FTS files provided by ResDAC.
    It supports fixed-width (.dat) raw data files where metadata is embedded in a parallel .fts file.

    Functional Responsibilities:
    - Resolves (*.fts) File Transfer Summary files to their corresponding data (*.dat) files
    - Parses FTS files using :class:`~dorieh.cms.fts2yaml.MedicareFTS`
    - Creates an :class:`~dorieh.utils.fwf.FWFReader` for reading fixed-width data using inferred column schema
    - Integrates with the context-configurable data loading pipeline via :class:`~dorieh.platform.loader.data_loader.DataLoader`

    Attributes:
        context (LoaderConfig): Configuration object carrying paths and settings for ingestion.

    Example Usage:
        loader = MedicareDataLoader(context)
        loader.run()

    See Also:
        - :class:`~dorieh.cms.fts2yaml.MedicareFTS`
        - :class:`~dorieh.utils.fwf.FWFReader`
        - :class:`~dorieh.platform.loader.data_loader.DataLoader`
    """

    @classmethod
    def dat4fts(cls, fts_path):
        """
         Given a path to an FTS metadata file, finds all matching .dat data files.

         The .dat files are expected to match the FTS filename prefix.

        :param fts_path:  Path to a .fts metadata file.
        :return:  List[str]: List of full paths to .dat files that correspond to the FTS file.
        """

        f, ext = os.path.splitext(fts_path)
        assert ext.lower() == '.fts'
        data_files = glob.glob("{}*.dat".format(f))
        return data_files

    @classmethod
    def open(cls, name: str, dat_path: str = None) -> FWFReader:
        """
        Opens a fixed-width reader for a Medicare file using both the FTS (metadata)
        and .dat (data) input files.

        Given either a .fts or .dat path (or the base file name), this method builds
        the appropriate pairing of FTS and DAT files, parses the metadata, and returns
        a FWFReader for iterating over the structured data rows.

        :param name:  Path to either the .fts or .dat file, or a base file path without extension.
        :param dat_path:  If provided, explicitly sets .dat file path to use.
        :return: A reader instance for parsing the structured fixed-width file.

        Raises:
        AssertionError: If provided file has an invalid or unsupported extension.
        ValueError: If file type cannot be determined from file name.
 
        """

        f, ext = os.path.splitext(name)
        if dat_path is not None:
            assert ext.lower() == '.fts'
            fts_path = name
        elif ext.lower() == ".fts":
            fts_path = name
            dat_path = f + ".dat"
        elif ext.lower() == ".dat":
            dat_path = name
            fts_path = f + ".fts"
        else:
            dat_path = name + ".dat"
            fts_path = name + ".fts"
        basedir, fname = os.path.split(f)
        t = mcr_type(fname)
        fts = MedicareFTS(t).init(fts_path)
        return FWFReader(fts.to_fwf_meta(dat_path))

    def __init__(self, context):
        """
        Initializes a MedicareDataLoader with the given context.

        :param context: A configuration object used by the data loading pipeline.
        """

        super().__init__(context)

    def get_files(self) -> List[Tuple[Any, Callable]]:
        """
        Resolves all FTS-to-DAT file pairs from the configured context data path,
        and returns a list of reader objects paired with file-open functions.

        This function provides the loading pipeline with all reader instances needed
        to load fixed-width Medicare data records.

        :return:  A list of reader/open-function pairs for streaming data.
        """

        objects = []
        for fts_path in self.context.data:
            dat_files = self.dat4fts(fts_path)
            for dat_file in dat_files:
                objects.append((self.open(fts_path, dat_file), fopen))
        return objects


if __name__ == '__main__':
    loader = MedicareDataLoader(None)
    loader.run()

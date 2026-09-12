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
This module defines an introspector for SAS 7BDAT files related to Medicare data.

The SASIntrospector class crawls a directory for SAS files matching a pattern,
extracts metadata (column info), and generates data model definitions in YAML format.
These models are written to a centralized registry.

Typical use case: building data models from Medicare SAS files (e.g., 1999–2010).

See Also:
- :class:`.SASIntrospector` (this class)
- :class:`.MedicareSAS` (superclass)
- :class:`~dorieh.platform.loader.introspector.Introspector`
- :class:`~dorieh.cms.tools.mcr_registry.MedicareRegistry`
"""

import logging
import re
import sys
from typing import List
import yaml

from dorieh.cms.tools.mcr_registry import MedicareRegistry
from dorieh.cms.tools.mcr_sas import MedicareSAS

from dorieh.platform.data_model.utils import split
from dorieh.platform.loader.introspector import Introspector
from dorieh.platform.pg_keywords import PG_INT_TYPE, PG_SERIAL_TYPE


class SASIntrospector(MedicareSAS, MedicareRegistry):
    """
    This class traverses a file path looking for SAS .sas7bdat files,
    extracts their schema using :class:`~dorieh.platform.loader.introspector.Introspector`,
    and creates a structured data model serialized to a YAML registry.

    In addition to field-level metadata, this introspector:
    - Attempts to identify common fields such as bene_id, state, zip, and year
    - Automatically generates a year column if missing
    - Marks special fields as indexed
    - Adds virtual key fields for file and record identifiers

    Inherits from:
        MedicareSAS: For file traversal and handling utilities
        MedicareRegistry: For interacting with the data model YAML registry
    """

    @classmethod
    def process(cls, registry_path: str, pattern: str, root_dir: str = '.'):
        """
        Entry point that initializes and runs the introspector.

        Args:
            registry_path (str): Path to output YAML registry file.
            pattern (str): Glob-like pattern to match .sas7bdat files.
            root_dir (str): Root directory to start searching. Default is current directory.
        """
        
        introspector = SASIntrospector(registry_path, root_dir)
        introspector.traverse(pattern)
        introspector.save()
        yaml.dump(introspector.registry, sys.stdout)
        return

    def __init__(self, registry_path: str, root_dir: str = '.'):
        """
        Initializes the SASIntrospector with the given registry path and SAS root directory.

        Args:
            registry_path (str): Path to the YAML registry file.
            root_dir (str): Base directory for SAS 7BDAT files.
        """

        MedicareSAS.__init__(self, root_dir)
        MedicareRegistry.__init__(self, registry_path)

    @classmethod
    def matches(cls, s: str, candidates: List[str]):
        """
        Determines whether a string matches any string or wildcard pattern in candidates.

        Args:
            s (str): String to match.
            candidates (List[str]): List of exact names or patterns (may include `*`).

        Returns:
            bool: True if s matches any candidate.
        """
        
        if s in candidates:
            return True
        patterns = [c.replace('*', '.*') for c in candidates if '*' in c]
        for p in patterns:
            if re.fullmatch(p, s):
                return True
        return False

    def handle(self, table: str, file_path: str, file_type: str, year: int):
        """
        Handles metadata extraction for a single .sas7bdat file.

        Args:
            table (str): Target table name to use in the registry.
            file_path (str): File path to the SAS data file.
            file_type (str): Type of file (e.g., 'denominator').
            year (int): Associated year of data.
        """

        if file_type == "denominator":
            index_all = True
        else:
            index_all = False
        self.add_sas_table(table, file_path, index_all, year)
        return

    def add_sas_table(self, table: str, file_path: str, index_all: bool,
                      year: int):
        """
        Extracts schema from a SAS file and registers columns into the YAML registry.

        - Uses introspection to extract columns and attach metadata.
        - Detects and indexes key columns (e.g., bene_id, state, year).
        - Auto-generates a 'year' column if missing using a virtual GENERATED column.
        - Indexes all columns if index_all is True (e.g., for denominator files).
        - Adds FILE and RECORD fields to simulate full uniqueness using a compound PK.

        Args:
            table (str): Name of the table in the registry.
            file_path (str): Path to the SAS file.
            index_all (bool): Whether all fields should be indexed.
            year (int): Year to use when generating missing year columns.

        Raises:
            ValueError: If duplicate key fields are detected or mandatory fields are missing.
        """

        introspector = Introspector(file_path)
        introspector.introspect()
        introspector.append_file_column()
        introspector.append_record_column()
        columns = introspector.get_columns()
        specials = {
            "bene_id":  (None, ["bene_id", "intbid", "qid", "bid_5333*"]),
            "state":  (None, ["state", "ssa_state", "state_code",
                              "bene_rsdnc_ssa_state_cd", "state_cd",
                              "medpar_bene_rsdnc_ssa_state_cd"]),
            "zip": (None, ["zip", "zipcode", "bene_zip_cd", "bene_zip",
                           "bene_mlg_cntct_zip_cd",
                           "medpar_bene_mlg_cntct_zip_cd"]),
            "year": (None, ["year", "enrolyr", "bene_enrollmt_ref_yr",
                            "rfrnc_yr"])
        }
        for column in columns:
            cname, c = split(column)
            if cname == "year":
                yc = cname
            is_key = False
            for key in specials:
                key_column, candidates = specials[key]
                if self.matches(cname, candidates):
                    if key_column is not None:
                        raise ValueError("Multiple {} columns in {}"
                                         .format(key, file_path))
                    specials[key] = (column, candidates)
                    is_key = True
            if index_all and not is_key:
                c["index"] = "true"

        for key in specials:
            column, _ = specials[key]
            if column is None:
                if key == "year":
                    columns.append(
                        {
                            key: {
                                "type": PG_INT_TYPE,
                                "index": True,
                                "source": {
                                    "type": "generated",
                                    "code": "GENERATED ALWAYS AS ({:d}) STORED"
                                        .format(year)
                                }
                            }
                        }
                    )
                    logging.warning("Generating year column for " + file_path)
                    continue
                raise ValueError("No {} column in {}".format(key, file_path))
            cname, c = split(column)
            if key == cname:
                c["index"] = "true"
                continue
            columns.append(
                {
                    key: {
                        "type": c["type"],
                        "index": True,
                        "source": {
                            "type": "generated",
                            "code": "GENERATED ALWAYS AS ({}) STORED"
                                .format(cname)
                        }
                    }
                }
            )
        
        self.registry[self.domain]["tables"][table] = {
            "columns": columns,
            "primary_key": [
                "FILE",
                "RECORD"
            ]
        }


if __name__ == '__main__':
    SASIntrospector.process(*sys.argv[1:])
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
Introspector that looks for all SAS 7BDAT files in a given path
matching a given pattern, reads metadata and generates data model
for each file in YAML format. the data model is written to the common
registry.
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
    Introspector that looks for all SAS 7BDAT files in a given path
    matching a given pattern, reads metadata and generates data model
    for each file in YAML format. the data model is written to the common
    registry.
    """

    @classmethod
    def process(cls, registry_path: str, pattern: str, root_dir:str = '.'):
        introspector = SASIntrospector(registry_path, root_dir)
        introspector.traverse(pattern)
        introspector.save()
        yaml.dump(introspector.registry, sys.stdout)
        return

    def __init__(self, registry_path: str, root_dir: str = '.'):
        MedicareSAS.__init__(self, root_dir)
        MedicareRegistry.__init__(self, registry_path)

    @classmethod
    def matches(cls, s: str, candidates: List[str]):
        if s in candidates:
            return True
        patterns = [c.replace('*', '.*') for c in candidates if '*' in c]
        for p in patterns:
            if re.fullmatch(p, s):
                return True
        return False

    def handle(self, table: str, file_path: str, file_type: str, year: int):
        if file_type == "denominator":
            index_all = True
        else:
            index_all = False
        self.add_sas_table(table, file_path, index_all, year)
        return

    def add_sas_table(self, table: str, file_path: str, index_all: bool,
                      year: int):
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
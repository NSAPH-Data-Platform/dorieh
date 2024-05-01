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
Loader looks for SAS 7BDAT files in a given path
matching a given pattern and loads the data in the database.

Used for 1999 to 2010 years
"""

import copy
import os

from dorieh.platform.loader.data_loader import DataLoader

from dorieh.cms.tools.mcr_sas import MedicareSAS
from dorieh.platform.loader import LoaderConfig


class SASLoader(MedicareSAS):
    """
    Loader looks for SAS 7BDAT files in a given path
    matching a given pattern and loads the data in the database.

    Used for 1999 to 2010 years
    """

    @classmethod
    def process(cls):
        loader = SASLoader()
        loader.traverse(loader.pattern)

    def __init__(self):
        self.pattern = "[1-2]*/*/*.sas7bdat"
        self.context = LoaderConfig(__doc__)
        self.context.domain = "cms"
        self.domain = self.context.domain
        self.context.set_empty_args()
        super().__init__(
            root_dir=self.context.data
        )
        if not self.context.incremental and not self.context.sloppy:
            self.context.reset = True
        return

    def handle(self, table: str, file_path: str, file_type: str, year: int):
        context = copy.deepcopy(self.context)
        context.table = table
        context.pattern = [os.path.join("**", os.path.basename(file_path))]
        loader = DataLoader(context)
        loader.run()


if __name__ == '__main__':
    SASLoader.process()



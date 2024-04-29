"""
A reader for `FST files <https://www.fstpackage.org/>`_
providing the same
interface as `CSV reader <https://docs.python.org/3/library/csv.html>`_.


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

import datetime
from typing import Optional

try:
    import rpy2.robjects as robjects
    import rpy2.robjects.packages as rpackages
    from rpy2.rinterface import NULL
    from rpy2.robjects import DataFrame
    from rpy2.robjects.vectors import DateVector


    EPOCH = datetime.date(year=1970, month=1, day=1).toordinal()


    def choose_cran_mirror():
        utils = rpackages.importr('utils')
        #mirrors = utils.getCRANmirrors()
        utils.chooseCRANmirror(ind=1)
        return utils


    def ensure_packages():
        utils = choose_cran_mirror()
        packages = ["fst"]
        for p in packages:
            if not rpackages.isinstalled(p):
                utils.install_packages(p)
            rpackages.importr(p)
        return


    def read_fst(path: str, start=1, end=None) -> (DataFrame, bool):
        ensure_packages()
        f = robjects.r["read_fst"]
        if start != 1 or end is not None:
            df = f(path, NULL, start, end)
            if end is None:
                complete = True
            elif df.nrow <= (end - start):
                complete = True
            else:
                complete = False
        else:
            df = f(path)
            complete = True
        return df, complete


    def vector2list(v):
        if DateVector.isrinstance(v):
            return [datetime.date.fromordinal(EPOCH + int(d)) if d == d else None for d in v]
        return list(v)


    class FSTReader:
        """
        Class providing CSV-like interface for FST files
        """

        def __init__(self, path, buffer_size = 10000, returns_mapping = False):
            if not path.endswith(".fst"):
                raise Exception("Unknown format of file " + path)
            self.path = path
            self.buffer_size = buffer_size
            self.columns = None
            self.pointer = 1
            self.last = 0
            self.first = 0
            self.complete = False
            self.returns_mapping = returns_mapping

        def read_next(self):
            self.first = self.pointer
            end = self.first + self.buffer_size - 1
            df, self.complete = read_fst(self.path, self.first, end)
            self.last = self.pointer + df.nrow
            self.columns = {
                df.colnames[c]: vector2list(df[c]) for c in range(df.ncol)
            }

        def current(self) -> Optional[int]:
            if self.pointer >= self.last:
                if self.complete:
                    return None
                self.read_next()
                if self.pointer >= self.last:
                    return None
            return self.pointer - self.first

        def current_row(self) -> Optional[list]:
            r = self.current()
            if r is None:
                return None
            row = [
                self.columns[column][r] for column in self.columns
            ]
            return row

        def current_mapping(self) -> Optional[dict]:
            r = self.current()
            if r is None:
                return None
            row = {
                column: self.columns[column][r] for column in self.columns
            }
            return row

        def __next__(self):
            if self.returns_mapping:
                row = self.current_mapping()
            else:
                row = self.current_row()
            if row is None:
                raise StopIteration()
            self.pointer += 1
            return row

        def close(self):
            self.columns = None
            self.pointer = -1
            self.complete = True

        def rewind(self):
            if self.pointer == 1:
                return
            self.pointer = 1
            self.read_next()

        def open(self):
            self.rewind()
            self.read_next()

        def __enter__(self):
            self.open()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.close()

        def __iter__(self):
            return self
except:
    class FSTReader:
        def __int__(self):
            raise NotImplementedError("FSTReader requires R environment")

### END

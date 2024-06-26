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

import glob
import os
from abc import ABC
from pathlib import Path

import sys
from typing import Iterable, Callable

from dorieh.utils.io_utils import is_yaml_or_json, is_dir
from psycopg2.extensions import connection

from dorieh.platform import init_logging, app_name
from dorieh.platform.data_model.domain import Domain
from dorieh.platform.loader.common import CommonConfig
from dorieh.platform.db import Connection
from dorieh.platform.loader.loader_config import LoaderConfig
from dorieh.platform.loader.monitor import DBActivityMonitor


def diff(files: Iterable[str]) -> bool:
    """
    Given a list of files, check if they are all identical

    :param files: a list of files
    :return: True if all files in the list are identical one to another
    """

    ff = list(files)
    for i in range(len(ff) - 1):
        ret = os.system("diff {} {}".format(ff[i], ff[i+1]))
        if ret != 0:
            return False
    return True


class LoaderBase(ABC):
    """
    Base class for tools responsible for data loading and processing
    """

    @classmethod
    def find_file_in_path(cls, fname: str):
        files = set()
        for d in sys.path:
            files.update(glob.glob(
                os.path.join(d, "**", fname),
                recursive=True
            ))
        if not files:
            raise ValueError("File {} not found".format(fname))
        if len(files) > 1:
            if not diff(files):
                raise ValueError("Ambiguous files {}".format(';'.join(files)))
        return  files.pop()

    @classmethod
    def get_domain(cls, name: str, registry: str = None) -> Domain:
        src = None
        registry_path = None
        if registry:
            if is_yaml_or_json(registry):
                if os.path.dirname(registry) or os.path.exists(registry):
                    registry_path = os.path.abspath(registry)
                else:
                    registry_path = cls.find_file_in_path(registry)
                if not os.path.isfile(registry_path):
                    raise ValueError("{} - is not a file".format(registry_path))
            elif not is_dir(registry):
                raise ValueError("{} - is not a valid registry path".format(registry))
            elif os.path.isdir(registry):
                src = registry
            else:
                raise NotImplementedError("Not Implemented: registry in an archive")
        if not src:
            src = Path(__file__).parents[3]
        if not registry_path:
            registry_path = os.path.join(src, "yml", name + ".yaml")
        if not os.path.isfile(registry_path):
            registry_path = cls.find_file_in_path(name + ".yaml")
        if not os.path.isfile(registry_path):
            raise ValueError("File {} does not exist".format(os.path.abspath(registry_path)))
        domain = Domain(registry_path, name)
        return domain

    def __init__(self, context: LoaderConfig):
        app = app_name()
        if context.table:
            name = context.table + '-' + app
        else:
            name = app
        init_logging(name=app)
        self.context = None
        self.domain = self.get_domain(context.domain, context.registry)
        if isinstance(context, LoaderConfig) and context.sloppy:
            self.domain.set_sloppy()
        self.domain.init()
        self.table = context.table
        self.monitor = DBActivityMonitor(context)
        self.exception = None

    def _connect(self) -> connection:
        c = Connection(self.context.db, self.context.connection)\
            .connect(self.context.autocommit)
        return c

    def get_pid(self, connxn: connection) -> int:
        with connxn.cursor() as cursor:
            cursor.execute("SELECT pg_backend_pid()")
            for row in cursor:
                return row[0]

    def execute_with_monitor(self,
                             what: Callable,
                             connxn: connection = None,
                             on_monitor: Callable = None):
        if not on_monitor:
            pid = self.get_pid(connxn)
            on_monitor = lambda: self.monitor.log_activity(pid)
        try:
            DBActivityMonitor.execute(what, on_monitor)
        except Exception as x:
            self.exception = x



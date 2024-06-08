#  Copyright (c) 2024. Harvard University
#
#  Developed by Research Software Engineering,
#  Harvard University Research Computing and Data (RCD) Services.
#
#  Author: Michael A Bouzinier
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#           http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
import logging
import sys

from psycopg2.extensions import connection

from dorieh.platform.db import Connection
from dorieh.platform.loader.monitor import DBActivityMonitor


def sleep(cnxn: connection, seconds: int = 100):
    """
    Runs a dummy process in a database for specified number of seconds using
    connection provided

    :param cnxn: Connection object, connected to PostgreSQL database
    :param seconds: number of seconds for the process to run
    :return:
    """

    with (cnxn.cursor()) as cursor:
        cursor.execute(f"SELECT pg_sleep({seconds})")


def get_pid(cnxn: connection) -> int:
    """
    Obtains the process id for a given connection

    :param cnxn: Connection object, connected to PostgreSQL database
    :return:  process id (it is both a unix prcoess id and PostgreSQL process id)
    """

    with cnxn.cursor() as cursor:
        cursor.execute("SELECT pg_backend_pid()")
        for row in cursor:
            return row[0]


def execute_with_monitor ():
    monitor = DBActivityMonitor()
    db_ini = monitor.context.db
    connection_name = monitor.context.connection
    with Connection(db_ini, connection_name) as cnxn:
        pid = get_pid(cnxn)
        callback = lambda: monitor.log_activity(pid)
        process = lambda: sleep(cnxn, 100)
        DBActivityMonitor.execute(process, callback)
    print("Process finished")


if __name__ == '__main__':
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    logging.basicConfig(level=logging.DEBUG, handlers = [handler])
    execute_with_monitor()


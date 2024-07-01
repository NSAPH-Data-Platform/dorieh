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

"""
Script to generate .pgpass file from database.ini
"""
import sys
from configparser import ConfigParser

from dorieh.platform.db import Connection


def main():
    dbf = sys.argv[1]
    parser = ConfigParser()
    parser.read(dbf)

    for section in parser.sections():
        print(f"Processing {section}")
        parameters = Connection.read_config(dbf, section)
        with open(".pgpass", "a") as pgpass:
            hostname = parameters["host"]
            port = parameters.get("port", "*")
            database = parameters["database"]
            username = parameters["user"]
            password = parameters["password"]
            line = f"{hostname}:{port}:{database}:{username}:{password}"
            print(line, file=pgpass)
    return


if __name__ == '__main__':
    main()

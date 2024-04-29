#  Copyright (c) 2024.  Harvard University
#
#   Developed by Research Software Engineering,
#   Harvard University Research Computing and Data (RCD) Services.
#
#   Author: Michael A Bouzinier
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#
import os

import psutil


def mem() -> int:
    mem_info = psutil.Process(os.getpid()).memory_full_info()
    if hasattr(mem_info, "uss"):
        m = mem_info.uss
    else:
        m = mem_info.rss
    return m


def qmem() -> int:
    return psutil.Process(os.getpid()).memory_info().rss

def qqmem(pid) -> int:
    return psutil.Process(pid).memory_info().rss


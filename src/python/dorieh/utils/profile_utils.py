"""
Shortcuts to get currently allocated memory in bytes
"""


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
    """
    Returns currently allocated memory using
    `full memory info <https://psutil.readthedocs.io/en/latest/#psutil.Process.memory_full_info>`_.

    When `uss` aka “Unique Set Size”, is available then this function returns the value of uss.
    USS is the memory which is unique to a process and which would be freed if the process was terminated right now.

    If `uss` is unavailable it returns the `pss`, aka “Proportional Set Size”,
    is the amount of memory shared with other processes, accounted in a way that
    the amount is divided evenly between the processes that share it.
    I.e., if a process has 10 MBs all to itself and 10 MBs shared with another process its PSS will be 15 MBs.

    This function might be slower than `qmem()`

    :return: currently allocated memory in bytes
    """

    mem_info = psutil.Process(os.getpid()).memory_full_info()
    if hasattr(mem_info, "uss"):
        m = mem_info.uss
    else:
        m = mem_info.rss
    return m


def qmem() -> int:
    """
    Quickly return currently allocated memory in bytes.
    This function returns rss, “Resident Set Size”, this is the non-swapped physical
    memory a process has used. On UNIX it matches “top“‘s RES column).

    :return: currently allocated memory in bytes
    """

    return psutil.Process(os.getpid()).memory_info().rss


def qqmem(pid) -> int:
    """
    Quickly return currently allocated memory in bytes given the process id.
    This function does not call `os.getpid()` and therefore, might be faster than `qmem()`.
     
    This function returns rss, “Resident Set Size”, this is the non-swapped physical
    memory a process has used. On UNIX it matches “top“‘s RES column).

    :param pid:
    :return: currently allocated memory in bytes
    """

    return psutil.Process(pid).memory_info().rss


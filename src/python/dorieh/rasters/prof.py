"""
Python class used to store profiling data to profile spatial aggregation
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
import logging
from datetime import timedelta
from typing import Optional

from dorieh.utils.io_utils import sizeof_fmt

from dorieh.utils.profile_utils import mem


class ProfilingData:
    def __init__(self):
        self.max_mem = mem()
        '''Maximum memory used during the execution'''

        self.factor = 1
        self.shape_x = 0
        self.shape_y = 0
        self.total_time = timedelta(0)
        self.core_time = timedelta(0)

    def update_mem_only(self, m: int):
        """
        Updates `max_mem` if the argument passed is greater than the current value.

        :param m: Currently used memory, presumably returned by the last called function or procedure
        :return:
        """

        if m > self.max_mem:
            self.max_mem = m

    def update_mem_time(self, m: int,
                        t: Optional[timedelta],
                        t0: timedelta = None):
        """
        Updates `max_mem` and time values. Memory is updated if the provided value is greater
        than current maximum, times (when provided) are added to the stored values.

        :param m:  Currently used memory, presumably returned by the last called function or procedure
        :param t:  total time used by a step, including wait time
        :param t0: "core" time used by a step, presumably, CPU time
        :return:
        """


        self.update_mem_only(m)
        if t is not None:
            self.total_time += t
        if t0 is not None:
            self.core_time += t0
        return

    def update(self, other):
        """
        This method is presumably called after a sub-procedure that collects its own
        profiling data is executed.

        :param other:  an instance of `ProfilingData` returned by sub-procedure
        :return:
        """

        if not isinstance(other, ProfilingData):
            raise ValueError(f"Instance of {self.__class__} expected")
        self.update_mem_time(other.max_mem, other.total_time, other.core_time)
        if other.factor > self.factor:
            self.factor = other.factor
        if other.shape_x > self.shape_x:
            self.shape_x = other.shape_x
        if other.shape_y > self.shape_y:
            self.shape_y = other.shape_y
        return

    def log(self, msg):
        """
        Logs currently available profiling data with a given message.
        Logs using current logger with INFO level.

        :param msg: A message to prepend to the data
        :return:
        """

        fmt = ("factor: %d ; shape: %d x %d ; aggr time: %s ; time: %s ;"
               + " memory: %d (%s)")
        logging.info(
            msg + fmt,
            self.factor,
            self.shape_x,
            self.shape_y,
            self.core_time,
            self.total_time,
            self.max_mem,
            sizeof_fmt(self.max_mem)
        )

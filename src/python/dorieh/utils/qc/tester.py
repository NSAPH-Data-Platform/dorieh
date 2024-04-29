"""
Generic object for testing for data quality issues.

Tester class contains list of tests to run on data. Tests contain a variable name, a condition, and a severity
"""

#  Copyright (c) 2021. Harvard University
#
#  Developed by Research Software Engineering,
#  Faculty of Arts and Sciences, Research Computing (FAS RC)
#  Author: Ben Sabath
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

from enum import Enum, auto
import pandas as pd
import numpy as np
import yaml
import logging


class Condition(Enum):

    less_than = "lt"
    greater_than = "gt"
    data_type = "dtype"
    no_missing = "no_nan"
    count_missing = "count_nan"


class Severity(Enum):

    debug = logging.DEBUG
    info = logging.INFO
    warning = logging.WARNING
    error = logging.ERROR
    critical = logging.CRITICAL

class ExpectationError(Exception):
    """
    Error for when an expected value to a condition cannot be valid
    """
    pass


class Test:

    def __init__(self, variable, condition, severity, val=None, name=None, logger = None):
        self.variable = variable
        self.condition = condition
        self.val = val
        """
        Value to compare against, can be excluded for a ``no_missing`` check
        """
        self.severity = severity
        self.name = name

        if not name:
            self.name = self.variable + "_" + self.condition.value
            if self.val:
                self.name += "_" + str(self.val)

        if logger:
            self.__logger = logger
        else:
            self.__logger = logging.getLogger(__name__ + ".Test." + self.name)

        self._validate_test()
        self.expectation = self._construct_expectation()


    def _validate_test(self):
        """
        Confirm that inputs define a valid test
        :return:
        """
        if self.condition == Condition.count_missing and self.val < 0:
            raise ExpectationError(self.name + ": Count Missing conditions must expect at least 0 missing rows")

    def _construct_expectation(self):
        """
        Phrase test expectation in words
        :return: str
        """
        out = ""
        out += self.name + ":" + self.severity.name + ": " + "For variable " + self.variable + ": "

        if self.condition == Condition.count_missing:
            if 0 < self.val < 1:
                out += "less than " + "%2.2f" % (self.val * 100) + "% missing"
            else:
                out += "less than " + str(self.val) + " values missing"
        elif self.condition == Condition.no_missing:
            out += "no missing values"
        elif self.condition == Condition.data_type:
            out += "all values are " + self.val
        elif self.condition == Condition.greater_than:
            out += "all values greater than " + str(self.val)
        elif self.condition == Condition.less_than:
            out += "all values less than " +str(self.val)

        return out



    def check(self, df: pd.DataFrame):
        """
        Check variable of input dataframe to see if it meets conditions

        :param df: Pandas data frame
        :return: boolean of if the data passed the test
        """

        message = None
        result = None

        if self.condition == Condition.count_missing:
            count = sum(np.isnan(df[self.variable]))
            if 1 > self.val > 0:
                # assume expectation is a %age
                result = count/len(df.index) < self.val
                if not result:
                    message = self.expectation + ". " + "%2.2f" % (count/len(df.index) * 100) + \
                              "% missing values observed for " + self.variable
            else:
                result = count < self.val
                if not result:
                    message = self.expectation + ". " + str(count) + \
                              " missing values observed for " + self.variable

        elif self.condition == Condition.data_type:
            result = type(df.loc[0, self.variable]).__name__ == self.val

        else:
            if self.condition == Condition.less_than:
                count = sum(df[self.variable] > self.val)
            elif self.condition == Condition.greater_than:
                count = sum(df[self.variable] < self.val)
            elif self.condition == Condition.no_missing:
                count = sum(np.isnan(df[self.variable]))

            result = count == 0

            if not result:
                message = self.expectation + ". check failed. " + "%2.2f" % (count/len(df.index) * 100) + \
                          "% of observations with invalid values."

        if message:
            self.__logger.log(self.severity.value, message)
        return result


class Tester:

    def __init__(self, name, yaml_file=None):
        self.name = name
        self._logger = logging.getLogger(__name__ + ".Tester." + self.name)
        self.tests = []
        if yaml_file:
            self.load_yaml(yaml_file)

    def add(self, t: Test):
        self.tests.append(t)

    def load_yaml(self, yaml_file):
        with open(yaml_file) as f:
            test_list = yaml.load(f, Loader=yaml.FullLoader)

        for item in test_list:
            item['condition'] = Condition[item['condition']]
            item['severity'] = Severity[item['severity']]
            item['logger'] = self._logger
            self.add(Test(**item))

    def check(self, df: pd.DataFrame):
        out = True
        num_tests = 0
        num_failures = 0
        for t in self.tests:
            num_tests += 1
            result = t.check(df)
            out = out and result
            if not result:
                num_failures += 1

        passes = num_tests - num_failures
        self._logger.info("All Tests Completed. Out of " + str(num_tests) + " tests: " +
                          str(passes) + " passed and " + str(num_failures) + " failed.")
        return out

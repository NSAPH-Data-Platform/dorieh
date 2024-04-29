"""
Utilities to create context and configuration objects
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

import argparse
import datetime
from enum import Enum
from typing import List


class Cardinality(Enum):
    """
    Cardinality of a configuration parameter: multiple or singular
    """

    single = "single"
    multiple = "multiple"


class Argument:
    """
    A wrapper class to describe a command-line arguments
    This is practically, a more rigid format for
    :func ArgumentParser.add_argument:
    """

    def __init__(self, name,
                 help: str,
                 type = str,
                 aliases: List = None,
                 default = None,
                 cardinality: Cardinality = Cardinality.single,
                 valid_values = None,
                 required = True
                 ):
        """
        All arguments are passed to Argparser

        :param name:
        :param help:
        :param type:
        :param aliases:
        :param default:
        :param cardinality:
        :param valid_values:
        """

        if aliases is None:
            aliases = []
        self.name = name
        self.type = type
        self.aliases = aliases
        if self.type == bool and default is None:
            self.default = False
        else:
            self.default = default
        self.cardinality = cardinality
        self.description = help
        self.choices = valid_values
        self.required_flag = self.default is None and required

        return

    def get_action(self):
        if self.type == bool:
            if not self.default:
                return 'store_true'
            return 'store_false'
        return None

    def get_nargs(self):
        if self.cardinality == Cardinality.single:
            return None
        if self.default:
            return '*'
        return '+'

    def get_help(self):
        if not self.is_required():
            h = self.description
            if h.strip() and h.strip()[-1] not in {'.', ','}:
                h += ', '
            h += "default: " + str(self.default)
            return h
        return self.description

    def is_required(self):
        return self.required_flag

    def add_to(self, parser):
        args = ["--" + self.name]
        for alias in self.aliases:
            if len(alias) == 1:
                args.append("-" + alias)
            else:
                args.append("--" + alias)

        action = self.get_action()
        nargs = self.get_nargs()
        kwargs = {
            "default": self.default,
            "help": self.get_help(),
            "required": self.is_required()
        }
        if action:
            kwargs['action'] = action
        else:
            kwargs["type"] = self.type
        if nargs:
            kwargs['nargs'] = nargs
        if self.choices:
            kwargs["choices"] = self.choices
        parser.add_argument(*args, **kwargs)

    def __str__(self):
        return "--" + self.name


class Context:
    """
    Generic class allowing to build context and configuration objects
    and initialize them using command line arguments
    """

    _years = Argument("years", help="""
         Year or list of years to download. For example, 
         the following argument: 
         `-y 1992:1995 1998 1999 2011 2015:2017` will produce 
         the following list: 
         [1992,1993,1994,1995,1998,1999,2011,2015,2016,2017]
    """,
                     aliases=['y'],
                     cardinality=Cardinality.multiple,
                     default="1990:{}".format(datetime.date.today().year),
                     )
    _compress = Argument("compress",
                         aliases=['c'],
                         cardinality=Cardinality.single,
                         type=bool,
                         default=True,
                         help="Use gzip compression for the result")

    def __init__(self, subclass,
                 description = None,
                 include_default: bool = True):
        """
        Creates a new object

        :param subclass: A concrete class containing configuration information
            Configuration options must be defined as class memebers with names,
            starting with one '_' characters and values be instances of
            :class Argument:
        :param description: Optional text to use as description.
            If not specified, then it is extracted from subclass documentation
        """

        self.arguments = None
        if include_default:
            self.years = None
            """
             Year or list of years to download. For example, 
             the following argument: 
             `-y 1992:1995 1998 1999 2011 2015:2017` will produce 
             the following list: 
             [1992,1993,1994,1995,1998,1999,2011,2015,2016,2017]
            """
            self.compress = None
            '''Specifies whether to use gzip compression for the result'''

        if description:
            self.description = description
        else:
            self.description = subclass.__doc__

        self._attrs = [
            field_name[1:] for field_name, field in subclass.__dict__.items()
            if isinstance(field, Argument)
        ]

        if include_default:
            self._attrs += [
                field_name[1:] for field_name, field in Context.__dict__.items()
                if isinstance(field, Argument) and field_name[1:] not in self._attrs
            ]

    def instantiate(self):
        self.arguments = [getattr(self, '_'+attr) for attr in self._attrs]
        return self._instantiate()

    def set_empty_args(self):
        self.arguments = [
            getattr(self, '_'+attr) for attr in self._attrs
            if getattr(self, attr) is None
        ]
        return self._instantiate()

    def _instantiate(self):
        parser = argparse.ArgumentParser(self.description)
        for arg in self.arguments:
            arg.add_to(parser)

        args = parser.parse_args()
        for attr in self._attrs:
            current = getattr(self, attr, None)
            setattr(self, attr,
                    self.validate(attr, getattr(args, attr, current))
            )
        return self

    def default(self):
        for attr in self._attrs:
            arg: Argument = getattr(self, '_'+attr)
            setattr(self, attr, arg.default)

    def __str__(self):
        return "; ".join([
            "{}: {}".format(attr, getattr(self, attr)) for attr in self._attrs
        ])

    def validate(self, attr, value):
        """
        Subclasses can override this method to implement custom handling
        of command line arguments

        :param attr: Command line argument name
        :param value: Value returned by argparse
        :return: value to use
        """

        if attr == "years":
            if type(value) is str:
                value = [value]
            years = []
            if isinstance(value, str):
                value = [value]
            for y in value:
                if ':' in y:
                    x = y.split(':')
                    y1 = int(x[0])
                    y2 = int(x[1])
                    years += range(y1, y2 + 1)
                else:
                    years.append(int(y))
            return sorted(years)
        return value

    @classmethod
    def enum(cls, enum_cls, s: str):
        """
        A helper method to return Enum value by its name

        :param cls: Enum class
        :param s: name of a member in Enum class
        :return: value of the member
        """

        d = {e.name: e for e in enum_cls}
        return d[s]

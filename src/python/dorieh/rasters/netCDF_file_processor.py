
#  Copyright (c) 2023.  Harvard University
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

"""
An entry point to a command line utility aggregating grid data
provided as NetCDF file over a set of shape files, assigning
labels defined in the shape files to the aggregated values.


See `NetCDF Website <https://www.unidata.ucar.edu/software/netcdf/>`__

"""

import logging
import os
from datetime import datetime
from typing import Optional, Dict

import yaml

from dorieh.rasters.gridmet_tools import find_shape_file
from dorieh.platform import init_logging
from dorieh.gis.compute_shape import StatsCounter

from dorieh.rasters.config import GridContext, OutputType
from dorieh.rasters.aggregator import Aggregator, GeoTiffAggregator, NetCDFAggregator

class NetCDFFile:
    def __init__(self, context: GridContext = None):
        """
        Creates a new instance

        :param context: An optional GridContext object, if not specified,
            then it is constructed from the command line arguments
        """

        if not context:
            context = GridContext(doc=__doc__).instantiate()
        self.context = context
        self.file_type = None
        log = os.path.basename(self.context.raw_downloads).split('.')[0]
        init_logging(
            name="aggr-" + log,
            level=logging.INFO
        )
        self.aggregator: Optional[Aggregator] = None
        self.infile = self.context.raw_downloads
        self.extra_columns = None
        StatsCounter.statistics = context.statistics
        return

    def on_prepare(self):
        """
        This method can be overwritten by subclasses
        to configure proper aggregation
        """

        pass

    def get_aggregation_year(self):
        return self.context.years

    def prepare(self):
        if self.infile.endswith(".nc"):
            self.file_type = "nc"
            aggregator = NetCDFAggregator
        elif self.infile.endswith(".tif") or self.infile.endswith(".tiff"):
            self.file_type = 'tiff'
            aggregator = GeoTiffAggregator
        elif OutputType.aggregation not in self.context.output:
            self.file_type = "nc"
            aggregator = NetCDFAggregator
        else:
            raise ValueError("NetCDF file is expected (extension .nc)")
        self.on_prepare()
        of, _ = os.path.splitext(os.path.basename(self.infile))
        of += '_' + self.context.geography.value + ".csv"
        if not os.path.isdir(self.context.destination):
            os.makedirs(self.context.destination, exist_ok=True)
        of = os.path.join(self.context.destination, of)
        if self.context.compress:
            of += ".gz"

        if not self.context.shape_files and self.context.shapes_dir:
            self.context.shape_files = find_shape_file(
                self.context.shapes_dir,
                int(self.get_aggregation_year()),
                str(self.context.geography.value),
                "polygon"
            )
        if len(self.context.shape_files) != 1:
            raise ValueError("Shape type is required and only one "
                             "shape type is allowed for aggregation."
                             "len(self.context.shape_files)={:d}"
                             .format(len(self.context.shape_files)))
        shape_file = self.context.shape_files[0]
        if len(self.context.variables) > 0:
            variable = self.context.variables
        else:
            raise ValueError("No variables are specified")
        self.aggregator = aggregator(
            infile=self.infile,
            variable=variable,
            outfile=of,
            strategy=self.context.strategy,
            shapefile=shape_file,
            geography=self.context.geography,
            extra_columns=self.extra_columns,
            ram=self.context.ram
        )
        return

    def get_domain_name(self):
        return "exposures"

    def get_table_name(self):
        if self.context.table is not None:
            return  self.context.table
        of = os.path.basename(self.aggregator.outfile).split('.')
        return of[0]

    def execute(self):
        start = datetime.now()
        if OutputType.aggregation in self.context.output:
            if os.path.isfile(self.infile):
                self.aggregator.execute()
                print(
                    "Aggregation of data from {} by {} has been executed. "
                    "Output: {}"
                        .format(
                            self.infile,
                            self.context.geography.value,
                            self.aggregator.outfile
                ))
            else:
                of = self.aggregator.write_header()
                logging.info("Input file was not found. Created empty file: {}"
                             .format(os.path.abspath(of)))
        if OutputType.data_dictionary in self.context.output:
            registry = self.get_registry()
            of = os.path.join(
                self.context.destination, self.get_domain_name() + ".yaml"
            )
            with open (of, "wt") as out:
                yaml.dump(registry, out)
            logging.info("Created data dictionary: " + os.path.abspath(of))
        # Info:
        end = datetime.now()
        self.aggregator.perf.total_time = end - start
        self.aggregator.perf.log("Resources: ")
        return

    def get_registry(self) -> Dict:
        return self.aggregator.get_registry(
            self.get_domain_name(),
            self.get_table_name(),
            description=self.context.description
        )


if __name__ == '__main__':
    task = NetCDFFile()
    task.prepare()
    task.execute()


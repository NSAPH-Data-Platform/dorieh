"""
API to aggregate data over shapes

The Aggregator class expects a netCDF dataset, containing 3 variables:
value, latitude and longitude
"""
#  Copyright (c) 2022. Harvard University
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
import logging
import math
import os
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Tuple, Set, Any

from dorieh.rasters.netCDF_tools import NCViewer
from dorieh.rasters.prof import ProfilingData
from dorieh.utils.profile_utils import qmem

import rasterio
from netCDF4 import Dataset
from dorieh.platform import init_logging
from dorieh.platform.pg_keywords import PG_NUMERIC_TYPE, PG_STR_TYPE, \
    PG_INT_TYPE
from dorieh.gis.compute_shape import StatsCounter
from dorieh.gis.constants import RasterizationStrategy, Geography
from dorieh.utils.io_utils import fopen, CSVWriter, Collector, sizeof_fmt

from dorieh.rasters.gridmet_tools import get_affine_transform, disaggregate, \
    estimate_optimal_downscaling_factor


class Aggregator(ABC):
    def __init__(self, infile: str, variable: str, outfile: str,
                 strategy: RasterizationStrategy, shapefile: str,
                 geography: Geography,
                 extra_columns: Tuple[List[str], List[str]] = None,
                 ram=0):
        """

        :param infile: Path to file with raster data to be aggregated.
            Can be either NetCDF or GeoTiff file
        :param variable: Name of variable or variables that need to be
            aggregated
        :param outfile: Path to the output "csv.gz" file
        :param strategy: Rasterization strategy
        :param shapefile: Path to shapefile with polygons
        :param geography: What kind of geography: US Counties or ZIP/ZCTA codes
        :param extra_columns: if we need to add any extra columns to the CSV
        :param ram: Runtime memory available to the process
        """

        self.infile = infile
        self.outfile = outfile
        self.factor = 1
        self.affine = None
        self.dataset: Dataset = None
        if isinstance(variable, list):
            self.aggr_variables = variable
        else:
            self.aggr_variables = [str(variable)]

        self.shapefile = shapefile
        self.geography = geography
        if extra_columns:
            self.extra_headers, self.extra_values = extra_columns
        else:
            self.extra_headers, self.extra_values = None, None
        self.strategy = None
        self.missing_value = None
        self.ram = ram
        self.set_strategy(strategy)
        self.perf = ProfilingData()

    def set_strategy(self, strategy: RasterizationStrategy):
        self.strategy = strategy
        if self.strategy in [
            RasterizationStrategy.default, RasterizationStrategy.all_touched
        ]:
            self.factor = 1
            set_factor = False
        else:
            set_factor = True
        ram = int (self.ram / math.sqrt(len(self.aggr_variables)))
        self.on_set_strategy(ram, set_factor)

    def on_set_strategy(self, ram: int, set_factor: bool):
        pass

    def prepare(self):
        if not self.affine:
            self.affine = get_affine_transform(self.infile, self.factor)
        logging.info("%s => %s", self.infile, self.outfile)
        self.open()
        variables = self.get_dataset_variables()

        for v in variables:
            if v in self.aggr_variables:
                return
        lv = [v.lower() for v in self.aggr_variables]
        for v in variables:
            if v.lower() in lv:
                idx = lv.index(v.lower())
                self.aggr_variables[idx] = v
                return

        vvv = [v for v in variables if v.lower() not in ['lat', 'lon']]
        raise ValueError(
            "Variable {} not found in the file {}. Available variables: {}"
            .format(self.aggr_variables, self.infile, ','.join(vvv))
        )

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def get_dataset_variables(self) -> Set[str]:
        pass

    @abstractmethod
    def get_layer(self, var):
        pass

    def get_header(self) -> List[str]:
        key = str(self.geography.value).lower()
        headers = self.aggr_variables + [key]
        if self.extra_headers:
            headers += self.extra_headers
        return headers

    def write_header(self):
        with fopen(self.outfile, "wt") as out:
            writer = CSVWriter(out)
            headers = self.get_header()
            writer.writerow(headers)
        return self.outfile

    def get_registry(self, domain_name: str, table_name: str,
                     description: str = None):
        t0 = datetime.now()
        if description is None:
            description = "Dorieh data model for aggregation of a grid"
        key = str(self.geography.value).lower()
        domain = {
            domain_name: {
                "schema": domain_name,
                "index": "all",
                "description": description,
                "header": True,
                "quoting": 3,
                "tables": {
                }
            }
        }
        columns = [
            {var: {
                "type": PG_NUMERIC_TYPE
            }} for var in self.aggr_variables
        ]
        columns.append({key: {
            "type": PG_STR_TYPE,
            "index": True
        }})
        pk = None
        if self.extra_headers:
            for i in range(len(self.extra_headers)):
                c = self.extra_headers[i]
                v = self.extra_values[i]
                if isinstance(i, int):
                    t = PG_INT_TYPE
                else:
                    t = PG_STR_TYPE
                columns.append({c: {
                    "type": t,
                    "index": True
                }})
                if c.lower() == "year":
                    pk = [key, c]

        table = {
            "columns": columns
        }
        if pk is not None:
            table["primary_key"] = pk

        domain[domain_name]["tables"][table_name] = table

        m = qmem()
        self.perf.update_mem_time(m, datetime.now() - t0)
        return domain

    def execute(self, mode: str = "wt"):
        """
        Executes computational task

        :param mode: mode to use opening result file
        :type mode: str
        :return:
        """

        self.prepare()
        if 'a' not in mode:
            self.write_header()
            if 't' in mode:
                mode = 'at'
            else:
                mode = 'a'
        with fopen(self.outfile, mode) as out:
            writer = CSVWriter(out)
            self.collect_data(writer)
        m = qmem()
        self.perf.update_mem_only(m)

    def collect_data(self, collector: Collector):
        t0 = datetime.now()
        layers = [self.get_layer(var) for var in self.aggr_variables]
        t1 = datetime.now()
        self.compute(collector, layers)
        collector.flush()
        t3 = datetime.now()
        t = datetime.now() - t0
        logging.info(" \t{} [{}]".format(str(t3 - t1), str(t)))

    def downscale(self, layer):
        if self.factor > 1:
            logging.info("Downscaling by the factor of " + str(self.factor))
            layer = disaggregate(layer, self.factor)
        else:
            layer = layer[:]
        m = qmem()
        self.perf.update_mem_only(m)
        return layer

    def compute(self, writer: Collector, layers):
        fid, _ = os.path.splitext(os.path.basename(self.infile))
        now = datetime.now()
        shape = layers[0].shape
        logging.info(
            "%s:%s:strategy=%s:%s: %s: layer shape %s",
            str(now),
            self.geography.value,
            self.strategy.value,
            self.aggr_variables,
            fid,
            str(shape)
        )
        if self.factor > self.perf.factor:
            self.perf.factor = self.factor
        x = layers[0].shape[0]
        y = layers[0].shape[1]
        if x > self.perf.shape_x:
            self.perf.shape_x = x
        if y > self.perf.shape_y:
            self.perf.shape_y = y

        if len(layers) == 1:
            layer = layers[0]
            for record in StatsCounter.process(
                    self.strategy,
                    self.shapefile,
                    self.affine,
                    layer,
                    self.geography
            ):
                row = [record.value, record.prop]
                if self.extra_values:
                    row += self.extra_values
                writer.writerow(row)
        else:
            for record in StatsCounter.process_layers(
                    self.strategy,
                    self.shapefile,
                    self.affine,
                    layers,
                    self.geography
            ):
                row: List[Any] = [v for v in record.values]
                row.append(record.prop)
                if self.extra_values:
                    row += self.extra_values
                writer.writerow(row)
        dt = datetime.now() - now
        self.perf.update_mem_time(StatsCounter.max_mem_used, None, dt)
        logging.info(
            "%s: %s completed in %s, memory used: %s",
            str(datetime.now()),
            fid,
            dt,
            sizeof_fmt(StatsCounter.max_mem_used)
        )


class NetCDFAggregator(Aggregator):
    def open(self):
        self.dataset = Dataset(self.infile)

    def get_dataset_variables(self) -> Set[str]:
        return set(self.dataset.variables)

    def get_layer(self, var):
        logging.info("Extracting layer: " + var)
        return self.downscale(self.dataset[var])

    def on_set_strategy(self, ram: int, set_factor):
        viewer = NCViewer(self.infile)
        if viewer.missing_value:
            self.missing_value = viewer.missing_value
        if set_factor:
            self.factor = viewer.get_optimal_downscaling_factor(ram)


class GeoTiffAggregator(Aggregator):

    def __init__(self, infile: str, variable: str, outfile: str,
                 strategy: RasterizationStrategy, shapefile: str,
                 geography: Geography,
                 extra_columns: Tuple[List[str], List[str]] = None,
                 ram: int = 0):
        super().__init__(infile, variable, outfile, strategy, shapefile,
                         geography, extra_columns, ram)
        self.array = None

    def open(self):
        if self.dataset is None:
            self.dataset = rasterio.open(self.infile)
        self.array = self.dataset.read()

    def get_dataset_variables(self) -> Set[str]:
        return set(self.dataset.descriptions)

    def get_layer(self, var):
        logging.info("Extracting layer: " + var)
        if var not in self.dataset.descriptions:
            raise ValueError(f'Variable {var} is not in the dataset')
        idx = self.dataset.descriptions.index(var)
        return self.downscale(self.array[idx])

    def on_set_strategy(self, ram: int, set_factor):
        self.dataset = rasterio.open(self.infile)
        grid_size = self.dataset.shape[0] * self.dataset.shape[1]
        if set_factor:
            self.factor = estimate_optimal_downscaling_factor(grid_size, ram)


if __name__ == '__main__':
    init_logging(level=logging.INFO)
    fn = sys.argv[1]
    if not fn.endswith(".nc"):
        raise ValueError("NetCDF file is expected (extension .nc)")
    sf = sys.argv[2]
    of, _ = os.path.splitext(fn)
    of += ".csv.gz"
    a = NetCDFAggregator(
        infile=fn,
        variable="PM25",
        outfile=of,
        strategy=RasterizationStrategy.downscale,
        shapefile=sf,
        geography=Geography.county,
        extra_columns=(["Year", "Month"], ["2018", "12"])
    )
    a.execute()
    print("All Done")


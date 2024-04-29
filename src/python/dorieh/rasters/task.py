"""
This module contains classes used to define, schedule and execute
long running computations used by gridMET pipelines
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

import csv
import logging
import os
from abc import ABC, abstractmethod
from datetime import date, timedelta, datetime
from enum import Enum
from typing import List, Dict

from netCDF4._netCDF4 import Dataset
from rasterstats.io import Raster
from tqdm import tqdm

from dorieh.rasters.config import GridmetVariable, GridMETContext, Shape
from dorieh.rasters.gridmet_tools import find_shape_file, get_nkn_url, get_variable, get_days, \
    get_affine_transform, disaggregate
from dorieh.rasters.netCDF_tools import NCViewer
from dorieh.rasters.prof import ProfilingData
from dorieh.gis.compute_shape import StatsCounter
from dorieh.gis.constants import Geography, RasterizationStrategy
from dorieh.gis.geometry import PointInRaster
from dorieh.utils.io_utils import DownloadTask, fopen, as_stream
from dorieh.utils.profile_utils import mem

NO_DATA = 32767.0  # The value filled in masked arrays in NetCDF files
# for the masked cells


def count_lines(f):
    with fopen(f, "r") as x:
        return sum(1 for line in x)


def quote(s:str) -> str:
    return '"' + s + '"'


class Parallel(Enum):
    points = "points"
    bands = "bands"
    days = "days"


class Collector(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def writerow(self, data: List):
        pass

    def flush(self):
        pass


class CSVWriter(Collector):
    def __init__(self, out_stream):
        super().__init__()
        self.out = out_stream
        self.writer = csv.writer(out_stream,
                                 delimiter=',',
                                 quoting=csv.QUOTE_NONE)

    def writerow(self, row: List):
        self.writer.writerow(row)

    def flush(self):
        self.out.flush()


class ListCollector(Collector):
    def __init__(self):
        super().__init__()
        self.collection = []

    def writerow(self, data: List):
        self.collection.append(data)

    def get_result(self):
        return self.collection


class ComputeGridmetTask(ABC):
    """
    An abstract class for a computational task that processes data in
    `Unidata netCDF (Version 4) format <https://www.unidata.ucar.edu/software/netcdf/>`_
    """

    origin = date(1900, 1, 1)

    def __init__(self, year: int, variable: GridmetVariable, infile: str,
                 outfile: str, date_filter=None, ram: int=0):
        """

        :param ram:
        :param date_filter:
        :param year: year
        :param variable: Gridemt band (variable)
        :param infile: File with source data in  NCDF4 format
        :param outfile: Resulting CSV file
        """

        self.year = year
        self.infile = infile
        self.outfile = outfile
        self.band = variable
        self.factor = 1
        self.affine = None
        self.dataset = None
        self.variable = None
        self.parallel = {Parallel.points}
        self.date_filter = date_filter
        self.perf = ProfilingData()
        self.missing_value = None
        self.ram = ram

    @classmethod
    def get_variable(cls, dataset: Dataset,  variable: GridmetVariable):
        return get_variable(dataset, variable.value)

    @abstractmethod
    def get_key(self):
        pass

    def get_days(self) -> Dict:
        all_days = get_days(self.dataset)
        days = dict()
        for i in range(len(all_days)):
            day = all_days[i]
            if self.date_filter:
                if self.date_filter.accept(self.to_date(day)):
                    days[day] = i
            else:
                days[day] = i
        return days

    def prepare(self) -> Dict:
        logging.info("%s => %s", self.infile, self.outfile)
        self.dataset = Dataset(self.infile)
        days = self.get_days()
        self.variable = self.get_variable(self.dataset, self.band)
        viewer = NCViewer(self.infile)
        if viewer.missing_value:
            self.missing_value = viewer.missing_value
        self.factor = viewer.get_optimal_downscaling_factor(self.ram)
        self.on_prepare()
        if not self.affine:
            self.affine = get_affine_transform(self.infile, self.factor)

        return days

    def on_prepare(self):
        pass

    def execute(self, mode: str = "wt"):
        """
        Executes computational task

        :param mode: mode to use opening result file
        :type mode: str
        :return:
        """

        days = self.prepare()

        with fopen(self.outfile, mode) as out:
            writer = CSVWriter(out)
            if 'a' not in mode:
                writer.writerow([self.band.value, "date", self.get_key().lower()])
            self.collect_data(days, writer)

    def collect_data(self, days: Dict, collector: Collector):
        t0 = datetime.now()
        for day in days:
            idx = days[day]
            layer = self.dataset[self.variable][idx, :, :]
            # layer = layer[layer.mask == False]
            t1 = datetime.now()
            self.compute_one_day(collector, day, layer)
            collector.flush()
            t3 = datetime.now()
            t = datetime.now() - t0
            logging.info(" \t{} [{}]".format(str(t3 - t1), str(t)))
        return collector

    @abstractmethod
    def compute_one_day(self, writer: Collector, day, layer):
        """
        Computes required statistics for a single day.
        This method is called by `execute()` and is implemented in
        specific subclasses

        :param writer: CSV Writer to output the result
        :param day: day
        :param layer: layer, corresponding to the day
        :return: Nothing
        """

        pass

    def to_date(self, day) -> datetime.date:
        return self.origin + timedelta(days=day)


class ComputeShapesTask(ComputeGridmetTask):
    """
    Class describes a compute task to aggregate data over geography shapes

    The data is expected in
    .. _Unidata netCDF (Version 4) format: https://www.unidata.ucar.edu/software/netcdf/
    """

    def __init__(self, year: int, variable: GridmetVariable, infile: str,
                 outfile: str, strategy: RasterizationStrategy, shapefile: str,
                 geography: Geography, date_filter=None, ram=0):
        """

        :param ram:
        :param date_filter:
        :param year: year
        :param variable: gridMET band (variable)
        :param infile: File with source data in  NCDF4 format
        :param outfile: Resulting CSV file
        :param strategy: Rasterization strategy to use
        :param shapefile: Shapefile for used collection of geographies
        :param geography: Type of geography, e.g. zip code or county
        """

        super().__init__(year, variable, infile, outfile, date_filter, ram)

        self.strategy = strategy
        self.shapefile = shapefile
        self.geography = geography

    def on_prepare(self):
        if self.strategy in [
            RasterizationStrategy.default, RasterizationStrategy.all_touched
        ]:
            self.factor = 1

    def get_key(self):
        return self.geography.value.upper()

    def compute_one_day(self, writer: Collector, day, layer):
        dt = self.to_date(day)

        start_ts = datetime.now()
        if self.factor > 1:
            logging.info("Downscaling by the factor of " + str(self.factor))
            layer = disaggregate(layer, self.factor)

        if self.factor > self.perf.factor:
            self.perf.factor = self.factor
        x = layer.shape[0]
        y = layer.shape[1]
        if x > self.perf.shape_x:
            self.perf.shape_x = x
        if y > self.perf.shape_y:
            self.perf.shape_y = y

        logging.info(
            "%s:%s:%s:%s: layer shape %s",
            str(start_ts),
            self.geography.value,
            self.band.value,
            dt,
            str(layer.shape)
        )

        aggr_ts = datetime.now()
        for record in StatsCounter.process(
            self.strategy,
            self.shapefile,
            self.affine, layer,
            self.geography,
            self.missing_value
        ):
            writer.writerow([record.value, dt.strftime("%Y-%m-%d"), record.prop])

        now = datetime.now()
        delta_ts = now - start_ts
        delta_aggr_ts = now -aggr_ts
        logging.debug(
            "Completed in %s, aggregation: %s",
            delta_ts,
            delta_aggr_ts
        )
        self.perf.update_mem_time(
            StatsCounter.max_mem_used, delta_ts, delta_aggr_ts
        )


class ComputePointsTask(ComputeGridmetTask):
    """
    Class describes a compute task to assign data to a collection of points

    The data is expected in
    .. _Unidata netCDF (Version 4) format: https://www.unidata.ucar.edu/software/netcdf/
    """

    force_standard_api = False

    def __init__(self, year: int, variable: GridmetVariable, infile: str,
                 outfile: str, points_file: str, coordinates: List,
                 metadata: List, date_filter=None, ram=0):
        """

        :param ram:
        :param year: year
        :param variable: Gridemt band (variable)
        :param infile: File with source data in  NCDF4 format
        :param outfile: Resulting CSV file
        :param points_file: path to a file containing coordinates of points
            in csv format.
        :param coordinates: A two element list of column names in csv
            corresponding to coordinates
        :param metadata: A list of column names in csv that should be
            interpreted as metadata (e.g. ZIP, site_id, etc.)
        """

        super().__init__(year, variable, infile, outfile, date_filter, ram)
        self.points_file = points_file

        assert len(coordinates) == 2
        self.coordinates = coordinates
        self.metadata = metadata
        self.first_layer = None

    def get_key(self):
        return self.metadata[0]

    def on_prepare(self):
        self.first_layer = Raster(
            self.dataset[self.variable][0, :, :],
            self.affine,
            nodata=-NO_DATA,
        )
        return

    def make_point(self, row) -> PointInRaster:
        x = float(row[self.coordinates[0]])
        y = float(row[self.coordinates[1]])
        point = PointInRaster(self.first_layer, self.affine, x, y)
        return point

    def execute(self, mode: str = "w") -> None:
        days = self.prepare()

        logging.info("Prepare rasters")
        rasters = {}
        for day_number in tqdm(range(len(days)), total=len(days)):
            layer = self.dataset[self.variable][day_number, :, :]
            raster = Raster(layer, self.affine, nodata=NO_DATA)
            rasters[day_number] = raster

        logging.info("Process points")
        with fopen(self.points_file, "r") as points_file, \
                fopen(self.outfile, "wt") as out:
            reader = csv.DictReader(points_file)
            writer = CSVWriter(out)
            writer.writerow([self.band.value, "date", self.get_key().lower()])

            for n, row in enumerate(tqdm(reader)):
                point = self.make_point(row)
                if point.is_masked():
                    continue

                metadata = [row[p] for p in self.metadata]

                for day_number in range(len(days)):
                    dt = self.origin + timedelta(days=days[day_number])
                    mean = point.bilinear(rasters[day_number])

                    writer.writerow([mean, dt] + metadata)

                if n % 10_000:
                    writer.flush()

    def compute_one_day(self, writer: Collector, day, layer):
        pass


class DownloadGridmetTask:
    """
    Task to download source file in NCDF4 format
    """

    BLOCK_SIZE = 65536

    @classmethod
    def get_url(cls, year:int, variable: GridmetVariable) -> str:
        """
        Constructs URL given a year and band

        :param year: year
        :param variable: Gridmet band (variable)
        :return: URL for download
        """
        return get_nkn_url(variable.value, year)

    def __init__(self, year: int,
                 variable: GridmetVariable,
                 destination: str):
        """
        :param year: year
        :param variable: Gridmet band (variable)
        :param destination: Destination directory for all downloads
        """
        if not os.path.isdir(destination):
            os.makedirs(destination)

        url = self.get_url(year, variable)
        target = os.path.join(destination, url.split('/')[-1])
        self.download_task = DownloadTask(target, [url])
        self.perf = ProfilingData()
        #self.max_mem_used = 0

    def target(self):
        """
        :return: File path for downloaded data
        """
        return self.download_task.destination

    def execute(self):
        """
        Executes the task
        :return: None
        """

        logging.info(str(self.download_task))
        if self.download_task.is_up_to_date():
            logging.info("Up to date")
            return
        buffer = bytearray(self.BLOCK_SIZE)
        start_ts = datetime.now()

        with fopen(self.target(), "wb") as writer, \
                as_stream(self.download_task.urls[0]) as reader:
            n = 0
            while True:
                ret = reader.readinto(buffer)
                if not ret:
                    break
                writer.write(buffer[:ret])
                n += 1
                if (n % 20) == 0:
                    print("*", end='')
        self.perf.update_mem_time(mem(), datetime.now() - start_ts)
        return


class GridmetTask:
    """
    Defines a task to download and process data for a single year and variable
    Instances of this class can be used to parallelize processing
    """

    @classmethod
    def destination_file_name(cls, context: GridMETContext,
                              year: int,
                              variable: GridmetVariable):
        """
        Constructs a file name for a given set of parameters

        :param context: Configuration object for the pipeline
        :param year: year
        :param variable: Gridmet band (variable)
        :return: `variable_geography_year.csv[.gz]`
        """
        g = context.geography.value
        s = context.shapes[0].value if len(context.shapes) == 1 else "all"
        f = "{}_{}_{}_{:d}.csv".format(variable.value, g, s, year)
        if context.compress:
            f += ".gz"
        return os.path.join(context.destination, f)

    @classmethod
    def find_shape_file(cls, context: GridMETContext, year: int, shape: Shape):
        """
        Finds shapefile for a given type of geographies for the
        closest available year

        :param context: Configuration object for the pipeline
        :param year: year
        :param shape: Shape type
        :return: a shape file for a given year if it exists or for the latest
            year before the given
        """

        parent_dir = context.shapes_dir
        geo_type = context.geography.value
        shape_type = shape.value
        return find_shape_file(parent_dir, year, geo_type, shape_type)

    def __init__(self, context: GridMETContext,
                 year: int,
                 variable: GridmetVariable):
        """
        :param context: Configuration object for the pipeline
        :param year: year
        :param variable: gridMET band (variable)
        """

        if os.path.isfile(context.raw_downloads):
            self.download_task = None
            self.raw_download = context.raw_downloads
        else:
            dest = context.raw_downloads
            _, ext = os.path.splitext(dest)
            if not os.path.isdir(dest) or ext:
                dest = os.path.dirname(dest)
            self.download_task = DownloadGridmetTask(year, variable, dest)
            self.raw_download = self.download_task.target()

        destination = context.destination
        if not os.path.isdir(destination):
            os.makedirs(destination)

        result = self.destination_file_name(context, year, variable)

        self.compute_tasks = []

        if context.shape_files:
            self.compute_tasks = [
                ComputeShapesTask(year, variable, self.raw_download, result,
                                  context.strategy, shape_filename,
                                  context.geography, context.dates,
                                  ram=context.ram)
                for shape_filename in context.shape_files
            ]

        elif Shape.polygon in context.shapes or not context.points:
            self.compute_tasks = [
                ComputeShapesTask(year, variable, self.download_task.target(),
                                  result, context.strategy, shape_file,
                                  context.geography, context.dates,
                                  ram=context.ram)
                for shape_file in [
                    self.find_shape_file(context, year, shape)
                    for shape in context.shapes
                ]
            ]

        if Shape.point in context.shapes and context.points:
            self.compute_tasks += [
                ComputePointsTask(year, variable, self.download_task.target(),
                                  result, context.points, context.coordinates,
                                  context.metadata, ram=context.ram)
            ]
        if not self.compute_tasks:
            raise Exception("Invalid combination of arguments")
        self.perf = ProfilingData()

    def execute(self):
        """
        Executes the task. First the download subtask is executed unless
        the corresponding file has already been downloaded. Then the compute
        tasks are executed

        :return: None
        """

        if self.download_task is not None:
            self.download_task.execute()
            self.perf.update(self.download_task.perf)
        for task in self.compute_tasks:
            task.execute()
            self.perf.update(task.perf)

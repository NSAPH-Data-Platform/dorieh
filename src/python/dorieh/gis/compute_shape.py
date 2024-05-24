"""
This module processes layers of data containing geographic coordinates
and observed values for a certain parameter (band)
and returns records containing
an identifier for a geographic shape and the value of the band
aggregated over the shape.

A progress bar is displayed while the computational process is running

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

import os.path
import sys
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

from dataclasses import dataclass
from typing import Iterable, Optional, Tuple, List, Callable, Dict

import rasterio
from rasterstats import zonal_stats, gen_zonal_stats
from tqdm import tqdm, trange
import shapefile

from dorieh.utils.profile_utils import mem, qmem, qqmem
from .constants import RasterizationStrategy, Geography

NO_DATA = 32767.0  # The default value filled in masked arrays in NetCDF files
# for the masked cells
# This value is overridden if it is defined by a property "missing_value"
# in the metadata of the NetCDF file


@dataclass
class Record:
    value: Optional[float]
    prop: str


@dataclass
class MultiRecord:
    values: List[Optional[float]]
    prop: str


class StatsCounter:
    statistics = "mean"
    max_mem_used = 0

    @classmethod
    def get_key_for_geography(cls, shpfile: str, geography: Geography) -> Tuple:
        shape = shapefile.Reader(shpfile)
        fields = [f[0] for f in shape.fields]
        if geography == Geography.zip:
            key = cls._determine_zip_key(fields)
        elif geography == Geography.zcta:
            key = cls._determine_zcta_key(fields)
        elif geography == Geography.county:
            key = cls._determine_county_key(fields)
        else:
            raise ValueError("Unsupported geography: " + str(geography))

        return key

    @classmethod
    def prepare_stats(cls, strategy: RasterizationStrategy, shpfile: str,
                      affine: rasterio.Affine, layer: Iterable, no_data,
                      is_generator: bool) -> List:
        """
        Given a layer, i.e. a slice of a dataframe, and a shapefile
        returns an iterable of records, containing aggregated values
        of the observations over the shapes in the shapefile.

        :param no_data: Value taht is treated as missing value
        :param strategy: Rasterization strategy to be used
        :param shpfile: A path to shapefile to be used
        :param affine: An optional affine transformation to be applied to
            the coordinates
        :param layer: A slice of dataframe, containing coordinates and values
        :return: A list of statistics compute objects
        """

        if is_generator:
            stats_function: Callable = gen_zonal_stats
        else:
            stats_function: Callable = zonal_stats

        non_all_touched_strategies = [
            RasterizationStrategy.default,
            RasterizationStrategy.combined,
            RasterizationStrategy.downscale,
        ]
        all_touched_strategies = [
            RasterizationStrategy.all_touched,
            RasterizationStrategy.auto,
            RasterizationStrategy.combined,
        ]

        stats = []
        if strategy in non_all_touched_strategies:
            stats.append(
                stats_function(
                    shpfile,
                    layer,
                    stats=cls.statistics,
                    affine=affine,
                    geojson_out=True,
                    all_touched=False,
                    nodata=no_data,
                )
            )
        if strategy in all_touched_strategies:
            stats.append(
                stats_function(
                    shpfile,
                    layer,
                    stats=cls.statistics,
                    affine=affine,
                    geojson_out=True,
                    all_touched=True,
                    nodata=no_data,
                )
            )

        return stats

    @classmethod
    def process(
            cls,
            strategy: RasterizationStrategy,
            shpfile: str,
            affine: rasterio.Affine,
            layer: Iterable,
            geography: Geography,
            no_data=None
    ) -> Iterable[Record]:
        """
        Given a layer, i.e. a slice of a dataframe, and a shapefile 
        returns an iterable of records, containing aggregated values
        of the observations over the shapes in the shapefile. 
        
        :param no_data: Values that is treated as missing value
        :param strategy: Rasterization strategy to be used
        :param shpfile: A path to shapefile to be used
        :param affine: An optional affine transformation to be applied to
            the coordinates
        :param layer: A slice of dataframe, containing coordinates and values
        :param geography: WHat type of geography is to be used: zip codes
            or counties
        :return: An iterable of records, containing an identifier
            of a certain shape with the aggregated value of the observation
            for this shape
        """

        if no_data is None:
            no_data = NO_DATA
        key = cls.get_key_for_geography(shpfile, geography)

        stats = cls.prepare_stats(
            strategy, shpfile, affine, layer, no_data, True
        )

        n = 0
        step = 100
        if len(stats) == 2:
            # Combined strategy

            iterator = zip(stats[0], stats[1])
            zipped = True
        else:
            iterator = stats[0]
            zipped = False

        label = os.path.basename(shpfile)
        cls.max_mem_used = 0
        pid = os.getpid()
        with tqdm(
                file=sys.stdout,
                desc=f"Aggregating over {label} using '{strategy.value}' strategy"
        ) as pbar:
            for s in iterator:
                if zipped:
                    s1, s2 = s
                    record = cls._combine(key, s1, s2)
                else:
                    if isinstance(cls.statistics, list):
                        values = [
                            s['properties'][stat] for stat in cls.statistics
                        ]
                        mean = ':'.join([
                            "{}={}".format(cls.statistics[i], str(values[i]))
                            for i in range(len(cls.statistics))
                        ])
                    else:
                        mean = s['properties'][cls.statistics]
                    props = [s['properties'][subkey] for subkey in key]
                    prop = "".join(props)
                    record = Record(value=mean, prop=prop)
                m = qqmem(pid)
                if m > cls.max_mem_used:
                    cls.max_mem_used = m
                if (n % step) == 0:
                    m = mem()
                    if m > cls.max_mem_used:
                        cls.max_mem_used = m
                    pbar.update(step)
                if (n % step) == 0:
                    pbar.update(step)
                n += 1
                yield record

    @classmethod
    def process_layers(
            cls,
            strategy: RasterizationStrategy,
            shpfile: str,
            affine: rasterio.Affine,
            layers: List[Iterable],
            geography: Geography
    ) -> Iterable[MultiRecord]:
        """
        Given a layer, i.e. a slice of a dataframe, and a shapefile
        returns an iterable of records, containing aggregated values
        of the observations over the shapes in the shapefile.

        :param strategy: Rasterization strategy to be used
        :param shpfile: A path to shapefile to be used
        :param affine: An optional affine transformation to be applied to
            the coordinates
        :param layers: A list of slices of dataframe, containing coordinates
            and values
        :param geography: WHat type of geography is to be used: zip codes
            or counties
        :return: An iterable of records, containing an identifier
            of a certain shape with the aggregated value of the observation
            for this shape
        """

        if strategy == RasterizationStrategy.combined:
            raise IncompatibleArgumentsError(
                "Combining all_tocuhed with default and multiple "
                "variables is not implemented"
            )
        key = cls.get_key_for_geography(shpfile, geography)

        stats = (
            cls.prepare_stats(strategy, shpfile, affine, layer, NO_DATA,
                              True)[0]
            for layer in layers
        )

        n = 0
        step = 10
        iterator = zip(*stats)
        label = os.path.basename(shpfile)
        cls.max_mem_used = 0
        pid = os.getpid()
        with tqdm(
                file=sys.stdout,
                desc=f"Aggregating over {label} using '{strategy.value}' strategy"
        ) as pbar:
            for ss in iterator:
                means = [s['properties'][cls.statistics] for s in ss]
                props_array = [
                    [
                        s['properties'][subkey] for subkey in key
                    ] for s in ss
                ]
                props = {"".join(p) for p in props_array}
                if len(props) != 1:
                    raise AggregationError("Conflicting geo ids: " + str(props))
                prop = next(iter(props))
                record = MultiRecord(values=means, prop=prop)
                m = qqmem(pid)
                if m > cls.max_mem_used:
                    cls.max_mem_used = m
                if (n % step) == 0:
                    m = mem()
                    if m > cls.max_mem_used:
                        cls.max_mem_used = m
                    pbar.update(step)
                n += 1
                yield record

    @classmethod
    def process_layers_return_dict(
            cls,
            strategy: RasterizationStrategy,
            shpfile: str,
            affine: rasterio.Affine,
            layers: List[Iterable],
            geography: Geography
    ) -> Dict[str, MultiRecord]:
        """
        Given a layer, i.e. a slice of a dataframe, and a shapefile
        returns an iterable of records, containing aggregated values
        of the observations over the shapes in the shapefile.

        :param strategy: Rasterization strategy to be used
        :param shpfile: A path to shapefile to be used
        :param affine: An optional affine transformation to be applied to
            the coordinates
        :param layers: A list of slices of dataframe, containing coordinates
            and values
        :param geography: WHat type of geography is to be used: zip codes
            or counties
        :return: A List of records, containing an identifier
            of a certain shape with the aggregated value of the observation
            for this shape
        """

        key = cls.get_key_for_geography(shpfile, geography)

        records = dict()
        for l1 in range(len(layers)):
            layer = layers[l1]
            stats = cls.prepare_stats(strategy, shpfile, affine, layer, NO_DATA,
                                      False)
            for i in range(len(stats[0])):
                if len(stats) == 2:
                    # Combined strategy
                    mean, prop = cls._combine(key, stats[0][i], stats[1][i])
                else:

                    mean = stats[0][i]['properties'][cls.statistics]
                    props = [stats[0][i]['properties'][subkey] for subkey in
                             key]
                    prop = "".join(props)
                if prop in records:
                    record = records[prop]
                else:
                    record = MultiRecord([None for _ in range(l1)], prop)
                    records[prop] = record
                record.values.append(mean)
            print('*', end=None)
        print()
        return records

    @classmethod
    def _determine_zip_key(cls, row) -> Tuple:
        candidates = ["ZIP"]
        return cls._determine_key(row, candidates),

    @classmethod
    def _determine_zcta_key(cls, row) -> Tuple:
        candidates = ["ZCTA5", "ZCTA5CE00", "ZCTA5CE10", "ZCTA5CE20"]
        return cls._determine_key(row, candidates),

    @classmethod
    def _determine_county_key(cls, row) -> Tuple:
        candidates = ["COUNTY", "COUNTYFP"]
        c = cls._determine_key(row, candidates)
        s = cls._determine_key(row, ["STATE", "STATEFP"])
        return s, c

    @staticmethod
    def _determine_key(row, candidates) -> str:
        props = None
        for candidate in candidates:
            if isinstance(row, dict):
                if candidate in row['properties']:
                    return candidate
                props = str([key for key in row['properties']])
            elif isinstance(row, list):
                if candidate in row:
                    return candidate
                props = row
            else:
                raise ValueError("Unknown type of row: " + str(row))
        raise ValueError(
            f"None of the expected properties found ('{candidates}'). "
            + f"Available: '{props}'"
        )

    @classmethod
    def _combine(cls, key, r1, r2) -> Record:
        prop1 = "".join([r1['properties'][subkey] for subkey in key])
        prop2 = "".join([r2['properties'][subkey] for subkey in key])
        assert prop1 == prop2

        m1 = r1['properties'][cls.statistics]
        m2 = r2['properties'][cls.statistics]
        if m1 and m2:
            mean = (m1 + m2) / 2
        elif m2:
            mean = m2
        elif m1:
            raise AssertionError("m1 && !m2")
        else:
            mean = None
        return Record(value=mean, prop=prop1)


class AggregationError(RuntimeError):
    pass


class IncompatibleArgumentsError(NotImplementedError):
    pass

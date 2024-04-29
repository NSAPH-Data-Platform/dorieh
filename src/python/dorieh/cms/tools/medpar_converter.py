"""
Converter for CMS DAT files described by FTS to CSV
"""

#  Copyright (c) 2022-2022. Harvard University
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
#
import concurrent
import glob
import os
import sys
import traceback
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional

from cms.tools.mcr_file import MedicareFile


class MedParFileSet:
    def __init__(self, fts:str, dat: List[str], destination: str):
        self.fts = fts
        self.dat = dat
        self.year = None
        self.dir = os.path.dirname(fts)
        self.name, _ = os.path.splitext(os.path.basename(fts))
        d = self.dir
        while len(d) > 3:
            d, e = os.path.split(d)
            if e.isdigit():
                yyyy = int(e)
                if 1999 < yyyy < 2030:
                    if e in self.name:
                        self.year = yyyy
        if self.year is None:
            raise ValueError("Could not find year for " + fts)
        self.reader: MedicareFile = MedicareFile(
                    dir_path=self.dir,
                    name=self.name,
                    year=str(self.year),
                    dest = os.path.join(destination, str(self.year))
                )
        return

    def __str__(self) -> str:
        return "{:d}: {}.(fts|{:d}-dat)".format(
            self.year, self.name, len(self.dat)
        )


class MedparConverter:
    @classmethod
    def dataset(cls, fts, destination) -> Optional[MedParFileSet]:
        base, ext = os.path.splitext(fts)
        csv_gz = sorted(glob.glob(base + "*.csv.gz"))
        if csv_gz:
            print("Skipping " + fts)
            return None
        dat = sorted(glob.glob(base + "*.dat"))
        if not dat:
            raise ValueError(
                "Mismatch: {} does not have corresponding dat file(s)".
                    format(fts)
            )
        return MedParFileSet(fts, dat, destination)

    @classmethod
    def find(cls, basepath: str, destination: str) -> List[MedParFileSet]:
        datasets: List[MedParFileSet] = []
        fts_files = sorted(glob.glob(
            os.path.join(basepath, "**", "*.fts"),
            recursive=True
        ))
        for fts in fts_files:
            ds = cls.dataset(fts, destination)
            if ds is not None:
                datasets.append(ds)
        return datasets

    def __init__(self, source_path: str,
                 destination: str = None,
                 verbose: bool = True):
        self.datasets: List[MedParFileSet] = []
        self.verbose = verbose
        if os.path.isdir(source_path):
            if destination is None:
                destination = source_path
            self.datasets = self.find(source_path, destination)
        elif os.path.isfile(source_path):
            if destination is None:
                raise ValueError(
                    "When source path is a single file, "
                    "destination must be defined"
                )
            self.datasets = [self.dataset(source_path, destination)]

    def list(self):
        for dataset in self.datasets:
            print(dataset)

    @staticmethod
    def convert_dataset(dataset: MedParFileSet, verbose):
        try:
            status = dataset.reader.status()
            if status in ["READY", "ERROR"] or "MISMATCH" in status:
                return "{}: SKIPPED[{}]".format(dataset.fts, status)
            if verbose:
                dataset.reader.info()
            dataset.reader.export()
            return "{}: SUCCESS".format(dataset.fts)
        except Exception as x:
            traceback.print_exc()
            return "{}: FAILED".format(dataset.fts)

    def convert(self):
        with ThreadPoolExecutor() as executor:
            futures = []
            for dataset in self.datasets:
                futures.append(
                    executor.submit(self.convert_dataset,
                                    dataset=dataset,
                                    verbose=self.verbose)
                )
        for future in concurrent.futures.as_completed(futures):
            print(future.result())

    def status(self):
        with ThreadPoolExecutor() as executor:
            futures = []
            for dataset in self.datasets:
                futures.append(
                    executor.submit(dataset.reader.status_message)
                )
        for future in concurrent.futures.as_completed(futures):
            print(future.result())


def args():
    parser = ArgumentParser ("Converter for CMS dat files described by FTS to csv")
    parser.add_argument(help="Path to a source directory or an FTS file",
                        dest="input")
    parser.add_argument("--status", "-s", action='store_true',
                        help="Display status and exit")
    parser.add_argument("--convert", "-c", action='store_true',
                        help="Do conversion")
    parser.add_argument("--verbose", "-v", action='store_true',
                        help="Display additional information")
    parser.add_argument("--destination", "-d",
                        help="Destination for converted files")
    arguments = parser.parse_args()
    return arguments


if __name__ == '__main__':
    my_args = args()
    status = False
    converter = MedparConverter(source_path=my_args.input,
                                destination=my_args.destination,
                                verbose=my_args.verbose)
    if my_args.verbose:
        converter.list()
    if my_args.status:
        converter.status()
    if my_args.convert:
        converter.convert()



#  Copyright (c) 2023. Harvard University
#
#  Developed by Research Software Engineering,
#  Harvard University Research Computing
#  and The Harvard T.H. Chan School of Public Health
#  Authors: Michael A Bouzinier, Kezia Irene, Michelle Audirac
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


"""
Given a NetCDF file with absolute values (e.g., for PM25) and a set of
NetCDF files containing percentage values for individual components,
this tool consolidates all data into a single NetCDF file with both
percentages and absolute values for all components.

See also:

https://unidata.github.io/netcdf4-python/
https://neetinayak.medium.com/combine-many-netcdf-files-into-a-single-file-with-python-469ba476fc14
https://docs.xarray.dev/en/stable/api.html

"""

import argparse
import logging
import os.path
import shutil
import sys
import tempfile
from typing import Optional, List

import numpy
import rasterio
import rioxarray
import xarray
from netCDF4 import Dataset


#from dorieh.platform import init_logging


class NetCDFDataset:
    """
    Class to combine NetCDF dataset with absolute values with
    dependent datasets containing components

    """

    def __init__(self):
        self.dataset: Optional[Dataset] = None
        '''NetCDF Dataset that we will be modifying'''
        self.rio_dataset = None
        '''Rasterio dataset that holds metadata lost when writing NetCDF dataset'''
        self.main_var: Optional[str] = None
        '''The name of the main variable'''
        self.components_list = [] 
        self.percentages: List[str] = []
        '''The names of the component variables containing percentages'''
        self.abs_values: List[str] = []
        '''The names of the component variables containing absolute values'''
        self.absolute_values_read = False
        self.temp_output = None
        
        return
    
    def open_original_dataset(self, infile):
        _, self.temp_output = tempfile.mkstemp()
        shutil.copyfile(infile, self.temp_output)
        self.dataset = Dataset(self.temp_output, mode='r+')
        self.rio_dataset = rasterio.open(infile)
        return

    def read_abs_values(self, filename: str, var: str = None):
        """
        Reads the NetCDF dataset from a \*.nc file
        Assumes that this dataset contains absolute values of
        the variable with the name provided by var parameter.

        Raises an exception if the variable is not None but is not present n the dataset.
        If the parameter "var" is None, checks that there is only one variable present beside "lat" and "lon".
        Raises exception if there is more than one variable

        :param var: The variable containing the absolute values of the feature of interest, e.g., "pm25"
            If None, defaults to a single variable present in teh dataset beside "lat" and "lon"
        :param filename: A path to file to read.
            Can also be a python 3 pathlib instance or the URL of an OpenDAP dataset.
        :raises: ValueError if var is None and there is more than one variable in the dataset or, if var
            is not None and is not present in teh dataset
        """
        # Create a Dataset variable for the file

        # Create new netcdf file
        self.open_original_dataset(filename)

        # If var is None, check that there is only one variable present beside "lat" and "lon"
        if var is None:
            variables = list(self.dataset.variables.keys())
            variables.remove("LAT")
            variables.remove("LON")
            if len(variables) != 1:
                raise ValueError(
                    "If var is None, there must be exactly one "
                    "variable besides 'lat' and 'lon'."
                )

            # Get the variable name
            var = variables[0]

        # Check that the specified variable is present in the dataset
        if var not in self.dataset.variables:
            raise ValueError("The variable '%s' is not present in the dataset." % var)

        # Get the absolute values of the specified variable
        self.abs_values = self.dataset.variables[var][:]

        # Assign the units from the old dataset to the new dataset
        self.absolute_values_read = True
        self.main_var = var 
        logging.info("Done with read_abs_values")
        return var

    @classmethod
    def pct_var(cls, var: str) -> str:
        return var + 'p'

    def add_component(self, filename: str, var: str = None):
        """
        Reads the NetCDF dataset from a \\*.nc file
        Assumes that this dataset contains percentage of a component defined by
        the var parameter.

        Can only be called after the dataset is initialized with absolute values.

        :param var: The variable containing percentage of a certain component
        :param filename: A path to file to read.
            Can also be a python 3 pathlib instance or the URL of an OpenDAP dataset.
        :raises: ValueError if var is None and there is more than one variable in the dataset or, if var
            is not None and is not present in the dataset
        :raises: ValueError if the grid of the component file is incompatible with
            the gird of the existing Dataset
        :raises: ValueError if the absolute values have not yet been read
        """

        # Check if absolute values have been read
        if not self.absolute_values_read:
            raise ValueError("The absolute values have not been read yet.")

        # Read the NetCDF dataset from the file
        component_pct_dataset = Dataset(filename)
        logging.info("New dataset variables: " + str(component_pct_dataset.variables.keys()))

        # If var is None, check that there is only one variable present beside "lat" and "lon"
        if var is None:
            variables = list(component_pct_dataset.variables.keys())
            variables.remove("LAT")
            variables.remove("LON")
            if len(variables) != 1:
                raise ValueError("If var is None, there must be exactly one variable besides 'lat' and 'lon'.")

            # Get the variable name
            var = variables[0]
            logging.debug("These are the variables of the components: " + var)
            
            logging.debug(str(self.components_list))
            self.components_list.append(var)
            logging.debug("Shape: " + str(component_pct_dataset[var].shape))

        
        # Check if the grid of the component file is compatible with the grid of the existing Dataset
        if component_pct_dataset[var].shape != self.dataset[self.main_var].shape:
            raise ValueError("The grid of the component file is incompatible with the grid of the existing Dataset.")

        
        # Create a new variable in the dataset to store the component data
        component_out = self.dataset.createVariable(
            self.pct_var(var), 'f4', component_pct_dataset[var].dimensions
        )

        # Add the component data to the dataset
        component_out[:] = component_pct_dataset.variables[var][:]
        # Add units to the variable
        component_out.units = self.dataset.variables[self.main_var].units
        logging.debug(str(self.dataset))
        logging.info("All components have been added")
        return

    def add_components(self, filenames: List[str]):
        """
        Adds multiple components in a single call from multiple files. Assumes that
        every file given contains only one variable beside lat and lon

        Can only be called after the dataset is initialized with absolute values.

        :param filenames:  A list of file paths to read.
            Elements of the list can also be a python 3 pathlib instance or the URL of an OpenDAP dataset.
        :raises: ValueError if there is more than one variable in any of the datasets
        :raises: ValueError if the grid of a component file is incompatible with
            the gird of the existing Dataset
        :raises: ValueError if the absolute values have not yet been read
        """
            # Check if absolute values have been read
        if not self.absolute_values_read:
            raise ValueError("The absolute values have not been read yet.")

        for filename in filenames:
            # Read the NetCDF dataset from the file
            logging.info("Adding components from: " + filename)
            self.add_component(filename)

        logging.debug("This is the dataset after adding components:")
        logging.debug(str(self.dataset))
             
        return

    def compute_abs_values(self):
        """
        Computes absolute values for every component present in the dataset by applying a formula.

        :param components: Array of component names
        :return: None
        :raises: ValueError if the absolute values have not yet been read
        """
        # Check if absolute values have been read
        if not self.absolute_values_read:
            raise ValueError("The absolute values have not been read yet.")

        for component in self.components_list:
            # Compute the absolute values for the component
            component_array = self.dataset.variables[self.pct_var(component)][:]
            component_array = numpy.nan_to_num(
                component_array, copy=True, nan=0, posinf=0, neginf=0
            )
            modified_values = component_array * self.dataset.variables[self.main_var][:] / 100

            # Create a new variable in the output dataset for the modified values
            modified_variable = self.dataset.createVariable(
                component, 'f4', ('LAT', 'LON')
            )
            modified_variable[:] = modified_values[:]
            # Add units to the variable
            modified_variable.units = "ug/m3"
        logging.info("Final dataset: ")
        logging.info(str(self.dataset))
        return
    
    def get_dataset(self) -> Dataset:
        return self.dataset

    def close (self, output_file_name):
        """
        Writes all the data to the output file and closes all temporary objects

        :return: None
        """
        # Save the current state of the dataset to a new file

        self.dataset.sync()
        with xarray.open_dataset(self.temp_output) as rds:
            for var in rds.variables:
                if var in self.components_list:
                    rds[var] = rds[var].where(rds[var] < 1000)
            rds.rio.write_crs(4326, inplace=True)
            rds.rio.write_transform(self.rio_dataset.transform, inplace=True)
            rds.rio.to_raster(output_file_name)

        self.rio_dataset.close()
        self.dataset.close()
        os.remove(self.temp_output)
        self.temp_output = None
        self.rio_dataset = None
        self.dataset = None
        logging.info("Created: " + output_file_name)
        return

    def __str__(self):
        """
        Constructs string representation of the NetCDF dataset, with variable names and dimensional information
        """
        # Get the variable names in the dataset
        variable_names = list(self.dataset.variables.keys())

        # Construct the string representation
        str_repr = "NetCDF Dataset:\n"
        str_repr += "\n".join(variable_names)

        return str_repr


def main(infile: str, components: List[str], outfile: str):
    if outfile is None:
        base, _ = os.path.splitext(infile)
        base += "_with_components"
        outfile = base + '.tif'
    elif os.path.isdir(outfile):
        basename = os.path.basename(infile)
        base, _ = os.path.splitext(basename)
        basename = base + '.tif'
        outfile = os.path.join(outfile, basename)
    ds = NetCDFDataset()
    #print("testing")
    ds.read_abs_values(infile)
    logging.debug(str(ds))
    ds.add_components(components)
    logging.debug(str(ds))
    ds.compute_abs_values()
    logging.debug(str(ds))
    ds.close(outfile)


if __name__ == '__main__':
    #init_logging(level=logging.INFO, name="NetCDF")
    parser = argparse.ArgumentParser (description="Tool to combine components into a single NetCDF file")
    parser.add_argument("--input", "-in", "-i",
                        help="Path to the main NetCDF file containing absolute values",
                        default=None,
                        required=True)
    parser.add_argument("--components", "-c",
                        help="Path to the NetCDF files containing components",
                        nargs='+',
                        default=None,
                        required=True)
    parser.add_argument("--output", "-out", "-o",
                        help="Path to the file with the combined dataset",
                        default=None,
                        required=False)
    parser.add_argument("--verbose", "-v",
                        help="Verbosity level",
                        default=1,
                        type=int)

    args = parser.parse_args()
    if args.verbose == 0:
        logging.basicConfig(level=logging.WARNING, stream=sys.stdout)
    elif args.verbose == 1:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    else:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    main(args.input, args.components, args.output)


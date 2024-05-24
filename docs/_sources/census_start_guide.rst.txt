Working with the ``census`` Package
===================================

.. warning::
    
    This is the old documentation that prepared by Ben, we need to find the right place and merge it into the new documentation.


Running the Command Line Interface
----------------------------------

When ``census`` is installed, a command line utility (also named ``census``)
is automatically made available in your environment. Documentation on the CLI can be
accessed by running: ::

    census --help


An example run would look like this: ::

    census --var_file census_vars.yml -y 2009:2019 --geom tract -d population -i x --out ../data/census_tract_2009_2019.csv

This would take the variable definitions in ``census_vars.yml`` (``--var_file census_vars.yml``)
, process them from the API for census tracts (``--geom tract``) for 2009 - 2019 (``-y 2009:2019``),
calculate density per square mile for the "population" variable (``-d population``),
would not interpolate (``-i x``), and would write the created data frame to the
path specified by ``--out``.

Main Python Workflow
--------------------

All main functionality for this package is contained within the `DataPlan` object.
For detailed documentation on its methods, please see :ref:`assemble_data.py`.

The general workflow is as follows:

- Create your DataPlan Object (this one is for county data for 2000-2019): ::

    plan = census.DataPlan("census_vars.yml", "county", years = census.census_years(2000, 2019))

On creation, the object creates a plan for a series of API queries to calculate the desired
variables based on the passed in yaml file. Details on how to structure that yaml file can be found in
:doc:`census_yaml`.

- Make the API calls: ::

    plan.assemble_data()

This tells the DataPlan object to start making and combing all the specified API calls.

After this completes, the data is usable for analysis. However, it will only contain data for
years that are available through the US census. It also will not have any densities, or other
columns. Despite this, if you are interpolating or calculating densities, it is still
best practice for reproducuibility to save a copy of your data at this point. You can do that
by running ::

    plan.write_data("census_uninterpolated.csv").

After this, we can begin interpolation.

- Interpolate the data: ::

    plan.interpolate(min_year = 1999, max_year = 2019)

This will interpolate missing data using a weighted moving average model missing data for each
variable, for each geographic unit, for each year in the dataset. Since ACS data/Decennial data
is available for counties in 2000, and in 2009 onward, this will create data for 1999, and 2001-2008.
More information on the interpolation methods can be seen in the ``dorieh.utils`` package documentation.

- Calculate Densities: ::

    plan.calculate_densities(["population"], sq_mi = True)

This will calculate the density per square mile of the variable population within the
assembled data set. This can take some time to run, as it needs to get the area of each geographic
unit from the tigerweb API. Also note that due to limited data availability, the area may not
100% correspond to the area of the year in question.

- Write the data: ::

    plan.write_data("census_interpolated.csv")

Your data set is now complete and written to disk.


Shapefile Downloads
-------------------

In addition to the general processing workflow, the package also includes
a function for downloading Census geography shape files. Please see :ref:`tigerweb.py`
for documentation on the functions interacting with the Census geographic resources.


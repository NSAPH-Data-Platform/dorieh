Quick Start 
===========

Set up your environment (or activate it) using :ref:`Setting Up Environment` section. 

Census data comes from different resources, and they may have a different formats in different years. The current supported source of data includes:
    
    - ``acs``  American Community Survey
    - ``dec``  Data collected by the decennial census
    - ``pums`` Public use microdata sample (has not been implemented.)

The users need to get familiar with these data sources and their variables and tables names for each year. In the ``census`` package, one can check the available variables based on the provided year and data source. 

For example, in the following code we want to see all available variables for `acs1` dataset in 2011.

.. code-block:: python3
     
    from census.census_info import get_varlist

    varlist = get_varlist(2011, "acs1")
    print(f"{Number of downloaded variables: len(varlist)}")
    print(f"List of first 10 variables: ")
    varlist[1:10]

The results are according to the following:

.. code-block:: console

    Number of downloaded variables: 34450
    List of first 10 variables: 
    ['B19001B_014E',
     'C02014_002E',
     'B23023_070E',
     'B07007PR_019E',
     'B19101A_004E',
     'B24022_061E',
     'B19001B_013E',
     'C02014_003E',
     'B07007PR_018E']

There are 34450 different variables for acs1 data set in 2011. You can google "census acs1 2011 variable_name" to get more information about the variable, or you can use the following link pattern to see more information about the data.

.. code-block:: console

    https://api.census.gov/data/2011/acs/acs1/variables/B23023_070E.json

And as you can see, this variable is

     `estimate of total females with a disability worked in the past 12 months! Usually worked 1 to 14 hours per week!!48 and 49 weeks.`

.. note::

    Please note that selecting the correct variables for the research is beyond the scope of this package and this documentation. This package will work the best when you know what you need to download.

After deciding what variables you want to download, you need to create ``census_vars.yml`` file (read more :doc:`census_yaml`). Here is an example:

.. code-block:: console

    hispanic_count:
        2000:
            census:
                num: P004002

Let's say we want to download and review hispanic_count in 2000, for each state. We can use the following code to get the results.

.. code-block:: python3

    import yaml
    import census

    with open("census_vars.yml") as f:
        yaml_dict = yaml.load(f, Loader=yaml.FullLoader)

    my_var = census.VariableDev("count_hispanic", yaml_dict["hispanic_count"][2000])
    data = my_var.do_query(2000, "state")
    print(data)

.. note::

    Please note that the best way to download data is using ``DataPlan`` class. These are some internal examples to become familiar with the package. 

Now, let's say we want to download the same data with ``DataPlan`` class. DataPlan has numerous methods to conduct different analyses and filters on data. 


.. code-block:: python3

    import census

    plan = census.DataPlan("census_myvar_test.yml", geometry="state", years=census.census_years(2000,2000))
    plan.assemble_data()
    plan.data.head()

If you take a look at the results, you will see that the column names are according to your request rather than the original table on Census API.

.. code-block:: console

    state  year  hispanic_count
    01     2000  75830
    02     2000  25852
    04     2000  1295617
    05     2000  86866
    06     2000  10966556

Now, if we want to compute the percentage of Hispanic population we can change the yaml file according to the following:

.. code-block:: console

    hispanic_pct:
    2000:
        census:
            num: P004002
            den: P001001

And rerun the plan:

.. code-block:: python3

    import census

    plan = census.DataPlan("census_myvar_test.yml", geometry="state", years=census.census_years(2000,2000))
    plan.assemble_data()
    plan.data.head()

This time we get the following results:

.. code-block:: console

    state  year  hispanic_count
    01     2000  0.017052
    02     2000  0.041236
    04     2000  0.252526
    05     2000  0.032493
    06     2000  0.323768


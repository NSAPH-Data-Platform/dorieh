Utility to generate test queries
================================

.. toctree::
   :maxdepth: 2
   :glob:
   :hidden:

   dbt_runner
   gen_dbt_cwl

.. contents::
   :local:

Generates SQL script that can be used with :doc:`dbt_runner`.
These scripts are used by :doc:`gen_dbt_cwl`.

Usage
-----

::

      python -m dorieh.platform.dbt.create_test --script SCRIPT [SCRIPT ...]
            [--table TABLE]
            [--db DB]
            [--connection CONNECTION]
            [--autocommit]
            [-h]
            [--verbose]

Options:

.. list-table:: Options
   :widths: 25 25 50
   :header-rows: 1

   * - Option
     - Alias
     - Description
   * - ``--help``
     - ``-h``
     - Show this help message and exit
   * - ``--script SCRIPT [SCRIPT...]``
     - ``-s SCRIPT [SCRIPT...]``
     - Path to the file to write the test scripts
   * - ``--autocommit``
     -
     - Use autocommit, default: False
   * - ``--database DB``
     - ``--db DB``
     - Path to a database connection parameters file, default: database.ini (in the working directory
   * - ``--connection CONNECTION``
     - ``--connection_name CONNECTION``
     - Section in the database connection parameters file
   * - ``--table TABLE``
     - ``-t TABLE``
     - Name of the table to being tested, default: None
   * - ``--verbose``
     -
     - Verbose output, default: False

Details
-------

.. automodule:: dorieh.platform.dbt.create_test
   :members:
   :undoc-members:

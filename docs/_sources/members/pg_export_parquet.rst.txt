The pg_export_parquet Module
============================

This utility uses `PyArrow Library <https://arrow.apache.org/docs/python/index.html>`_
to write Parquet files. It is capable of writing very large files with hundreds of
billions of records.

To write huge files one should use *hard* partitioning to work around a memory leak in
the Arrow library.

It can export either a table of a result of an SQL query.


Usage
^^^^^

.. code-block::

    pg_export_parquet.py [-h] [--sql SQL] [--schema SCHEMA] [--table TABLE]
                            [--partition PARTITION [PARTITION ...]] --output
                            OUTPUT --db DB --connection CONNECTION
                            [--batch_size BATCH_SIZE] [--hard]


    options:
      -h, --help            show this help message and exit
      --sql SQL, -s SQL     SQL Query or a path to a file containing SQL query
      --schema SCHEMA       Export all columns for all tables in the given schema
      --table TABLE, -t TABLE
                            Export all columns a given table (fully qualified name
                            required)
      --partition PARTITION [PARTITION ...], -p PARTITION [PARTITION ...]
                            Columns to be used for partitioning
      --output OUTPUT, --destination OUTPUT, -o OUTPUT
                            Path to a directory, where the files will be exported
      --db DB               Path to a database connection parameters file
      --connection CONNECTION, -c CONNECTION
                            Section in the database connection parameters file
      --batch_size BATCH_SIZE, -b BATCH_SIZE
                            The size of a single batch
      --hard                Hard partitioning: execute separate SQL statement for
                            each partition (for writing huge files).

API
^^^

.. automodule:: dorieh.platform.util.pg_export_parquet
   :members:
   :undoc-members:


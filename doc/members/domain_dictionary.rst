The Data Dictionary Generation tool
===================================

Generating data dictionary
--------------------------

In Dorieh, one can define a data model, including tables
(or views and materialized views), columns, indices and
relations between tables (foreign keys) using
:doc:`Dorieh DSL <../Datamodels>`. The DSL also describes
how the original incoming data should be transformed to
create the eventual data structure.

The Data dictionary tool generates documentation for the data
elements (such as tables and columns) in the data model and data lineage
diagrams at the tables levels and at column levels for every column.

The output of the tool is described below.

Domain Dictionary Output
-------------------------
.. _domain-dictionary-output:

* Main table-level data lineage diagram showing the order of the
  data processing and the dependencies between tables.
* If the diagram is generated using SVG format, then every table
  is clickable, linked to a file with the table description.
* Every table description file includes verbal description, SQL or DDL
  used to create the table and the list of all columns in the table.
  Each column is linked to another file with detailed description
  for this column.
* Each column description file contains a description of the column
  and a lineage diagram for the column showing what columns in which tables
  have been used to compute the value of this column. The SVG
  diagram is clickable and every element is linked to the description
  file for the column.
* File, containing alphabetical list of all columns in all tables.
  For every column a list of tables in which the column is present
  is displayed. During the transformation process columns are
  transferred from one table to another, hence a column usually is present in
  multiple tables.


The tool first generates Markdown files that can be subsequently converted to HTML.

There are two modes for Markdown generation:

* Standalone mode, when Pandoc is used to generate HTML
* Sphinx mode designed to produce files that will be included in the Sphinx generated documentation

Usage
-----

::

    python -m dorieh.platform.dictionary.domain_dictionary
        [-h] [--fmt {none,png,gif,ps2,svg,cmapx,jpeg}]
        [--lod {full,none,min}]
        [--mode {standalone,sphinx}]
        [--output OUTPUT]
        yaml [yaml ...]

Positional arguments:

.. list-table:: Positional Arguments
   :widths: 20 80
   :header-rows: 1

   * - Argument
     - Description
   * - ``yaml``
     - Paths to YAML files with domain definitions

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
   * - ``--fmt {none,png,gif,ps2,svg,cmapx,jpeg}``
     - ``-f {none,png,gif,ps2,svg,cmapx,jpeg}``
     - Format of generated image, if 'none', then no image is generated
   * - ``--lod {full,none,min}``
     -
     - Level of details for column-level lineage documentation [#lodnote]_
   * - ``--mode {standalone,sphinx}``
     -
     - Documentation generation mode
   * - ``--output OUTPUT``
     - ``--of OUTPUT, -o OUTPUT``
     - Path to the main output file with Table-level data lineage diagram

.. [#lodnote]
   **Level of Details for ``--lod``:**

   - ``none``: No column-level lineage documentation or diagrams are generated. Only table-level diagrams and summaries are produced.
   - ``min``: Lineage graphs are generated only for derived columns. For columns that have no predecessors (i.e., is not derived from other columns), a markdown file is created, but no lineage diagram is generated. For columns with predecessors, both diagrams and markdown are generated as in ``full`` mode.
   - ``full``: All columns in all tables will have their lineage diagrams and markdown documentation generated, regardless of whether they have predecessors. This is the most comprehensive documentation mode.

Details
-------

.. automodule:: dorieh.platform.dictionary.domain_dictionary
   :members:
   :undoc-members:


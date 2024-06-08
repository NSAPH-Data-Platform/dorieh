# Core Platform Python Modules 

```{seealso}
[Python Module Index](modindex)
```

```{contents}
---
local:
---
```


## Package dorieh.platform

This package contains teh following modules used in subpackages:

* [](members/platform.rst) API to initialize logging and database connections
* [db](members/db.rst) is a PostgreSQL
  connection wrapper. It reads connection parameters from
  an `ini` file and connects to the database. It can
  transparently connect over **ssh tunnel** when required.
  See also [](DBConnections)
* [fips](members/fips.rst) US State FIPS codes, represented as Python dictionary
* [pg_keywords](members/pg_keywords.rst) PostgreSQL keywords, e.g.
  type names, etc.

## Package dorieh.platform.data_model
                                         
APIs for data modelling, loading and manipulations.
This subpackage focuses on generating code required to do the
actual processing. It uses the same Medallion architecture paradigm
as [Databricks](https://www.databricks.com/glossary/medallion-architecture).

The main concept is a knowledge domain, or
just a domain. Domain model is define in a YAML file as
described in the [documentation](Datamodels). A domain model
defines a graph of data transformations using intermediate
views, materialized views and tables (in this sense it 
is more flexible than 
[Databricks DLT model](https://www.databricks.com/product/delta-live-tables) 
that only uses materialized views).


The most important
module that processes the YAML definition of the domain
is [domain.py](members/domain). Another
module, [inserter](members/inserter)
handles parallel insertion of the data into domain tables.

Auxiliary modules perform various maintenance tasks.
Module [index_builder](members/index_builder)
builds indices for a given tables or for all
tables within a domain.
Module [utils](members/utils)
provides convenience function wrappers and defines
class DataReader that abstracts reading CSV and FST files.
In other words, DataReader provides uniform interface
to reading columnar files in two (potentially more)
different formats.


* [Domain class](members/domain.rst) Data modeling for a data domain
* [Inserter](members/inserter) API to parallel data loader
* [utils](members/utils) Miscellaneous data handling API

## Package dorieh.platform.loader
         
Command line utilities to manipulate data
Implements parallel loading .


* [](members/loader.rst)
* [Data Introspector](members/introspector) introspects columnar data to 
  infer the types of the columns
* [](members/data_loader.rst) Transfers data from file(s) to the database.
    Implements parallel loading of data into a PostgreSQL database and handling multiple file formats
    (CSV, FST, JSON, SAS, FWF). It is also responsible for loading DDL and creation of view,
    both virtual and materialized.
* [Project Loader](members/project_loader.rst) Recursively introspects and loads 
    data directory into the database
* [Index Builder](members/index_builder) Builds indices for a table or for all 
    tables in the data domain, reporting the progress
* [Database Activity Monitor](members/monitor) API and command line utility
    to monitor database activity, see [](MonitoringDB)
* [Vacuum](members/vacuum) Executes VACUUM command in the database to tune
    tables for better query performance
* [Common Configuration](members/common) options
    for working with the database
* [Loader Configurator](members/loader_config) Configuration options
    for data loader


## Package dorieh.platform.requests

Package `dorieh.platform.requests` 
contains some PoC-quality API that is
intended to be used for fulfilling user requests. Its
development is currently put on hold.


* [HDF5 Export](members/hdf5_export.rst) API and utility to export result 
    of quering the database in HDF5 format
* [Query class](members/query) API and utility to generate SQL query 
    based on a YAML query specification

## Package dorieh.platform.utils

Miscellaneous tools and APIs

* [CWL Output collector](members/cwl_collect_outputs) Command line 
    utility to copy outputs from a CWL tool or sub-workflow into 
    the calling workflow
* [Blocking Executor Pool](members/executors) Blocking executor pool to 
    avoid memory overflow with long queues
* [Localhost for Airflow](members/net) Overrides host resolver for Airflow, so
    it can use localhost
* [JSON to/from Table converter](members/pg_json_dump) A command line utility 
    to import/export JSON files as database tables
* [Resource finder](members/resources) An API to look for resources
    in Python packages. See [Resources section](platform.md#resources).
* [sas_explorer](members/sas_explorer) A tool to print metadata of a SAS 
    SAS7BDAT file
* [SSA to FIPS Mapping](members/ssa2fips) A utility to create in-database 
    mapping table between SSA and FIPS codes 
* [ZIP to FIPS mappings](members/zip2fips) A utility to download ZIP to 
    FIPS mapping from HUD site

```{seealso}
 [Python Module Index](modindex)
```
 
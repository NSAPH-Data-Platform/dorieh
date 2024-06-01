# Dorieh Core Data Platform

[Documentation Home](home)

```{toctree}
---
maxdepth: 4
hidden: 
---
Datamodels
DataLoader
ProjectLoader
TerritorialCodes
SampleQuery
UserRequests
SQLDocumentation
```

```{contents}
---
local:
---
```

## Core platform overview

The data platform provides generic functionality for Dorieh Data Platform
with APIs and command line utilities dependent on the infrastructure
and the environment. For instance, its components assume presence of PostgreSQL
DBMS (version 13 or later) and CWL runtime environment.

Some mapping (or crosswalk) tables are also included in the Core
Platform module. These tables include between different
territorial codes, such as USPS ZIP codes, Census ZCTA codes,
FIPS codes for US states
and counties, SSA codes for codes for US states
and counties. See more information in the
[Mapping between different territorial codes](https://nsaph-data-platform.github.io/nsaph-platform-docs/common/core-platform/doc/TerritorialCodes.html)

## Tool Examples

Examples of tools included in this package are:

* [Universal Data Loader](members/data_loader)
* A [utility to monitor progress of long-running database](members/monitor) processes like indexing.
* A [utility to infer database schema and generate DDL](members/introspector) from a CSV file
* A [utility to link a table to GIS](members/link_gis) from a CSV file
* A [wrapper around database connection to PostgreSQL](#module-database-connection-wrapper)
* A [utility to import/export JSONLines](members/pg_json_dump) files into/from PostgreSQL
* A [utility to export Parquet files](members/pg_export_parquet) files from PostgreSQL
* An [Executor with a bounded queue](members/executors)

(core-prj-struct)=
## Project Structure 

**The package is under intensive development, the project structure is in flux**

Top level directories are:

    - doc
    - resources
    - src
    - examples
    - docker

Doc directory contains documentation.

Resource directory contains resources that must be loaded in
the data platform for its normal functioning. For example,
they contain mappings between US states, counties, fips and zip codes.
See details in [Resources](#resources) section.

Src directory contains software source code.
See details in {ref}`core-software-sources` section.

(core-software-sources)=
### Software Sources 

The directories under sources are:

    - cwl
    - python
    - sql

They are described in more details in the corresponding sections.
Here is a brief overview:

* **cwl** contains reusable workflows, packaged as tools
  that can and should be used by
  Dorieh pipelines. Examples of such tools 
  are: introspection of CSV files, indexing tables, linking
  tables with GIS information for easy mapping, creation of a
  Superset datasource.
* **sql** contains PostgreSQL procedures and functions
  implemented in the PostgreSQL dialect of SQL/DDL and PL/pgSQL language
* **python** contains Python code. See [more details](#python-packages).

### Python packages

#### dorieh.platform Package

This is the main package containing the majority of the code.
Modules and subpackages included in `dorieh.platform` package are described below.

##### Subpackage for Data Modelling

* `dorieh.platform.data_model`

Implements version 2 of the data modelling toolkit.

Version 1 was focused on loading into the database already
processed data saved as flat files. It inferred data
model from the data files structure and accompanied README
files. The inferred data model is converted to database schema
by generating appropriate DDL.

Version 2 focuses on generating code required to do the
actual processing. The main concept is a knowledge domain, or
just a domain. Domain model is define in a YAML file as
described in the [documentation](Datamodels). The main
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

##### Module Database Connection Wrapper

* `dorieh.platform.db`

Module [db](members/db) is a PostgreSQL
connection wrapper. It reads connection parameters from
an `ini` file and connects to the database. It can
transparently connect over **ssh tunnel** when required.

##### Loader Subpackage

* `dorieh.platform.loader`

A set of utilities to manipulate data.

Module [data_loader](members/data_loader)
Implements parallel loading data into a PostgreSQL database.
It is also responsible for loading DDL and creation of view,
both virtual and materialized.

Module [index_builder](members/index_builder)
is a utility to build indices and monitor the build progress.

##### Subpackage to describe and implement user requests [Incomplete]

* `dorieh.platform.requests`

Package `dorieh.platform.requests` contains some code that is
intended to be used for fulfilling user requests. Its
development is currently put on hold.

Module [hdf5_export](members/hdf5_export) exports
result of SQL query as an HDF5 file. The structure of the HDF5 is
described by a YAML request definition.

Module [query](members/query) generates SQL query
from a YAML request definition.

##### Subpackage with miscellaneous utilities

* `dorieh.platform.util`

Package `dorieh.platform.util` contains:

* Support for packaging [resources](#resources)
  in two modules [resources](members/resources)
  and [pg_json_dump](members/pg_json_dump). The
  latter module imports and exports PostgreSQL (pg) tables
  as JSONLines format.
* Module [net](members/net) contains
  one method resolving host to `localhost`. This method is
  required by Airflow.
* Module [executors](members/executors)
  implements a
  [ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor)
  with a bounded queue. It is used to prevent out of memory (OOM)
  errors when processing huge files (to prevent loading
  the whole file into memory before dispatching it for processing).

### Resources

Resources are organized in the following way:

```
- ${database schema}/
    - ddl file for ${resource1}
    - content of ${resource1} in JSON Lines format (*.json.gz)
    - ddl file for ${resource2}
    - content of ${resource2} in JSON Lines format (*.json.gz)
```

Resources can be packaged when a
[wheel](https://pythonwheels.com/)
is built. Support for packaging resources during development and
after a package is deployed is provided by
[resources](members/resources) module.

Another module, [pg_json_dump](members/pg_json_dump),
provides support for packaging tables as resources in JSONLines
format. This format is used natively by some DBMSs.

### SQL Utilities

Utilities, implementing the following:

* [Functions](members/utils.sql):
    * Counting rows in tables
    * Finding a name of the column that contains year from most tables used in data platform
    * Creating a hash for [HLL aggregations](https://en.wikipedia.org/wiki/HyperLogLog)
* Procedure:
    * [A procedure](members/utils.sql) granting `SELECT` privileges
      to a user on all NSAPH tables
    * [A procedure to rename indices](members/rename_indices.sql)
* Set of SQL statements:
    [to map tables from another database](members/map_to_foreign_database.ddl)
    This can be used to map public tables available to anybody
    to a more secure database, containing health data
* [Tables and functions](members/zip2fips.sql) to 
    [map between different territorial codes](#territorial-codes-mappings), 
    including USPS ZIP codes, Census ZCTA codes, 
    FIPS codes for US states
    and counties, SSA codes for codes for US states
    and counties. 

## Territorial Codes Mappings

An important part of the data platform is the mappings between different
territorial codes, such as USPS ZIP codes, Census ZCTA codes,
FIPS codes for US states and counties, SSA codes for codes for US states
and counties. See more information in the
[Mapping between different territorial codes](TerritorialCodes)
page.

(core-soft-idx)=
## Documentation Indices 

* [genindex](genindex)
* [modindex](modindex)

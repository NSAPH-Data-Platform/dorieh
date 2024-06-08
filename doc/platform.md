# Dorieh Core Data Platform

[Documentation Home](home)

```{toctree}
---
maxdepth: 4
hidden: 
---
Datamodels
DBConnections
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
and counties, SSA codes for US states
and counties. See more information in the
[Mapping between different territorial codes](https://nsaph-data-platform.github.io/nsaph-platform-docs/common/core-platform/doc/TerritorialCodes.html)

See also: [](DBConnections).


## Tool Examples

Examples of tools included in this package are:

* [Universal Data Loader](members/data_loader)
* A [utility to monitor progress of long-running database](MonitoringDB) processes like indexing.
* A [utility to infer database schema and generate DDL](members/introspector) from a CSV file
* A [utility to link a table to GIS](members/link_gis) from a CSV file
* A [wrapper around database connection to PostgreSQL](members/db)
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

Modules and subpackages included in `dorieh.platform` package are 
described [here](CoreLibrary.md).

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
      to a user on all tables created or managed by Dorieh platform
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

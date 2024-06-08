# Data Modelling for Dorieh Data Platform

**How data models are defined and handled**

```{toctree}
---
maxdepth: 4
hidden: 
---
DataModellingExtensions
Medicare
Medicaid
```


```{contents}
---
local:
---
```

## Introduction to data modelling for NSAPH Data Platform

Data models consist of database tables, relations between them
(e.g. foreign keys), indices and conventions that govern things
like namings and roles of specific columns.

We assume that a model is defined for a specific knowledge domain.
Between domains, data can be linked based on the naming conventions
for columns. For instance, a column named `zipcode` means the US zip
code in any domain and thus can be used for linkages and aggregations.

Currently, we are in the process of defining data models for the
following domains

* Medicaid
* Medicare
* EPA
* Census
* Climate (gridMET data)

Extended functionality for data transformations is provided by
[Data Modelling Extensions](DataModellingExtensions) that are used by 
[Medicare processing workflow](Medicare)  and 
[Medicaid processing workflow](Medicaid). These functionalities include:

* Combining data from different tables (approximate **union** operation)
* Casting data types
* Validating consistency of data across tables

See also: [](DBConnections).

## Domain

Handling domains is implemented by the
[Domain](members/domain) class.

For each domain, its data model is defined by a YAML file in
the `src/yml` directory.

Each model is represented by a "forest": a set of treelike
structures of tables. It can contain one or several root tables

Domain should be the first entry in the YAML file:

```yaml
my_domain:
```

The following parameters can be defined fro domain:


| Parameter    | Required? | Description                                                                                                                                                |
|--------------|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| schema       | yes       | Database schema, in which all tables are generated                                                                                                         |
| schema.audit | no        | Database schema for tables containing audit logs of data ingestion, including corrupted, duplicate and inconsistent records                                |
| index        | no        | Default indexing policy for this domain. This policy is used for tables that do not define their own indexing policy                                       |
| tables       | yes       | list of table definitions                                                                                                                                  |
| description  | no        | description of this domain to be included in auto-generated documentation                                                                                  |
| reference    | no        | URL with external documentation                                                                                                                            |
| header       | no        | Boolean value, passed to CSV loader. Describes input source rather than data model itself                                                                  |
| quoting      | no        | One of the following values: QUOTE_MINIMAL (or MINIMAL), QUOTE_ALL (or ALL), QUOTE_NONNUMERIC (or NONNUMERIC), QUOTE_NONE (or NONE), passed to CSV loader. Describes input source rather than data model itself. Numeric values are accepted for compatibility (QUOTE_MINIMAL=0, QUOTE_ALL=1, QUOTE_NONNUMERIC=2, QUOTE_NONE=3)  |

## Table

The following parameters can be defined for a table:

| Parameter          | Required? | Description                                                                                                                                 |
|--------------------|-----------|---------------------------------------------------------------------------------------------------------------------------------------------|
| type               | no        | view / table                                                                                                                                |
| hard_linked        | no        | Denotes that the table is an integral part of parent table rather than a separate table with a many-to-one relationship to the parent table |
| columns            | yes       | list of column definitions                                                                                                                  |
| indices or indexes | yes       | dictionary of multi-column indices                                                                                                          |
| primary_key        | yes       | list of column names included in the table primary key                                                                                      |
| children           | no        | list of table definitions for child tables of this table                                                                                    |
| description        | no        | description of this domain to be included in auto-generated documentation                                                                   |
| reference          | no        | URL with external documentation                                                                                                             |
| invalid.records    | no        | [action](#invalid-record) to be performed upon encountering an invalid record (corrupted, incomplete, duplicate, etc.)                      |
| create             | no        | If the table or view should be created from existing database objects, see [detailed description](#create-statement)                        |

### Create statement

Describes how a table or a view should be created.

| Parameter | Required?             | Description                                                                                                                                                                                                                             |
|-----------|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| type      | no                    | view / table                                                                                                                                                                                                                            |
| select    | no                    | columns to put in `SELECT` clause of CREATE statement                                                                                                                                                                                   |
| from      | no                    | What to put into `FROM` clause                                                                                                                                                                                                          |
| group by  | no                    | What to put into `GROUP BY` clause                                                                                                                                                                                                      |
| populate  | no, default is `True` | If `False`, then a condition that can never be satisfied will be added as `WHERE` clause, ehnce an empty table will be created that can be populated later. This is mostly used when additional triggers needed for population process. |

### Invalid Record

By default, an exception is raised if an invalid
record is encountered during data ingestion. However,
it is possible to override this behaviour by instructing
the data loader to either ignore such records or put them
in a special audit table.

| Parameter   | Required? | Description                                                               |
|-------------|-----------|---------------------------------------------------------------------------|
| action      | yes       | Action to be performed: `INSERT` or `IGNORE`                              |
| target      | yes/no    | For action INSERT - a target table                                        |
| description | no        | description of this domain to be included in auto-generated documentation |
| reference   | no        | URL with external documentation                                           |

## Column

| Parameter   | Required? | Description                                                                                                                       |
|-------------|-----------|-----------------------------------------------------------------------------------------------------------------------------------|
| type        | yes       | Database type                                                                                                                     |
| source      | no        | [source](#source) of the data                                                                                                     |
| requires    | no        | List of tables and views required to compute this column. Should be used if `source` is a SQL statement referencing other tables. |
| index       | no        | Override default to build an index based on this column. Possible values: true/false/dictionary. See [index](#index)              |
| description | no        | description of this domain to be included in auto-generated documentation                                                         |
| reference   | no        | URL with external documentation                                                                                                   |

Beside "normal" columns, when the value is
directly taken from a column in a tabular input source,
there are three types of special columns:

* Computed columns
* Generated columns
* Transposed columns (i.e., when multiple columns of a single record are converted to multiple records)

Special columns must have their `source` defined. If a column
name in input source is different from a column name in the
database, such column also must define `source`.

### Source

Source must be defined for special columns and for columns
with the name in the database different from the name
in the input source.

| Parameter   | Required? | Description                                                    |
|-------------|-----------|----------------------------------------------------------------|
| column name | no        | A column name in the incoming tabular data                     |
| type        | no        | Types: `generated`, `multi_column`, `range`, `compute`, `file` |
| range       | no        |                                                                |
| code        | no        | Code for generated and computed columns                        |
| columns     | no        |                                                                |
| parameters  | no        |                                                                |
                   

### Index

The value for `index` key can be a simple boolean `true` or `false`. If additional parameters 
are required, the value can be a dictionary with the following keys. For the explanation
of options like *using* or *include*, see 
[PostgreSQL Documentation](https://www.postgresql.org/docs/current/sql-createindex.html).

| Parameter                    | Required? | Description                                                                                                                                                                                             |
|------------------------------|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name                         | no        | A custom index name, if omitted the name will be generated                                                                                                                                              |
| using                        | no        | The indexing method, the default is BTREE                                                                                                                                                               |
| include                      | no        | Additional columns to include with index                                                                                                                                                                |
| required_before_loading_data | no        | Adding this key tells the generator that this index must be created before the table is populated. Otherwise, to improve performance, indices might be created after a table is popualted with all data |


### Generated columns

Generated columns are columns that are not present in the source
(e.g. CSV or FST file) but whose value
is automatically computed using other columns values,
or another deterministic expression **inside the database**.

From [PostgreSQL Documentation](https://www.postgresql.org/docs/current/ddl-generated-columns.html):

>Theoretically, generated columns are for columns
>what a view is for tables. There are two kinds of
>generated columns: stored and virtual. A stored
>generated column is computed when it is written
>(inserted or updated) and occupies storage as if
>it were a normal column. A virtual generated column
>occupies no storage and is computed when it is read.
>Thus, a virtual generated column is similar to a
>view and a stored generated column is similar to a
>materialized view (except that it is always updated automatically).

>However, **PostgreSQL currently implements only STORED generated columns**.

### Computed columns

Computed columns are columns that are not present in the source
(e.g. CSV or FST file) but whose value is computed
using provided Python code by the Universal Database Loader.
They use the values of other columns in the same record and can call
out to standard Python functions.

The columns used for computation are listed in either `columns`
or `parameters` sections. Column names are names of the original
columns in the data file. To reference columns in the
database use parameters.
Referenced them by a number in curly brackets in the compute code.


Here is an example of a computed column:

```yaml
- admission_date:
    type: "DATE"
    source:
        type: "compute"
        columns:
            - "ADMSN_DT"
        code: "datetime.strptime({1}, '%Y%m%d').date()"
```

Here in `code` the pattern `{1}` is replaced with the name of the
first (and only) column in the list: `ADMSN_DT`.

Another example, using database columns:

```yaml
- fips5:
    source:
      type: "compute"
      parameters:
        - state
        - residence_county
      code: "fips_dict[{1}] * 1000 + int({2})"
```

Here, `{1}` references the value that would be inserted into the
table column `state` and `{2}` references the value that
would be inserted into the table column `residence_county`.

### File columns

File columns are of type `file`. They store the name of the file,
from which the data has been ingested.

### Record columns

Record columns are of type `record`. They store the sequential
index of the record (line number) in the file,
from which the data has been ingested.

### Transposing columns
                                          
Columns can be unnested (aka exploded) or collapsed. 

Exploding might be for example, useful if there is a separate column for every month. 
The easiest way to do it is to combine these monthly columns into an array and then 
use `unnest` function.

### Wildcards

To make it easier to work with similarly named columns, Dorieh supports wildcards.
Wildcard expression starts with `$` followed by a single letter. Values are provided 
in square braces that follow a wildcard. 

Example:

```yaml
  - diag[$n=1:25]:
      type: varchar
      optional: true
      source:
        - dgnscd$n
```

Will be expanded to 25 columns named `diag1`, `diag2`, `diag25`.

## Multi-column indices

Multi-column indices of a table are defined in `indices` section
(spelling `indexes` is also acceptable). This is a dictionary with an
index name as a key and its definition as the value. At the very minimum,
the definition should include the list of the columns to be used in the
index.

Index definition can also include
[index type](https://www.postgresql.org/docs/current/indexes-types.html)
(e.g. btree, hash, etc.)  and data to be included with the index.

| Parameter | Required? | Description                                         |
|-----------|-----------|-----------------------------------------------------|
| columns   | yes       | A list of columns to include in the index           |
| using     | no        | The indexing method, the default is BTREE           |
| include   | no        | Additional columns to include with index            |
| unique    | no        | Specifies that the index defines a unique constrain |
                                                      
Example:

 ```yaml
    indices:
      adm_ys_idx:
        columns:
          - state
          - year
      adm_ys_iso_idx:
        columns:
          - state_iso
          - year
        include:
          - bene
```



## Generation of the database schema (DDL)

From a domain YAML file, the database schema is
generated in the form of PostgreSQL dialect of DDL.

The main class responsible for the generation of DDL is
[Domain](members/domain)

## Indexing policies

* **explicit**. Indices are only created for columns that define an index
* **all** Indices are only created for all columns
* **selected** Indices are only created for columns matching certain pattern 
  (defined in `index_columns` variable of [model](members/model)) module
* **unless excluded** Indices are only created for all columns not explicitly excluded

## Linking with nomenclature

### US States

Database includes a table with codes for US states. It is taken from:

<https://www.nrcs.usda.gov/wps/portal/nrcs/detail/national/technical/nra/nri/results/?cid=nrcs143_013696>

The data leaves locally in [fips.py](members/fips)

County codes:

<https://www.nber.org/research/data/ssa-federal-information-processing-series-fips-state-and-county-crosswalk>

## Ingesting data

The following command ingests data into a table and all hard-linked
child tables:

```
    usage: python -u -m dorieh.platform.data_model.model2 [-h] [--domain DOMAIN]
                [--table TABLE] [--data DATA]
                [--reset] [--autocommit] [--db DB] [--connection CONNECTION]
                [--page PAGE] [--log LOG] [--limit LIMIT] [--buffer BUFFER]
                [--threads THREADS]

    optional arguments:
    -h, --help              show this help message and exit
    --domain DOMAIN         Name of the domain
    --table TABLE, -t TABLE Name of the table to load data into
    --data DATA             Path to a data file or directory. Can be a single CSV,
                            gzipped CSV or FST file or a directory recursively
                            containing CSV files. Can also be a tar, tar.gz (or
                            tgz) or zip archive containing CSV files
    --pattern PATTERN       pattern for files in a directory or an archive, e.g.
                            `**/maxdata_*_ps_*.csv`
    --reset                 Force recreating table(s) if it/they already exist
    --incremental           Commit every file and skip over files that have
                            already been ingested
    --autocommit            Use autocommit
    --db DB                 Path to a database connection parameters file
    --connection CONNECTION Section in the database connection parameters file
    --page PAGE             Explicit page size for the database
    --log LOG               Explicit interval for logging
    --limit LIMIT           Load at most specified number of records
    --buffer BUFFER         Buffer size for converting fst files
    --threads THREADS       Number of threads writing into the database
```

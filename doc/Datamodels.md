# Data Modeling for Dorieh Data Platform

**How data models are defined and handled**

This page is the authoritative reference for the core Dorieh
data-modeling DSL: the YAML directives understood by the
[Domain](members/domain) DDL generator and the Universal Database
Loader. Additional directives, used to combine heterogeneous
per-year tables into federated views, are documented separately in
[Data Modeling Extensions](DataModellingExtensions.md).

```{toctree}
---
maxdepth: 4
hidden: 
---
DataModellingExtensions
```

The DSL in use — worked models and tooling documented elsewhere:

* [Medicare: Building a Data Warehouse from ResDac Files](Medicare.md) and
  [Medicaid](Medicaid.md) — production-scale models written in this DSL
* [Data dictionary and lineage for Medicare processing](MedicareLineage.md)
* [The Data Dictionary Generation tool](members/domain_dictionary.rst)


```{contents}
---
local:
---
```

## Introduction to data modeling for Dorieh Data Platform

Data models consist of database tables, relations between them
(e.g. foreign keys), indices and conventions that govern things
like namings and roles of specific columns.

We assume that a model is defined for a specific knowledge domain.
Between domains, data can be linked based on the naming conventions
for columns. For instance, a column named `zipcode` means the US zip
code in any domain and thus can be used for linkages and aggregations.

Dorieh ships data models for the following domains:

* Medicaid
* Medicare
* EPA
* Census
* Climate (gridMET data)
* Exposure (Air pollution data)

Extended functionality for data transformations is provided by
[Data Modeling Extensions](DataModellingExtensions) that are used by 
[Medicare processing workflow](Medicare)  and 
[Medicaid processing workflow](Medicaid). These functionalities include:

* Combining data from different tables (approximate **union** operation)
* Casting data types
* Composing checks that validate consistency of data across tables
  (there is no single directive; see
  [the extensions page](DataModellingExtensions.md#validating-consistency-of-data-across-tables))

See also: [](DBConnections).

## Domain

Handling domains is implemented by the
[Domain](members/domain) class.

For each domain, its data model is defined by a YAML file. The model
files shipped with Dorieh live in the `models` subdirectory of the
Python package they belong to, under `src/python/dorieh/`. For
example, the Medicare model is
[src/python/dorieh/cms/models/medicare.yaml](https://github.com/ForomePlatform/dorieh/blob/main/src/python/dorieh/cms/models/medicare.yaml)
and the Medicaid model is
`src/python/dorieh/cms/models/medicaid.yaml`; the model used by the
climate tutorial is `doc/tutorial/climate/example1_model.yml`. There
is no requirement to keep model files in any particular directory:
every tool that consumes a model takes the path to the YAML file as
an argument, and some tools (such as the Project Loader) can generate
a starter model file by introspecting the data.

Each model is represented by a "forest": a set of treelike
structures of tables. It can contain one or several root tables.

Domain should be the first entry in the YAML file:

```yaml
my_domain:
```

The following parameters can be defined for a domain:


| Parameter    | Required? | Description                                                                                                                                                |
|--------------|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| schema       | yes       | Database schema, in which all tables are generated                                                                                                         |
| schema.audit | no        | Database schema for tables containing audit logs of data ingestion, including corrupted, duplicate and inconsistent records                                |
| index        | no        | Default [indexing policy](#indexing-policies) for this domain. This policy is used for tables that do not define their own indexing policy                                       |
| tables       | yes       | list of table definitions                                                                                                                                  |
| description  | no        | description of this domain to be included in auto-generated documentation                                                                                  |
| reference    | no        | URL with external documentation                                                                                                                            |
| header       | no        | Boolean value, passed to CSV loader. Describes input source rather than data model itself                                                                  |
| quoting      | no        | One of the following values: QUOTE_MINIMAL (or MINIMAL), QUOTE_ALL (or ALL), QUOTE_NONNUMERIC (or NONNUMERIC), QUOTE_NONE (or NONE), passed to CSV loader. Describes input source rather than data model itself. Numeric values are accepted for compatibility (QUOTE_MINIMAL=0, QUOTE_ALL=1, QUOTE_NONNUMERIC=2, QUOTE_NONE=3)  |

## Table

The following parameters can be defined for a table:

| Parameter          | Required? | Description                                                                                                                                 |
|--------------------|-----------|---------------------------------------------------------------------------------------------------------------------------------------------|
| type               | no        | Ignored at the table level; the object kind (table / view / materialized view) is determined by `create.type` (see [Create statement](#create-statement))     |
| hard_linked        | no        | Denotes that the table is an integral part of parent table rather than a separate table with a many-to-one relationship to the parent table |
| columns            | yes*      | list of column definitions (may be omitted for tables fully defined by their `create` statement)                                            |
| indices or indexes | no        | dictionary of multi-column indices                                                                                                          |
| primary_key        | see below | list of column names included in the table primary key                                                                                      |
| children           | no        | list of table definitions for child tables of this table                                                                                    |
| description        | no        | description of this table to be included in auto-generated documentation                                                                   |
| reference          | no        | URL with external documentation                                                                                                             |
| invalid.records    | no        | [action](#invalid-record) to be performed upon encountering an invalid record (corrupted, incomplete, duplicate, etc.)                      |
| create             | no        | If the table or view should be created from existing database objects, see [detailed description](#create-statement)                        |

`primary_key` is optional in general, but it is required whenever
Dorieh needs to know the identity of a row:

* for tables ingested from files by the Universal Database Loader
  (the loader uses the primary key to detect records with missing
  key values);
* for tables that have child tables (the parent's primary key becomes
  the foreign key of every child table);
* for tables that define [invalid.records](#invalid-record)
  validation.

For views created with a `group by` clause the primary key is derived
automatically from the grouping columns (see
[Create statement](#create-statement)).

### Create statement

Describes how a table or a view should be created. In the vocabulary
of
[The Dorieh approach](concepts.md#dataset-operators-and-field-construction-operators),
every table or view with a `create` clause is a dataset operator.

| Parameter         | Required?             | Description                                                                                                                                                                                                                             |
|-------------------|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| type              | no                    | `table` (default) / `view` / `materialized view`                                                                                                                                                                                        |
| select            | no                    | columns to put in `SELECT` clause of CREATE statement. When `select` is used, `type` must also be given explicitly                                                                                                                       |
| from              | no                    | What to put into `FROM` clause: a single table or view, two relations combined with the literal keyword `natural join` (see below), or a list of table name patterns for a [federated view](DataModellingExtensions.md)                  |
| group by          | no                    | List of columns to put into `GROUP BY` clause. Also adds a `NOT NULL` filter for every grouping column and derives the primary key of the view (see below)                                                                              |
| nullable group by | no                    | List of columns to put into `GROUP BY` clause. Unlike `group by`, keeps records with NULL values in the grouping columns and does not derive a primary key (see below)                                                                  |
| populate  | no, default is `True` | If `False`, then a condition that can never be satisfied will be added as `WHERE` clause, hence an empty table will be created that can be populated later. This is mostly used when additional triggers are needed for the population process. |

The value of `type` is inserted verbatim into the generated
`CREATE ...` statement, hence `materialized view` is fully supported
alongside `table` and `view`. Both the climate tutorial model
(`gold_temperature_by_state` in `example1_model.yml`) and the Medicare
model (`_ps`, `qc_enrollments` and `qc_admissions` in `medicare.yaml`)
use materialized views.

#### Natural join in `from`

When `create` contains both `select` and `from`, the value of `from`
may be two relations combined with the literal keyword
`natural join`. The DDL generator splits the clause on this keyword,
qualifies each relation with the domain schema, and merges the column
definitions of both parent relations into the new table or view. Note
that the whole `from` clause is folded to lower case, so use
lower-case relation names with this feature. The Medicare model uses
it to combine beneficiary-level and enrollment-level data for quality
control:

```yaml
    qc_enrl_bene:
      create:
        type:  view
        select: '*'
        from: enrollments natural join beneficiaries
```

If `from` is a list of table name patterns (or a single pattern
containing `*`), the core DDL generator skips the table: such
federated views are built by the
[Data Modeling Extensions](DataModellingExtensions.md) tooling.

#### Group by and nullable group by

`group by` and `nullable group by` apply to views and materialized
views whose columns are defined by the `columns` list (that is,
without a `select` clause in `create`). A plain `group by` has two
side effects beyond emitting the `GROUP BY` clause:

* a `WHERE` clause is added requiring every grouping column to be
  `NOT NULL`, so records with missing keys are excluded from the
  view;
* the grouping columns are recorded as the primary key of the view in
  the model (mapped through column `source` definitions when the view
  renames a column), and this derived primary key is used wherever
  the primary key is needed — for example, as the foreign key linking
  child tables.

`nullable group by` emits only the `GROUP BY` clause: records with
NULL values in the grouping columns are kept (SQL `GROUP BY` places
them in a common NULL group per key), and no primary key is derived. This is
used for quality-control aggregates where NULL is a legitimate group,
e.g. in `qc_enrollments` and `qc_admissions` in `medicare.yaml`.

### Invalid Record

By default, an invalid record encountered during data ingestion
causes an error: a record violating the primary key raises a database
error, and a record with a missing primary key value is rejected by
the loader with a warning. The `invalid.records` directive overrides
this behaviour by instructing the platform to either silently discard
such records or journal them in a special audit table.

| Parameter   | Required? | Description                                                                  |
|-------------|-----------|-------------------------------------------------------------------------------|
| action      | yes       | Action to be performed: `INSERT` (journal in an audit table) or `IGNORE` (discard). Case-insensitive |
| target      | yes/no    | For action INSERT - the target audit table, see below                        |
| description | no        | description of this action to be included in auto-generated documentation |
| reference   | no        | URL with external documentation                                           |

The `target` value is a dictionary with two optional keys, `schema`
and `table`. If `schema` is omitted, the domain schema is used; if
`table` is omitted, the audit table gets the same name as the table
being validated. A value starting with `$` is a reference to a
top-level domain parameter: for example, in `medicare.yaml` the
`admissions` table declares

```yaml
              invalid.records:
                action: "INSERT"
                target:
                  schema: $schema.audit
```

which journals invalid admission records into
`medicare_audit.admissions` (`schema.audit` is defined as
`medicare_audit` for the domain, and the table name defaults to
`admissions`).

#### Validation checks and journaling

The validation machinery is generated for a child table that defines
its own `primary_key`; the primary key of the parent table serves as
the implicit foreign key. The DDL generator emits a
`BEFORE INSERT` trigger (with a PL/pgSQL function named
`{schema}.validate_{table}()`) that performs three checks on each
incoming row, in this order:

1. **Primary key integrity**: if any primary-key column of the new
   row is NULL, the row fails with reason `PRIMARY KEY`;
2. **Consistency across records (referential integrity)**: if the
   parent table contains no row matching the new row's foreign-key
   columns, the row fails with reason `FOREIGN KEY`;
3. **Elimination of duplicates**: if the table already contains a row
   with the same primary key values, the new row fails with reason
   `DUPLICATE`.

A failing row is never inserted into the main table. What happens to
it depends on `action`:

* with `IGNORE` it is silently discarded;
* with `INSERT` it is journaled in the audit table.

For action `INSERT`, the audit table is created automatically in the
target schema. It contains the same data columns as the main table —
including generated columns, which compute their values in the audit
table as well — but without the primary key or other constraints, so
that any failing row can be stored. Three bookkeeping columns are
added:

| Column      | Type                                | Content                                                                     |
|-------------|-------------------------------------|------------------------------------------------------------------------------|
| REASON      | VARCHAR(16)                         | Which check failed: `PRIMARY KEY`, `FOREIGN KEY` or `DUPLICATE`             |
| REFCTID     | TID                                 | For `DUPLICATE`: the physical row id (`ctid`) of the retained row in the main table that the journaled row collided with |
| recorded_at | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | When the row was journaled                                                  |

The generator also indexes the audit table: on `REASON`, on
`REFCTID`, and, for every data column that would be indexed in the
main table, both a single-column index and a composite
`(REASON, column)` index.

#### The quality column

The `quality` column is not created automatically. For every table
that is populated from another relation (a `create` statement with
`select`/`from` and `populate` not set to `False`) and whose
`invalid.records` action is `INSERT`, Dorieh generates an
`UPDATE ... SET quality` statement after the table is populated. Such
a table must therefore declare a `quality` column, as the
`admissions` table in `medicare.yaml` does:

```yaml
                - quality:
                    type: "VARCHAR(12) DEFAULT 'PASS'"
```

Declaring the column satisfies the generated statement; it does not
gate its generation. The `UPDATE`
statement back-annotates the retained rows: every row of the
main table whose `ctid` is recorded as `REFCTID` in the audit table
with reason `DUPLICATE` gets `quality = 'DUPLICATE'`, while
unaffected rows keep the declared default (`'PASS'`). In other words,
`quality` marks the kept counterpart of every journaled duplicate, so
that both sides of a collision can be found. This update is emitted
both when the table is populated on creation and by the generated
INSERT ... SELECT population statement.

## Column

In the vocabulary of
[The Dorieh approach](concepts.md#dataset-operators-and-field-construction-operators),
every column definition with a `source` is a field construction
operator.

| Parameter   | Required? | Description                                                                                                                       |
|-------------|-----------|-----------------------------------------------------------------------------------------------------------------------------------|
| type        | no        | Database type. If omitted, defaults to `VARCHAR`                                                                                  |
| source      | no        | [source](#source) of the data                                                                                                     |
| requires    | no        | List of tables and views required to compute this column. Should be used if `source` is a SQL statement referencing other tables. |
| index       | no        | Override default to build an index based on this column. Possible values: true/false/dictionary. See [index](#index)              |
| identifier  | no        | Boolean. Marks a column of a view as part of the identity of the modeled entity; see [Identifier columns](#identifier-columns-and-the-identifiers-token) |
| description | no        | description of this column to be included in auto-generated documentation                                                         |
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

The value of `source` can be:

* a string — for tables loaded from files, the name of a column in
  the incoming tabular data; for views, a SQL expression evaluated
  over the relation in `create.from` (e.g. `MIN(dob)`);
* an integer — a zero-based index of a column in the incoming
  tabular data (useful when the input has unnamed columns);
* a list of candidate column names — an extension used when building
  federated views over tables with varying column names, see
  [Data Modeling Extensions](DataModellingExtensions.md);
* the literal string `None` — suppresses the column definition in the
  generated DDL; used when the `create.select` statement already
  produces the column but it still has to be documented in the model;
* a dictionary with the keys described below.

| Parameter   | Required?                        | Description                                                              |
|-------------|----------------------------------|--------------------------------------------------------------------------|
| type        | no                               | One of: `column`, `multi_column`, `range`, `compute`, `generated`, `file` |
| column      | for type `column`                | A column name in the incoming tabular data                              |
| pattern     | for type `multi_column`          | Python format pattern (e.g. `"MONTH_{:d}"`) naming the input column for each value of the accompanying `range` column |
| values      | for type `range`                 | The list of values over which the record is transposed                  |
| code        | for types `generated`, `compute` | Code for generated and computed columns                                 |
| columns     | for type `compute`               | Names of input-file columns referenced by the compute code              |
| parameters  | for type `compute`               | Names of database columns referenced by the compute code                |

A column with source type `range` transposes the data: for every
input record, one database record is created per value listed in
`values`, and the column stores that value. Only one `range` column
per table is allowed. Columns with source type `multi_column` can
only be used in a table that has a `range` column: for each value of
the range, the value of a `multi_column` column is taken from the
input column whose name is produced by applying `pattern` to that
value. Together these two source types convert wide records (e.g.
one column per month) into long ones (one record per month).

#### Joined view columns (`select` / `from` / `where`)

In a view created with a `group by` clause, the `source` of a column
can also be a dictionary with the keys `select`, `from` and
(optionally) `where`. Such a column is generated as a correlated
scalar subquery: `select` supplies the selected expression, `from`
names another table of the domain, the view's grouping columns are
equated with the corresponding columns of the joined table (column
names are mapped through `source` definitions where they differ), and
the optional `where` condition is ANDed to these join conditions.
A living example from `medicaid.yaml`:

```yaml
            - months_eligible:
                source:
                  select: "COUNT(distinct month)"
                  from: monthly
                  where: "max_elg_cd != '00'"
```


### Index

The value for `index` key can be a simple boolean `true` or `false`. If additional parameters 
are required, the value can be a dictionary with the following keys. For the explanation
of options like *using* or *include*, see 
[PostgreSQL Documentation](https://www.postgresql.org/docs/current/sql-createindex.html).

| Parameter                    | Required? | Description                                                                                                                                                                                             |
|------------------------------|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name                         | no        | A custom index name, if omitted the name will be generated                                                                                                                                              |
| using                        | no        | The indexing method; defaults to BTREE, or to GIN for array-typed columns                                                                                                                               |
| include                      | no        | Additional columns to include with index                                                                                                                                                                |
| required_before_loading_data | no        | Adding this key tells the generator that this index must be created before the table is populated. Otherwise, to improve performance, indices might be created after a table is populated with all data |


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

The columns used for computation are listed under either `columns`
or `parameters`. Names under `columns` are the original column names
in the data file; to reference database columns, use `parameters`.
Reference either kind by its number in curly brackets in the compute
code.


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

Here in `code` the pattern `{1}` is replaced with a reference to the
value of the first (and only) listed column, `ADMSN_DT`, in the
current input record.

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
(This example illustrates the `parameters` syntax; see the note at
the end of this section — it does not run unmodified against the
current loader.)

#### Execution scope of the compute code

Knowing exactly how the compute code is executed helps when writing
it:

* The code is a single Python expression, evaluated with `eval()` by
  the [inserter](members/inserter) module
  (`dorieh.platform.data_model.inserter`) for every database record
  produced — once per input record, or once per range value for
  transposed (range-column) tables.
* The placeholders `{1}`, `{2}`, ... are substituted before
  evaluation with references to cells of the raw input record. They
  refer first to the entries of `parameters` and then to the entries
  of `columns`, in the order listed; `{0}` is reserved and must not
  be used.
* The names available to the expression are the Python builtins plus
  the names imported by the inserter module. Of these, the ones
  intended for use in compute code are `datetime` and `timedelta`
  (the classes from the standard `datetime` module) — as in the
  `datetime.strptime(...)` example above, which is used in production
  by `medicaid.yaml`. The raw input record is also visible as `row`.
* If the expression raises any exception, the value is silently set
  to `None` and NULL is stored in the database. Test compute columns
  on sample data: a typo in the expression does not stop the load, it
  produces empty values.

Note that `fips_dict` (a dictionary mapping US state postal codes to
state FIPS codes, defined in
[dorieh.platform.fips](members/fips)) is **not**
currently imported into the inserter's namespace, so the `fips5`
example above illustrates the `parameters` referencing syntax rather
than a configuration that can run unmodified against the current
loader.

### File columns

File columns are declared with source type `file` (their database
type is an ordinary character type). They store the base name of the
file, from which the data has been ingested. When the Project Loader
introspects the incoming data it appends a `FILE` column
(`VARCHAR(128)`, with an index created before loading) to every
table automatically.

### Record columns

A record column stores the sequential index of the record within the
data ingested from a file. There is no special `record` source type:
a record column is an ordinary column declared with a PostgreSQL
auto-increment type (`SERIAL` or `BIGSERIAL`). The Universal Database
Loader omits columns of these types from the generated `INSERT`
statements, so the database itself assigns each row the next value of
the backing sequence in ingestion order. When the Project Loader
introspects the incoming data it appends a `RECORD` column
(`BIGSERIAL`, indexed) automatically, alongside `FILE`, and makes
`(FILE, RECORD)` the default primary key. Together, the `FILE` and
`RECORD` columns anchor row-level provenance: every database row can
be traced back to a source file and a position within it.

### Identifier columns and the `{identifiers}` token

In a view definition, a column can be marked with `identifier: true`
to declare that it is part of the identity of the modeled entity.
The `source` expression of any other column of the same view may then
contain the token `{identifiers}` (in lower case). The DDL generator
replaces the token with a parenthesized, comma-separated list built
from all identifier columns: for an identifier column whose source is
an aggregate expression such as `MIN(dob)`, the underlying column
name inside the parentheses is used (a `distinct` keyword, if
present, is stripped); for an identifier column with no `source` at
all, the column's own name is used. An identifier column must take
one of these two forms — a source that is a plain, non-parenthesized
expression is not supported.

The `_beneficiaries` view in `medicare.yaml` marks `dob`, `race` and
`sex` as identifiers and counts records that disagree on any of them:

```yaml
        - discrepancies:
            source: >
              (
                COUNT(distinct {identifiers}) - 1 +
                ...
              )
```

Here `COUNT(distinct {identifiers})` expands to
`COUNT(distinct (dob, race, sex))`.

### Transposing columns
                                          
Columns can be unnested (also known as exploded) or collapsed.
Exploding is useful when, for example, there is a separate column for
every month. Dorieh supports two mechanisms:

* **Wide-to-long at load time.** A column with source type `range`,
  together with `multi_column` source columns, converts wide records
  (one column per month) into long ones (one record per month) while
  the data is ingested; see [Source](#source).
* **In-database collapse and unnesting.** Repeated columns of one
  record can be collapsed into a single array column, and an array
  can be unnested with the SQL `unnest()` function so that each
  element becomes its own record, as in the Medicaid `monthly` view.

### Wildcards

To make it easier to work with similarly named columns, Dorieh supports wildcards.
Wildcard expression starts with `$` followed by a variable name
(single letters are the convention used in the shipped models). Values
are provided in square brackets that follow the wildcard. 

Example:

```yaml
  - diag[$n=1:25]:
      type: varchar
      optional: true
      source:
        - dgnscd$n
```

Will be expanded to 25 columns named `diag1`, `diag2`, ..., `diag25`.

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
| include   | no        | Additional columns to include with index. Currently ignored when `unique` is also specified |
| unique    | no        | Specifies that the index defines a unique constraint |
                                                      
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



## Indexing policies

* **explicit**. An index is built only where a column definition
  carries an `index` key
* **all** Every column gets an index
* **selected** Indices are created for columns matching certain patterns
  (defined in `index_columns` variable of [model](members/model) module)
  and for columns that define an `index`. This is the default policy,
  used when the domain does not specify one
* **unless excluded** An alias for **all**: internally both are mapped
  to the same policy. Indices are created for all columns except those
  that explicitly opt out with `index: false`

Regardless of the policy, `index: false` always suppresses the
single-column index, and columns of type `TEXT`, `HLL` or
`HLL_HASHVAL` are never indexed automatically. Specifying any other
policy name raises an error.

## Linking with nomenclature

### US States

Database includes a table with codes for US states. It is taken from:

<https://www.nrcs.usda.gov/wps/portal/nrcs/detail/national/technical/nra/nri/results/?cid=nrcs143_013696>

The data lives locally in [fips.py](members/fips), which contains a
hard-coded dictionary of two-digit state FIPS codes keyed by state
postal abbreviation (together with the SQL query that re-derives them
from the `us_iso` nomenclature table).

### County codes

County FIPS codes are not part of `fips.py`. The Medicare data model
derives them from Social Security Administration (SSA) county codes
through the `ssa` crosswalk table, which the
[ssa2fips](members/ssa2fips) utility
(`dorieh.platform.crosswalks.ssa2fips`) builds by downloading the
SSA-to-FIPS state and county crosswalk files published by the
National Bureau of Economic Research (NBER):

<https://www.nber.org/research/data/ssa-federal-information-processing-series-fips-state-and-county-crosswalk>

## Ingesting data

The following command ingests data into a table and all hard-linked
child tables:

```
    usage: python -u -m dorieh.platform.loader.data_loader [-h] [--domain DOMAIN]
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

## Where to go next

* The federated-view directives — combining heterogeneous per-year
  tables into a single view — continue in
  [Data Modeling Extensions](DataModellingExtensions.md).
* To see the DSL at production scale, follow the
  [Medicare claims pipeline tutorial](tutorial/medicare/building-medicare-pipeline.md)
  — a guided path — with the
  [Medicare case study](Medicare.md) as its reference; both are built
  around `src/python/dorieh/cms/models/medicare.yaml`.

```{seealso}
**Further reading:** Appendix A of the companion book
[*Research Data that Can Be Trusted*](about-the-book.md) covers the
same core DSL syntax. This page is the maintained, authoritative
reference. This documentation is self-contained; the book is optional
enrichment.
```

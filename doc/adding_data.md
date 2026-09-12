# How to add data to the database

```{contents}
---
local:
---
```
                         
## What data are you adding?

There are many ways to add data to the database. We review the following 
options:

- Creating a new data domain with its own pipelines and, optionally,
    software tools written in a programming language like Python, Java, R,
    Pl/PgSQL, etc.,
- Adding a new table:
    - from a file on file system
    - from remote data source
- Adding data to existing table
- Bulk ingesting multiple CSV-like files (we support many formats) from
    local file system to create a lightweight data domain

For creating new tables in the database, there is a choice between
manually creating a data model and required data conversions and
transformations or automatically inferring data structure based on 
data sampling.

(data-modelling-vs-data-introspection)=
## Data modeling vs data introspection

Tools for data modeling are discussed in 
[](Datamodels.md). 

Examples of manually created data models are data models for
[Medicare](Medicare.md) and 
[Medicaid](Medicaid.md) domains. Actual models are defined
respectively in 
[](members/medicare_yaml.md) and
[](members/medicaid_yaml.md)

To automatically infer data structure by analyzing sample data
and generating data model corresponding to the existing structure
one can use
[Introspector tool](members/introspector.rst).
It can be run as a standalone command-line tool or used via Python API.
Introspection generates a Bronze-layer model as described in
[The Dorieh approach](concepts.md#medallion-architecture-as-dorieh-implements-it),
including the FILE and RECORD provenance columns used for row-level
lineage.
Examples of using introspector via API can be found in 
[EPA pipeline](members/epa_registry.rst). 

[Project Loader Tool](ProjectLoader.md)
also uses Introspector.

## Adding new data domain

To add a new data domain, create a new repository (or a new package
inside Dorieh) and follow the structure of an existing domain such as
[Medicare](Medicare.md): a data model in YAML, CWL pipelines, and
optional Python tools. The
[climate tutorial](tutorial/climate/index.md) walks through building
such a domain end to end.

## Creating new single table

In many cases, creating a new single table will mean running a 
pipeline that first 
[introspects the data](members/introspector.rst) 
in a file (CSV, JSON, FST and some other
formats) and then running the 
[Data Loader](DataLoader.md). 
However, for simple cases one can use 
[Project Loader Tool](ProjectLoader.md)
to either ingest or just to introspect the data 
(introspection can be done by using `--dryrun` argument).

## Adding a table from a remote data source

Data residing at a remote source is first downloaded by a pipeline and
then ingested from the downloaded files as described above. See the
[EPA pipelines](epa.md) and the [gridMET utilities](climate.md) for
examples of pipelines that download data before loading it into the
database.

## Adding data to existing table

The process of adding data to an existing table is described in
[](DataLoader.md)

## Automatically ingesting multiple files from a file system

See [Project Loader Tool](ProjectLoader.md)
for details.

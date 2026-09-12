# Terms and acronyms used in this documentation

## Concepts

The following terms form the conceptual vocabulary of this
documentation. Each is defined at length, with pointers to where
Dorieh implements it, on the
[Concepts: the Dorieh approach](concepts.md) page.

**Medallion architecture** — an organization of a data warehouse into
progressively refined layers, in Dorieh named Bronze, Silver and Gold,
where each layer is derived only from the layer beneath it. See
[Concepts](concepts.md).

**Bronze / Silver / Gold layers** — the three Medallion layers: Bronze
holds data exactly as ingested from the source files, Silver holds
validated, deduplicated and cleaned data derived only from Bronze, and
Gold holds aggregates derived only from Silver for analysis and
quality control. See [Concepts](concepts.md).

**Dataset operator** — a node in the dataflow graph of a pipeline that
consumes one or more datasets and produces a dataset; in Dorieh, the
tables, views and materialized views declared in a data model, and the
workflow steps that populate them, are dataset operators. See
[Concepts](concepts.md).

**Field construction operator** — the rule by which one output field
is computed from input fields; in a Dorieh data model this is a
column's `source` definition, such as a SQL expression, an aggregate,
or compute code. See [Concepts](concepts.md).

**Disambiguation rules** — rules for resolving conflicting values when
records are aggregated: one value is chosen by a deterministic rule
(for example, the earliest date of birth) and the discarded
alternative is kept in a secondary column, with a consistency flag
recording that a conflict occurred. See [Concepts](concepts.md).

**Journaling** — recording records that fail validation in an audit
table, together with the reason for the failure and a timestamp,
instead of silently dropping them. See [Concepts](concepts.md).

**Invalid-records policy** — the `invalid.records` directive of a data
model, which tells the loader what to do with a record that fails
validation: raise an error (the default), ignore the record, or insert
it into an audit table (journaling). See [Concepts](concepts.md).

**FILE and RECORD provenance columns** — columns declared with the
`file` and `record` column types, which store for every ingested row
the name of the source file and the row's sequential index within that
file; they are the row-level provenance anchors of a Dorieh table. See
[Concepts](concepts.md).

**Fine-grained (cell-level) lineage** — lineage that combines
column-level tracing (which input columns and transformations produced
an output column) with row-level tracing (which source records
produced a row), so that any individual cell can be traced to its
origin. See [Concepts](concepts.md).

**Data dictionary** — generated documentation describing every table
and column of a data model; Dorieh generates it from the same YAML
definitions that build the database, so it cannot drift from the
schema. See [Concepts](concepts.md).

## Acronyms

| Term                                                                                                  | Expansion                                                                                                                                                                                        | More Info                                                                                                                                          |
|-------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| 7BDAT                                                                                                 | Proprietary binary data file format used by SAS software to store datasets (.sas7bdat extension). The file extension is .sas7bdat, but it's often referred to as 7BDAT in development workflows.  SAS uses this format to store structured data tables, including metadata (column names, types, etc.). | [SAS Introspector](members/mcr_sas2yaml.rst), [SAS Data Loader](members/mcr_sas2db.rst) |
| Airflow                                                                                               | A Workflow management system                                                                                                                                                                     | [Wikipedia](https://en.wikipedia.org/wiki/Apache_Airflow)                                                                                          |
| AirNow                                                                                                | US Government source for air quality data                                                                                                                                                        | [Website](https://www.airnow.gov/)                                                                                                                 |
| AQS                                                                                                   | Air Quality System: US Government source for air quality data                                                                                                                                    | [Website](https://www.epa.gov/aqs)                                                                                                                 |
| CCW                                                                                                   | Chronic Condition Data Warehouse                                                                                                                                                                 | [Website](https://www.healthypeople.gov/2020/data-source/chronic-condition-data-warehouse)                                                         |
| CMS                                                                                                   | Centers for Medicare & Medicaid Services                                                                                                                                                         | [Website](https://www.cms.gov/)                                                                                                                    |
| CRS                                                                                                   | Coordinate reference system                                                                                                                                                                      | [Wikipedia](https://en.wikipedia.org/wiki/Spatial_reference_system)                                                                                |
| CSV                                                                                                   | File format, comma separated values                                                                                                                                                              | [Wikipedia](https://en.wikipedia.org/wiki/Comma-separated_values)                                                                                  |
| CUREC                                                                                                 | Current Reason for Entitlement Code, a field in Medicare enrollment data                                                                                                                         | [The Dorieh approach](concepts.md) and [Medicare](Medicare.md)                                                                                     |
| CWL                                                                                                   | Common Workflow Language                                                                                                                                                                         | [Wikipedia](https://en.wikipedia.org/wiki/Common_Workflow_Language) and [Website](https://www.commonwl.org/v1.2/)                                  |
| DAG                                                                                                   | Directed Acyclic Graph, the shape of a workflow's dataflow                                                                                                                                       | [Wikipedia](https://en.wikipedia.org/wiki/Directed_acyclic_graph) and [Pipelines](pipelines.md)                                                    |
| DBMS                                                                                                  | Database Management System                                                                                                                                                                       | [Wikipedia](https://en.wikipedia.org/wiki/Database#Database_management_system)                                                                     |
| DSL                                                                                                   | Domain-Specific Language, such as the Dorieh data-modeling language                                                                                                                              | [Data modeling reference](Datamodels.md)                                                                                                           |
| EPA                                                                                                   | U.S. Environmental Protection Agency                                                                                                                                                             | [Website](https://www.epa.gov/)                                                                                                                    |
| EPSG                                                                                                  | The IOGP's EPSG Geodetic Parameter Dataset is a collection of definitions of coordinate reference systems and coordinate transformations. 4326 is the EPSG identifier of WGS84                   | [Website](https://epsg.org/home.html)                                                                                                              |
| FST                                                                                                   | File format used by R                                                                                                                                                                            | [Description](https://www.fstpackage.org/)                                                                                                         |
| FTS                                                                                                   | File Transfer Summary, often created by SAS                                                                                                                                                      | [More details](fts)                                                                                                                                |
| gridMET                                                                                               | a dataset of daily high-spatial resolution surface meteorological data                                                                                                                           | [Website](http://www.climatologylab.org/gridmet.html)                                                                                              |
| HDF5                                                                                                  | File format (hierarchical)                                                                                                                                                                       | [Wikipedia](https://en.wikipedia.org/wiki/Hierarchical_Data_Format) and [Website](https://www.hdfgroup.org/)                                       |
| HLL                                                                                                   | HyperLogLog is an algorithm for approximating the number of distinct elements in a query result                                                                                                  | [Wikipedia](https://en.wikipedia.org/wiki/HyperLogLog)                                                                                             |
| IaC                                                                                                   | Infrastructure as Code                                                                                                                                                                           | [Why a data platform](rationale.md)                                                                                                                |
| MAX data                                                                                              | Medicaid Analytic eXtract (MAX) data                                                                                                                                                             | [Information](https://www.cms.gov/Research-Statistics-Data-and-Systems/Computer-Data-and-Systems/MedicaidDataSourcesGenInfo/MAXGeneralInformation) |
| NSAPH                                                                                                 | National Studies on Air Pollution and Health                                                                                                                                                     | [Website](https://www.hsph.harvard.edu/nsaph/) and [Introduction](home.md)                                                                         |
| OOM                                                                                                   | Out of Memory Error                                                                                                                                                                              |                                                                                                                                                    |
| OREC                                                                                                  | Original Reason for Entitlement Code, a field in Medicare enrollment data                                                                                                                        | [The Dorieh approach](concepts.md) and [Medicare](Medicare.md)                                                                                     |
| QC                                                                                                    | Quality Control                                                                                                                                                                                  | [The Dorieh approach](concepts.md)                                                                                                                 |
| SAS                                                                                                   | Statistical Analysis System, a popular software tool                                                                                                                                             | [Wikipedia](https://en.wikipedia.org/wiki/SAS_(software)) and [Company website](https://www.sas.com/)                                              |
| SQL                                                                                                   | Structured Query Language                                                                                                                                                                        | [Wikipedia](https://en.wikipedia.org/wiki/SQL)                                                                                                     |
| WGS 84                                                                                                | The World Geodetic System (WGS) is a standard for use in cartography, geodesy, and satellite navigation including GPS. 4326 is the EPSG identifier of WGS84                                      | [Wikipedia](https://en.wikipedia.org/wiki/World_Geodetic_System) and [documentation](http://www.unoosa.org/pdf/icg/2012/template/WGS_84.pdf)       |




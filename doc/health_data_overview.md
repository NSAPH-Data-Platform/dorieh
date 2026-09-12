# Health Data in Dorieh (Medicare and Medicaid)

```{seealso}
* [Data dictionary and lineage for Medicare processing](MedicareLineage.md) —
  every table and column of the warehouse, with lineage diagrams.
* [Health Data: See Also](health_seealso.md) — related pages in other
  sections.
```

```{contents}
---
local:
---
```


## Overview of Health Data Processing

Dorieh includes Data processing pipelines to
ingest and process health datasets provided by the
[Centers for Medicare & Medicaid Services (CMS)](https://www.cms.gov/) via 
[ResDac](https://resdac.org/).

These pipelines build a data warehouse from ResDAC-delivered 
raw data files (both Medicare and Medicaid), preparing the data 
for analysis and visualization. The data warehouse can
be used as Feature Store for building ML/AI models.

The workflow performs:

* Ingestion of raw fixed-width and SAS-based files into a relational database
* Data cleansing and deduplication (where possible)
* Creation of standardized and federated tables
* Computation of quality metrics (QC)
* Optimization for efficient querying

For more details, refer to:

* [Medicare](Medicare.md) processing workflow and data model (schema)
* [Medicaid](Medicaid.md) processing workflow and data model (schema)
* Tips on [querying of Medicaid data](QueringMedicaid.md)

Medicare processing workflow includes a
[pipeline to automatically generate Quality Control (QC) Tables](Medicare.md#creating-qc-tables).

These tables can be visualized in the included Apache Superset dashboard. 

## Project Structure

The two directories at the repository root relevant to this section are
`doc/` (this documentation) and `src/` (CWL workflows and Python code);
examples and Docker Compose setups live under `examples/` and `docker/`.

The `src/` directory is organized as follows:

    - cwl
    - python

### CWL Workflows

The `cwl/` folder contains reusable Common Workflow Language (CWL) 
tools and workflows. Each CMS data processing step (
e.g. ingest, combine, transform) is implemented as a modular CWL tool.

CWL tools are documented individually.
Tools are combined into full workflows, such as:

* [Medicare Pipeline](pipeline/medicare)
* [Medicaid Pipeline](pipeline/medicaid)


### Python Utilities

The `python/` directory provides CLI tools and 
reusable modules, documented in:

* [CMS Python Package Overview](CMSLibrary.md).

These include:

* Parsing fixed-width data layouts from FTS files
* Working with SAS7BDAT files
* Generating dynamic schemas (YAML models)
* Data loading and validation
* PostgreSQL utilities (indexing, vacuuming)


### Data Model for health data

We define a YAML-based data model (schema) to describe each 
processing table.

This model is used to:

* Automatically generate SQL DDL statements
* Control how data is read from files and loaded into the database
* Standardize naming conventions, indexing, and transformations

Schemas are:

* Automatically generated via FTS parsing (for 2011+ ResDAC files)
* Programmatically introspected from SAS7BDAT files (for 1999–2010 Medicare data)

#### Medicare Tables

See also:

* 📄 [Medicare Data Model (YAML)](members/medicare_yaml.md)
* 🔗 [Medicare pipeline documentation](Medicare.md)
                                 
Main Tables:

* `medicare.beneficiaries` [details](Medicare.md#creating-beneficiaries-table)
* `medicare.enrollments` [details](Medicare.md#creating-enrollments-table)
* `medicare.admissions` [details](Medicare.md#creating-inpatient-admissions-table)

Federated / intermediate SQL Views:

* `medicare.ps` [Union of raw data for patient summaries](Medicare.md#creating-federated-patient-summary)
* `medicare._ps` [Companion materialized view adding county FIPS codes](Medicare.md#second-step-mapping-to-county-fips-codes)
* `medicare.mbsf_d` [Union of the split dual-eligibility component files](Medicare.md#creating-the-mbsf_d-dual-eligibility-view)
* `medicare.ip` [Union of raw data for inpatient admissions](Medicare.md#creating-federated-admissions-view)


#### Medicaid Tables

See also:

* 📄 [Medicaid Data Model (YAML)](members/medicaid_yaml.md)
* 🔗 [Medicaid processing steps](Medicaid.md)

Tables:

* `medicaid.beneficiaries` [details](Medicaid.md#beneficiaries)
* `medicaid.enrollments` [details](Medicaid.md#enrollments)
* `medicaid.eligibility` [details](Medicaid.md#eligibility)
* `medicaid.admissions` [details](Medicaid.md#inpatient-admissions)

Federated / intermediate SQL Views:

* `medicaid.monthly`
* `medicaid._eligibility`

### SQL Utilities 

#### Stored Procedures

📄 [Procedures](members/procedures.md) 
help scale population of large tables like 
[eligibility](Medicaid.md#eligibility),
by batching inserts by beneficiary, or by year and state.
This avoids resource exhaustion in large transactions.

#### Date Parsing Functions

📄 [Custom SQL functions](members/functions.md) to parse 
non-standard date formats
commonly found in legacy Medicare files and ResDAC data.

(cms-indices-and-tables)=
## Documentation Indices

* [](genindex)
* [](modindex)

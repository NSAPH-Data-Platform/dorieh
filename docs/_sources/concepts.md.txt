# The Dorieh Approach: Declarative Data Modeling, Medallion Layers, and Fine-Grained Lineage

This page defines the concepts and vocabulary that the rest of the
documentation relies on. Every term introduced here links to the page
where it is developed in depth and to the code artifact that implements
it. The documentation is self-contained: everything on this page can be
verified against the repository's own code, models and synthetic data.

```{contents}
---
local:
---
```

## Two languages, one pipeline

A Dorieh pipeline is described by two complementary, declarative
languages:

* A **workflow language** — the
  [Common Workflow Language (CWL)](pipelines.md) — describes the
  *topology* of the pipeline: which steps exist, what files and values
  flow between them, and which steps can run in parallel. The pipeline
  is a directed acyclic graph (DAG); CWL declares its nodes and edges
  but says nothing about what happens to the data inside a node.
* The **Dorieh data-modeling DSL** — a YAML dialect documented in the
  [data modeling reference](Datamodels.md) and its
  [extensions](DataModellingExtensions.md) — describes what each node
  *does to the data*: which tables and views exist, how every output
  column is computed from input columns, what constitutes a valid
  record, and what to do with records that are not valid.

Both languages are declarative: they state what the result must be, and
Dorieh generates the imperative code (DDL, SQL, triggers, loader
invocations) that produces it. The generated SQL is ordinary PostgreSQL
and can be inspected, which is what makes the pipeline auditable rather
than a black box (see [Why Data Platform?](rationale.md)).

Two properties follow from this design and are relied on everywhere:

* **Immutability of inputs.** A transformation never modifies the
  dataset it reads. Downstream layers are created as views, materialized
  views or `CREATE TABLE ... AS SELECT` statements over upstream
  objects; the as-ingested data is never updated in place.
* **Idempotency.** Because outputs are pure functions of immutable
  inputs, a step can be re-run and yields the same result. The
  [data loader](Datamodels.md#ingesting-data) supports this directly
  with its `--incremental` flag, which commits after every file and
  skips files that have already been ingested.

## Medallion architecture as Dorieh implements it

Dorieh organizes the tables and views of a domain into the three layers
of the medallion architecture:

* **Bronze** — data exactly as ingested. Dorieh creates a separate
  table for every source file (see
  [storing raw Medicare data](Medicare.md#storing-raw-data-in-the-database)),
  because in longitudinal data the file structure often changes from
  year to year. When Dorieh introspects source files to generate a
  Bronze model, it appends two provenance columns to every table: a
  `FILE` column holding the original file name and a `RECORD` column
  holding the line number of the record in that file (see the
  [data introspector](members/introspector)). Bronze tables are
  immutable: no downstream step ever updates them.
* **Silver** — harmonized, cleaned and federated data, built from
  Bronze data only — either directly or through intermediate Silver
  views — never from Gold aggregates. This is where heterogeneous
  yearly schemas are united into a single view, types are cast, codes
  are normalized and invalid records are filtered out and journaled.
* **Gold** — analytic and quality-control (QC) aggregates, built *only*
  from Silver objects. Gold datasets are typically materialized views
  grouped by the dimensions users actually query. Audit journals
  produced during Silver validation (such as
  `medicare_audit.admissions`) are Silver-layer byproducts, so a Gold
  object such as `qc_adm_union`, which unions them with the accepted
  records, still satisfies this rule.

Two worked references are used throughout the documentation:

| Layer  | Climate tutorial                                              | Medicare pipeline                                                                       |
|--------|---------------------------------------------------------------|------------------------------------------------------------------------------------------|
| Bronze | `bronze_temperature` table                                    | `cms.*` tables, one per source file                                                     |
| Silver | `silver_temperature` view                                     | `medicare.ps` / `_ps`, `beneficiaries`, `enrollments`, `admissions` and the federated admission views |
| Gold   | `gold_temperature_by_state` materialized view                 | `medicare.qc_*` QC aggregates                                                           |

The climate layers are built step by step in the
[Bronze–Silver–Gold climate tutorial](tutorial/climate/index.md)
from the model file
[`doc/tutorial/climate/example1_model.yml`](tutorial/climate/example1_model.yml).
The Medicare layers are described in the
[Medicare case study](Medicare.md) and defined in
`src/python/dorieh/cms/models/medicare.yaml`.

## Dataset operators and field construction operators

The data-modeling DSL is built around two kinds of operators:

* A **dataset operator** is a node in the dataflow DAG: it consumes one
  or more datasets and produces a dataset. In the DSL, every table or
  view definition with a `create` clause is a dataset operator — the
  `from` key names the datasets it consumes, and optional `group by`,
  `select` and `exclude` keys shape the result. See the
  [create statement reference](Datamodels.md#create-statement).
* A **field construction operator** describes how a single output field
  is computed from input fields. In the DSL, every column definition
  with a `source` or a computing expression is a field construction
  operator. See the [column reference](Datamodels.md#column).

For example, the Gold layer of the climate tutorial is one dataset
operator: it consumes `silver_temperature` and produces a materialized
view aggregated by state and date
(from [`example1_model.yml`](tutorial/climate/example1_model.yml)):

```yaml
gold_temperature_by_state:
  description: |
    Temperature variations by US State
  create:
    type: materialized view
    from: silver_temperature
    group by:
      - us_state
      - date
```

Inside the Silver layer of the same model, a field construction
operator derives a Celsius temperature from the Kelvin value ingested
into Bronze:

```yaml
- temperature_in_C:
    type: float
    description: Temperature in Celsius
    source: (tmmx - 273.15)
```

When an output field is derivable from other fields *of the same output
record*, the DSL can delegate the computation to the database as a
[generated column](Datamodels.md#generated-columns). From the Medicare
`beneficiaries` table (`src/python/dorieh/cms/models/medicare.yaml`):

```yaml
- number_of_gap_years:
    type: INT
    source:
      type: generated
      code: "GENERATED ALWAYS AS (last_enrollment_year - first_enrollment_year + 1 - CARDINALITY(all_enrollment_years)) STORED"
```

## Families of field transformations

Field construction operators used across Dorieh models fall into a few
recurring families:

* **Direct copies and casts.** A column is carried through unchanged,
  possibly renamed or cast to a uniform type. The
  [`cast` extension](DataModellingExtensions.md#cast) lets one column
  declare a different conversion for each source type, which is
  essential when the same variable arrives as text in one year and as a
  number in another.
* **Single-value conversions.** A scalar function of one input value,
  such as the Kelvin-to-Celsius conversion `(tmmx - 273.15)` shown
  above, or parsing an eight-digit string into a date.
* **Rollups and approximations.** A value is mapped to a coarser
  nomenclature, sometimes only approximately. In the Medicare model,
  when a county code is absent the residence county is approximated
  from the ZIP code (`public.zip_to_fips3(year, zip)`), and a companion
  flag `fips3_is_approximated` records that the value is an
  approximation rather than a fact. A validation column
  `fips3_valdiated` (sic — the misspelling is preserved in the physical
  schema) cross-checks ZIP, state and county codes.
* **Aggregations.** Values of a group of records are combined with an
  aggregate function: standard SQL aggregates (`MIN(dob)`, `MAX(dod)`,
  `AVG(temperature_in_C)`), custom aggregations written as SQL
  expressions, and **HLL hashes** for approximate distinct counts. In
  Medicare tables, a generated column `bene` stores
  `hll_hash_text(bene_id)`, so Gold-level QC views can compute
  `NumDistinctBeneficaries` (sic — preserved physical name) over any
  grouping without rescanning beneficiaries; see
  [Using HyperLogLog](UsingHLL.md).
* **Unions and federation across heterogeneous yearly schemas.** A
  single Silver view is defined over many Bronze tables whose columns
  differ from year to year. A column may list several possible
  [source names](DataModellingExtensions.md#combining-multiple-sources-and-optional-columns),
  be marked `optional` for years where it does not exist, and carry
  per-type casts. The Medicare `ps` view federates all
  `cms.mbsf_ab*` and `cms.mcr_bene_*` tables this way; see
  [creating the federated patient summary](Medicare.md#creating-federated-patient-summary).
* **Array collapse and unnesting.** Repeated columns of one record are
  collapsed into an array — the 25 `diag1` … `diag25` columns of an
  inpatient record become a single `diagnoses` array in the Medicare
  `admissions` table — or, conversely, an array (or a set of monthly
  columns) is unnested so that each element becomes its own record, as
  in the Medicaid `monthly` view (see
  [transposing columns](Datamodels.md#transposing-columns)).

## Disambiguation rules

This section is the canonical definition of **disambiguation rules** in
the Dorieh documentation; the
[Medicaid](Medicaid.md#deduplication-and-data-cleansing) and
[Medicare](Medicare.md#creating-beneficiaries-table) pages show the
rules applied to real models.

An aggregation frequently expects a single value where the source
records can disagree. When all records for one Medicare beneficiary are
combined into a single `beneficiaries` row, that person has, in
reality, exactly one date of birth — but the raw yearly files may
report several. Dorieh never resolves such a conflict silently.
Instead, a disambiguation rule has three parts:

1. **Pick a deterministic primary value.** A fixed, documented rule
   selects the canonical value — for example, the earliest date of
   birth (`MIN(dob)`), the latest date of death (`MAX(dod)`), or for
   OREC (Original Reason for Entitlement Code) the value from the
   earliest enrollment year with ties broken by the smallest code.
2. **Keep the divergent value in a secondary column.** The discarded
   alternative is preserved next to the primary: `dob_latest` is
   non-null only when the records disagreed on the date of birth
   (`dod_earliest` and `orec_latest` play the same role for their
   columns). From `_beneficiaries` in `medicare.yaml`:

   ```yaml
   - dob_latest:
       source: |
         CASE
           WHEN MAX(dob) <> MIN(dob) THEN  MAX(dob)
         END
   ```

3. **Surface a `consistent_*` flag.** A QC column classifies every
   entity as `MISSING` (no value at all), `AMBIGUOUS` (sources
   disagreed; the secondary column holds the alternative) or
   `CONSISTENT`. For date of death, where a null value is normal —
   most beneficiaries in any given year are alive — the flag uses
   `NONE` instead of `MISSING`. The Medicare QC view `qc_enrl_bene`
   defines `consistent_dob`, `consistent_dod`, `consistent_sex`,
   `consistent_race` and `consistent_orec` this way (the sex and race
   flags, which classify aggregated string lists, take only
   `AMBIGUOUS` or `CONSISTENT`).

Because the primary value is deterministic, the resulting tables are
reproducible; because the secondary column and the flag are preserved, a
project curator can still choose their own inclusion rule (for example,
exclude all ambiguous records, or only those where the dates of birth
differ by more than a threshold).

Disambiguation also determines *where* an attribute may live: an
attribute belongs at the grain where it is invariant. OREC is set at
enrollment and is invariant for the life of the beneficiary, so it is a
column of `beneficiaries`; CUREC, the *current* reason for entitlement,
legitimately varies by year, so it stays on `enrollments`, together
with its consistency flag (`consistent_curec`). The full story —
including the natural-join failure mode that motivated this rule — is
told in
[Entitlement reason codes: OREC and CUREC](Medicare.md#entitlement-reason-codes-orec-and-curec).

## Validation and journaling

Dorieh treats validation as part of the data model, not as an
afterthought. When a table declares an
[invalid-records policy](Datamodels.md#invalid-record), the DDL
generator (the [Domain](members/domain) class) emits a database
trigger that applies **three validation checks** to every incoming
record, in order:

1. **Primary key integrity.** A record whose primary-key columns are
   null cannot be identified and is rejected with reason
   `PRIMARY KEY`.
2. **Consistency across records (referential integrity).** The record
   must match an existing record in its parent table — for example, a
   Medicare admission must match an enrollment for the same
   beneficiary, year and state. A record with no match is rejected with
   reason `FOREIGN KEY`.
3. **Elimination of duplicates.** If a record with the same primary key
   already exists, the newcomer is rejected with reason `DUPLICATE`,
   and the audit record keeps a physical reference (`REFCTID`) to the
   row that was retained, whose own `quality` column is updated to mark
   that it had duplicates.

What happens to a rejected record is governed by the
`invalid.records` policy in the DSL. The default, with no policy, is to
raise an exception and stop. The policy can instead say `IGNORE`
(drop silently — rarely appropriate) or, as the Medicare `admissions`
table does, journal the record:

```yaml
invalid.records:
  action: "INSERT"
  target:
    schema: $schema.audit
```

**Journaling** means every failed record is inserted into an audit
table in a separate audit schema, together with a `REASON` code and a
timestamp, instead of being silently dropped. The Gold QC view
`qc_adm_union` then unions the audit records with the accepted ones
(labeled with reason `OK`), so QC aggregates such as `qc_admissions`
account for every incoming record exactly once, broken down by
`OK` / `PRIMARY KEY` / `FOREIGN KEY` / `DUPLICATE`. Nothing is lost, and
the share of rejected data is itself a queryable quality metric; see
[Medicare QC tables](Medicare.md#creating-qc-tables).

## Fine-grained lineage

Dorieh aims at **cell-level lineage**: for any value in any table, it
should be possible to establish both *how* it was computed and *from
which raw records* it came. Cell-level lineage is the combination of:

* **Column-level lineage**, derivable statically from the field
  construction operators in the model: every column's `source`
  expression names the upstream columns it depends on, so the chain of
  transformations from a Gold column back to Bronze columns can be
  reconstructed and drawn without running the pipeline.
* **Row-level lineage**, provided by the `FILE` and `RECORD`
  provenance columns anchored in Bronze: `FILE` stores the original
  source file name and `RECORD` the line number within it. Silver
  objects carry these columns forward — the Medicare `enrollments`
  view, for instance, aggregates them so each enrollment row lists all
  contributing files and record numbers.

The data dictionary and lineage tooling generates these artifacts
automatically from the model: a table-level lineage diagram, a
documentation page per table and per column, a column-level lineage
diagram for every column, and an index of columns across all tables.
See the
[tutorial on constructing data dictionaries and lineage graphs](tutorial/climate/constructing-lineage.md)
for the climate model and the
[Medicare data dictionary and lineage](MedicareLineage.md) for a
production-scale example.

## Where each concept lives

| Concept                                | Documentation page                                                                 | Code artifact                                                                 |
|----------------------------------------|--------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| Workflow language (CWL), DAG topology  | [Data processing pipelines](pipelines.md)                                          | `src/cwl/*.cwl`                                                                |
| Data-modeling DSL (core syntax)        | [Data modeling reference](Datamodels.md)                                           | `dorieh.platform.data_model.domain`                                            |
| DSL extensions (federation, casts)     | [Data modeling extensions](DataModellingExtensions.md)                             | `ps` view in `src/python/dorieh/cms/models/medicare.yaml`                      |
| Medallion layers (teaching example)    | [Climate tutorial](tutorial/climate/index.md)                  | `doc/tutorial/climate/example1_model.yml`                                      |
| Medallion layers (case study)          | [Medicare pipeline](Medicare.md)                                                   | `src/python/dorieh/cms/models/medicare.yaml`                                   |
| Disambiguation rules                   | This page; applied in [Medicaid](Medicaid.md) and [Medicare](Medicare.md)          | `_beneficiaries` and `qc_enrl_bene` in `medicare.yaml`                         |
| Validation and journaling              | This page; [invalid-records reference](Datamodels.md#invalid-record)               | validation trigger generator in `dorieh.platform.data_model.domain`            |
| HLL approximate distinct counts        | [Using HyperLogLog](UsingHLL.md)                                                   | `bene` generated columns in `medicare.yaml`                                    |
| Lineage and data dictionary            | [Lineage tutorial](tutorial/climate/constructing-lineage.md), [Medicare lineage](MedicareLineage.md) | `dorieh.platform.loader.introspector` (FILE/RECORD), dictionary tool |
| Terms and acronyms                     | [Glossary](glossary.md)                                                             | —                                                                              |

```{seealso}
**Further reading:** Chapters 5 ("Language Design") and 6 ("Proof of
Concept Implementation") of the companion book
[*Research Data that Can Be Trusted*](about-the-book.md) develop the
ideas behind this page in depth. This documentation is self-contained;
the book is optional enrichment.
```

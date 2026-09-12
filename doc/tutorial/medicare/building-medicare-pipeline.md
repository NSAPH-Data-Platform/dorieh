# Tutorial: Building the Medicare Claims Pipeline

```{contents}
---
local:
---
```

```{seealso}
* [Medicare: Building a Data Warehouse from ResDac Files](../../Medicare.md) — the reference this tutorial walks through.
* [Example: Medicare Processing Pipeline with Synthetic Data](../../medicare-example.md) — the guide to running the pipeline yourself.
```

## Introduction

This tutorial plays the same role for the Medicare case study that the
[climate tutorial](../climate/index.md) plays for the climate example —
with one important difference. The climate tutorial builds a small pipeline
from scratch; the Medicare pipeline already exists in the repository as a
production-scale artifact. Instead of writing files, you will read them,
retracing the design decisions behind them and following the data from raw
claims files to a quality-control dashboard.

The two tutorials are meant to be read as a matched pair. The
[design section](#designing-the-pipeline) below follows the same five
design steps that shaped the climate pipeline (see
[how that pipeline was designed](../climate/building-climate-pipeline.md#how-this-pipeline-was-designed)):
identify the sources, specify the consumers, map the dataflow, lay out the
topology, plan documentation and provenance. What each step settles in a
sentence for open climate data takes a real decision for restricted,
drifting claims data — so here the steps are named and taken one at a time.

Two artifacts define the entire pipeline:

* `src/python/dorieh/cms/models/medicare.yaml` — the data model, written in
  the [Dorieh data-modeling DSL](../../Datamodels.md): every table and view
  of the warehouse, how every column is computed, what happens to invalid
  records. A rendered copy is the
  [generated Medicare data model](../../members/medicare_yaml.md).
* `src/cwl/medicare.cwl` — the workflow, declaring the pipeline's steps and
  their order; its generated documentation is
  [the Medicare pipeline spec](../../pipeline/medicare.md).

This split — CWL for the topology, the YAML DSL for what each node does to
the data — is the central pattern of Dorieh, introduced in
[Concepts: two languages, one pipeline](../../concepts.md#two-languages-one-pipeline).
If terms like *disambiguation rules* or *journaling* are new to you, read
the [concepts page](../../concepts.md) first.

## Designing the pipeline

Before opening the model file, it is worth reconstructing how this pipeline
was designed. Each step below records a design decision; the walkthrough
that follows shows it written down in `medicare.yaml` and `medicare.cwl`.

### Step 1. Identify data sources and producers

The inputs are administrative claims files produced by CMS and distributed
to researchers by ResDAC. For each year the pipeline expects at least two
deliverables: a beneficiary summary file (MBSF, also called the patient
summary or denominator) and an inpatient admissions file (MEDPAR); in some
years the beneficiary summary arrives split into components (the `mbsf_d`
files carry the monthly dual-eligibility indicators). The data files are
fixed-width text (`.dat`), each accompanied by a File Transfer Summary
([FTS](../../fts.md)) document — a plain-text, human-readable layout of
column names, types, widths and positions.

Three properties of these sources drive the whole design:

* **The schemas drift.** Column names, types and even the set of files
  change from year to year — see
  [the overview of ingesting raw Medicare files](../../Medicare.md#ingesting-raw-files).
  No hand-written schema would survive; the layouts must come from the FTS
  documents themselves.
* **Access is restricted.** The real files may only be used within
  environments covered by a data use agreement; the repository instead
  ships a [synthetic look-alike dataset](../../medicare-example.md)
  reproducing the file formats with no real person's data.
* **The data grows by whole years.** A new deliverable adds a year's worth
  of files rather than revising the years already loaded, so ingestion
  should be able to add a year without redoing the rest — a requirement
  Step 4 returns to.

### Step 2. Specify data consumers and target outputs

On the output side sit two kinds of consumers. Researchers query the
warehouse in PostgreSQL and expect curated, indexed tables at the grains
they reason about: one row per beneficiary, per person-year-state
enrollment, per validated admission. Data curators watch the
[Superset QC dashboard](../../medicare-example.md) shipped with the example
and expect every number to be explainable: where a value came from, how
many records were rejected and why. Both expect reproducibility and
documented provenance.

Those expectations fix the target outputs: three curated tables —
`beneficiaries`, `enrollments`, `admissions` — and the QC aggregates
behind the dashboard, `qc_enrollments` and `qc_admissions`, in which the
share of rejected records is an ordinary queryable measure.

### Step 3. Map the logical dataflow

Working backward from those outputs, a small set of transformations is
unavoidable:

* **Schemas from FTS documents** — before anything is loaded, each year's
  layout must be turned into a machine-readable schema, since Step 1 ruled
  out maintaining one by hand.
* **Schema harmonization across years** — uniting the heterogeneous yearly
  files into single views with uniform column names and types.
* **Normalization of dates and identifiers** — dates arrive as character
  strings in some years and SAS numerics in others; two-digit years must
  become four-digit; nine-digit ZIP codes must be split in two.
* **Geographic rollups and approximations** — the raw SSA codes and ZIP
  codes must be mapped to the FIPS codes researchers use; a missing county
  code is approximated from the ZIP code, flagged, not hidden.
* **Disambiguation of person-level attributes** — a person has one date of
  birth, but the yearly files may disagree; conflicts are resolved by
  deterministic [disambiguation rules](../../concepts.md#disambiguation-rules)
  that keep the discarded alternative and flag the discrepancy.
* **Quality-control checkpoints** — each admission must pass three
  validation checks (primary-key integrity, referential integrity against
  enrollments, elimination of duplicates); failed records are journaled,
  never silently dropped, so the share of rejected data is itself queryable.

These transformations arrange themselves into the
[Medallion layers](../../concepts.md#medallion-architecture-as-dorieh-implements-it):
Bronze holds the files exactly as ingested; Silver harmonizes, disambiguates
and validates; Gold aggregates for quality control. Each layer is derived
only from the layer beneath it.

### Step 4. Lay out the workflow topology

With sources, outputs and dataflow settled, the topology follows:
initialize the database, ingest the raw files, build the beneficiary and
enrollment objects, build the admissions objects (validated against
enrollments, so they come after), then build the QC aggregates.
`medicare.cwl` expresses exactly this chain of five steps, ordered by data
dependencies — see [Orchestration](#orchestration-five-steps-in-medicarecwl)
below — with the division of labor stated in the introduction: CWL declares
the topology; what each node does to the data lives in the data-model DSL.

This is also where Step 1's growth pattern is served. Ingestion is
incremental: tables already in the database are kept and only those whose
files appear in the input are replaced, so a new year's deliverables can be
added without reloading previous years — with an empty input directory the
step is skipped and later steps rebuild from what the database holds.
Parallelism lives inside this step, too: the loader writes to the database
over several concurrent threads (the `threads` parameter of
[load_raw_medicare](../../pipeline/load_raw_medicare.md), four by default),
while the in-database steps stay deliberately sequential — each Medallion
layer is built from the one beneath it.

### Step 5. Plan documentation and provenance

Finally, provenance is designed in rather than reconstructed later: `FILE`
and `RECORD` columns anchor every Bronze row to the exact line of its source
file; the model records the derivation of every column, so data dictionaries
and lineage diagrams can be generated from it; and the invalid-records
policy journals every rejected record with a reason code, turning failures
into auditable evidence rather than silent losses (see
[Documentation and lineage](#documentation-and-lineage) below).

### The design at a glance

| Design step | Decision for Medicare | Dorieh feature used |
|-------------|-----------------------|---------------------|
| 1. Sources and producers | Ingest yearly ResDAC deliverables (MBSF, MEDPAR) despite schema drift; develop against a synthetic look-alike | FTS-driven schema generation |
| 2. Consumers and outputs | Curated tables at three grains, plus QC aggregates behind a Superset dashboard | Data-modeling DSL; HLL distinct counts |
| 3. Logical dataflow | Harmonize, disambiguate, validate — layered as Bronze/Silver/Gold | Federated views, disambiguation rules, invalid-records policy |
| 4. Workflow topology | Five steps chained by data dependencies; incremental, multi-threaded ingestion | CWL sub-workflows wired with `depends_on` |
| 5. Documentation and provenance | Generate the dictionary and lineage from the model; anchor every row to its source line | Generated docs, `FILE`/`RECORD` columns, audit journal |

## From FTS documents to machine-readable schemas

The walkthrough begins where Step 3's dataflow does. The pipeline cannot
hand-maintain a schema for every year, so it derives schemas from the FTS
documents themselves. The
[fts2yaml module](../../members/fts2yaml.rst) parses each `.fts` file into a
YAML data model — column names, types, widths and indexing hints — which is
then used to create the staging table and to configure the fixed-width
reader that parses the matching `.dat` file. The
[load_raw_medicare](../../pipeline/load_raw_medicare.md) tool orchestrates
the sequence, scanning the input directory recursively for `.fts` files,
generating a schema from each, and loading the corresponding data file.

One convention matters: the immediate parent folder of each file must be
named after the year of its data (the year is inferred from the path) — see
[the Medicare reference](../../Medicare.md#files-for-years-2011-and-later).

## Bronze: one table per source file

Because the file structures differ, Dorieh creates a **separate table for
every source file**, all in the `cms` schema. The data is kept as delivered,
plus only what makes the tables joinable and traceable:

* the two provenance columns — `FILE`, the original file name, and `RECORD`,
  the line number within it — anchoring every row to its source;
* generated columns with uniform names for the four attributes every
  downstream object needs — `bene_id`, `year`, `state` and `zip` — each
  hiding a year-specific original column name.

This is the entire Bronze layer planned in Step 3: minimal standardization,
no cleansing, no filtering — see
[Storing raw data in the Database](../../Medicare.md#storing-raw-data-in-the-database).

## Silver: harmonize, disambiguate, validate

The Silver layer is where the model file earns its keep — the
harmonization, disambiguation and validation mapped out in Step 3 become
concrete declarations here. It is built by the
[medicare_beneficiaries](../../pipeline/medicare_beneficiaries.md) and
[medicare_admissions](../../pipeline/medicare_admissions.md) steps; every
object in it is declared in `medicare.yaml`.

### The federated patient summary: `ps` and `_ps`

The `ps` view unites all yearly beneficiary summary tables (`cms.mbsf_ab*`
and `cms.mcr_bene_*`) into one schema: each column declares the alternative
names it may have in the sources and a cast for each type it may arrive in.
The date of birth is a compact example (from
`src/python/dorieh/cms/models/medicare.yaml`):

```yaml
- dob:
    type: date
    description: Date of birth
    cast:
      "character varying": "public.parse_date({column_name})"
      numeric: "to_date(to_char({column_name}, '00000000'), 'YYYYMMDD')"
    source:
      - dob
      - bene_dob
      - bene_birth_dt
```

Whatever the year called the column and however it encoded the value, `ps`
exposes a single `dob` of SQL type `DATE`. The same pattern — built on the
[DSL extensions](../../DataModellingExtensions.md) — normalizes the year to
four digits, splits nine-digit ZIP codes into `zip` and `zip4`, maps SSA
state codes to state abbreviations and FIPS codes, and standardizes the
death date, sex, race and the monthly coverage indicator arrays.

A companion materialized view, `_ps`, adds the geographic rollups on top of
`ps`: the county FIPS code `fips3`, resolved from the SSA county code when
present and **approximated from the ZIP code** when it is not — with
`fips3_is_approximated` recording that the value is an inference, not a
fact — plus `yob`, the year of birth computed from the reported age (see
[Creating Federated Patient Summary](../../Medicare.md#creating-federated-patient-summary)).

### One row per person: `beneficiaries`

The `beneficiaries` table groups `_ps` by `bene_id`, collapsing all of a
person's yearly records into one row. The raw records can disagree about
attributes that in reality have exactly one value; the model resolves each
conflict with a [disambiguation rule](../../concepts.md#disambiguation-rules):
a deterministic primary value, the divergent alternative kept in a secondary
column, and a consistency flag.

* `dob` is the earliest date of birth, `MIN(dob)`; when the records
  disagree, `dob_latest` holds the latest one — its source in
  `medicare.yaml` is `CASE WHEN MAX(dob) <> MIN(dob) THEN MAX(dob) END`.
* `dod`, the date of death, mirrors the rule in the other direction: the
  latest value wins and `dod_earliest` keeps the alternative.
* `race` and `sex` are aggregated as comma-separated lists of the distinct
  codes encountered, so a conflict is visible in the value itself.
* `orec`, the Original Reason for Entitlement Code, is by definition set
  once and never changes — a per-person invariant, hence a `beneficiaries`
  column. Its canonical value comes from the earliest enrollment year, ties
  broken by the smallest code — `(array_agg(orec ORDER BY year, orec))[1]` —
  while `orec_latest` is non-null only when OREC changed over the years,
  which the downstream `consistent_orec` flag reports as `AMBIGUOUS`.

A `discrepancies` column counts the alternative values recorded for each
beneficiary; enrollment-span columns (`first_enrollment_year`,
`last_enrollment_year`, `all_enrollment_years`, the generated
`number_of_gap_years`) and a generated [HLL hash](../../UsingHLL.md) of the
beneficiary id (`bene`) complete the table — see
[Creating Beneficiaries table](../../Medicare.md#creating-beneficiaries-table).

### One row per person, year and state: `enrollments`

The `enrollments` table groups `_ps` by `(bene_id, year, state)` — its
primary key; a beneficiary who moved between states during a year has one
row per state. Address attributes can still vary within a group, so the
model keeps a deterministic pick (`MAX`) for `zip`, `fips3` and the SSA
codes alongside list columns (`zips`, `residence_counties`, `ssa2_list`,
`ssa3_list`) preserving all encountered values. Two QC columns guard the
geography: `fips3_is_approximated`, true when every contributing record had
its county approximated from the ZIP code, and `fips3_valdiated` (sic — the
physical column name is misspelled; use this spelling in queries), which
cross-checks county against state and ZIP.

The entitlement code that lives here is `curec`, the *Current* Reason for
Entitlement, which legitimately varies by year. It is aggregated as
`MAX(curec)` within the group; if duplicate source records disagree,
`curec_latest` becomes non-null and the generated `consistent_curec` column
flags the row `AMBIGUOUS`. Its per-person sibling `orec` is deliberately
**not** an `enrollments` column: the Gold QC view joins `enrollments` and
`beneficiaries` with a natural join, where any shared column silently
becomes part of the join key, dropping every year where the values
disagreed. The rule — invariants on `beneficiaries`, year-varying attributes
on `enrollments` — is explained in
[Entitlement reason codes: OREC and CUREC](../../Medicare.md#entitlement-reason-codes-orec-and-curec).
The table also carries the `hmo`, `buyin` and `dual` coverage families (each
a monthly indicator array, a month count and a generated boolean), a `died`
flag and the `state_count` diagnostic — see
[Creating Enrollments table](../../Medicare.md#creating-enrollments-table).

### Validated admissions

Admissions follow the same two-stage pattern: a federated view `ip` unites
the yearly MEDPAR tables (`cms.medpar_*` and `cms.mcr_ip_*`), normalizing
admission and discharge dates, and the `admissions` table built from it
collapses the up to 25 separate diagnosis columns into a single `diagnoses`
array next to `primary_diagnosis`. Unlike the tables above, `admissions` is
a **child of `enrollments`** and carries an
[invalid-records policy](../../Datamodels.md#invalid-record)
(from `src/python/dorieh/cms/models/medicare.yaml`):

```yaml
invalid.records:
  action: "INSERT"
  target:
    schema: $schema.audit
```

With it, Dorieh generates a trigger applying the three validation checks:

1. **Primary key integrity** — a record missing part of its key (beneficiary
   id, year, state, admission or discharge date): reason `PRIMARY KEY`.
2. **Referential integrity** — the admission must match an enrollment record
   for the same beneficiary, year and state: reason `FOREIGN KEY`.
3. **Elimination of duplicates** — a record whose primary key already
   exists: reason `DUPLICATE`; the retained row's `quality` column (default
   `PASS`) is updated to mark that it had duplicates.

Rejected records are not dropped: they are **journaled** into
`medicare_audit.admissions` with their `REASON` code, so the Gold layer can
account for every incoming record — see
[Creating Inpatient Admissions table](../../Medicare.md#creating-inpatient-admissions-table)
and [Validation and journaling](../../concepts.md#validation-and-journaling).

## Gold: the QC aggregates

The Gold layer, built by the [medicare_qc](../../pipeline/medicare_qc.md)
step, delivers the QC aggregates promised to Step 2's dashboard consumers:
two materialized views, each backed by a helper view.

For enrollments, the helper view `qc_enrl_bene` joins `enrollments` with
`beneficiaries` (the natural join whose safety the OREC rule guarantees) and
computes the beneficiary-grain consistency flags: `consistent_dob` and
`consistent_orec` take `MISSING`, `AMBIGUOUS` or `CONSISTENT`;
`consistent_dod` uses `NONE` instead of `MISSING` (a beneficiary without a
recorded death date is not inconsistent); `consistent_sex` and
`consistent_race` take only `AMBIGUOUS` or `CONSISTENT`.
The materialized view `qc_enrollments` aggregates it by seventeen
dimensions: `year`, `state`, `zip`, `fips3`, `orec`, `curec`, the booleans
`hmo`, `dual` and `buyin`, the six consistency flags (including
`consistent_curec`, arriving through the join), `fips3_is_approximated` and
`fips3_valdiated`. The grouping is declared `nullable group by`, so records
with missing dimension values are counted rather than excluded.

Every group carries the same measures: `NumRecords`, a plain `COUNT(*)`, and
(from `src/python/dorieh/cms/models/medicare.yaml`)

```yaml
- NumDistinctBeneficaries:
    type: BIGINT
    source: "(#(hll_add_agg(bene)))::BIGINT"
    index: false
```

`NumDistinctBeneficaries` (sic — the physical column name is missing an "i";
use this spelling in queries) is an approximate distinct count computed from
the [HLL hashes](../../UsingHLL.md) generated in Silver; a third column,
`bene_hll`, stores the HLL sketch itself, so distinct counts can be
re-aggregated over any subset of groups without touching the detail tables.

For admissions, the helper view `qc_adm_union` unions the journaled records
of `medicare_audit.admissions` — each carrying its `REASON` — with the
accepted records of `admissions`, labeled `'OK'`. The materialized view
`qc_admissions` aggregates the union by `year`, `state`, `zip` and `reason`,
with the same three measures. The share of data that failed each validation
check is thus an ordinary query — and a chart on the
[Superset dashboard](../../medicare-example.md). Full definitions:
[Creating QC Tables](../../Medicare.md#creating-qc-tables).

## Orchestration: five steps in medicare.cwl

The workflow [`medicare.cwl`](../../pipeline/medicare.md) is Step 4's
topology made concrete: it ties the layers together as five steps, each a
sub-workflow (or tool) of its own:

1. [`initdb`](../../pipeline/initdb.md) — updates the database utilities;
2. [`load_raw_data`](../../pipeline/load_raw_medicare.md) — the FTS-driven
   ingestion that builds the Bronze layer;
3. [`enrollments`](../../pipeline/medicare_beneficiaries.md) — builds
   `mbsf_d` (the view uniting the split dual-eligibility component files),
   `ps`, `_ps`, the intermediate grouping views `_beneficiaries` and
   `_enrollments`, and the `beneficiaries` and `enrollments` tables;
4. [`admissions`](../../pipeline/medicare_admissions.md) — builds `ip` and
   the validated `admissions` table;
5. [`qc`](../../pipeline/medicare_qc.md) — builds the Gold QC objects.

CWL has no "run after" clause; ordering is expressed through data
dependencies. Every step after `initdb` declares a `depends_on` input wired
to an output of its predecessor (from `src/cwl/medicare.cwl`):

```yaml
  admissions:
    run: medicare_admissions.cwl
    doc: Process medicare inpatient admissions (aka Medpar) data
    in:
      database: database
      connection_name: connection_name
      depends_on: enrollments/enrlm_table_vacuum_log
```

The `admissions` step starts only when the enrollments table is created,
indexed *and* vacuumed — `depends_on` names the last log of the previous
sub-workflow; `qc` depends on `admissions/adm_vacuum_log` likewise. Each
step's logs are workflow outputs, so every run leaves a record of itself.

## Documentation and lineage

Here Step 5's plan pays off. Because the model file records the derivation
of every column, the documentation of the warehouse is generated, not
written: a table-level
lineage diagram, a page per table, a page per column with its column-level
lineage diagram, and an index of columns — published as the
[Medicare data dictionary and lineage](../../MedicareLineage.md). The same
tooling is demonstrated hands-on in
[Constructing data dictionaries and lineage graphs](../climate/constructing-lineage.md).

Column-level lineage is only half of
[fine-grained lineage](../../concepts.md#fine-grained-lineage); the other
half is row-level. The `FILE` and `RECORD` anchors ingested in Bronze are
carried forward through Silver — `enrollments`, for instance, aggregates
them as comma-separated lists, so every enrollment row names all the source
files and line numbers that contributed to it. Any value — and any journaled
record — can thus be traced to the exact raw line it came from.

## Running it yourself

Everything this tutorial walked through can be run end to end without any
data use agreement, using the synthetic dataset published on Zenodo. The
[Medicare example](../../medicare-example.md) is the operational guide:
downloading the synthetic files, running `medicare.cwl` with
`toil-cwl-runner` against a local PostgreSQL instance, and importing the
pre-built Superset dashboard. When the run finishes, use this page and the
[reference](../../Medicare.md) to interpret the results.

```{seealso}
**Further reading:** Chapter 7 ("Sample Application: Building ML-Ready
Datasets") and Chapter 8 ("Dorieh Medicare Claims Data Pipeline") of the
companion book [*Research Data that Can Be Trusted*](../../about-the-book.md)
develop the ideas behind this page in depth. This documentation is
self-contained; the book is optional enrichment.
```

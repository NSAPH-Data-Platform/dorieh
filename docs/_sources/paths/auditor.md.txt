# Learning Path: Reviewers and Auditors

**This path is for you if** you need to *assess* data produced with
Dorieh — verify where a value came from, how records were validated,
what was excluded and why — for a methods review, an internal audit, or
regulatory documentation.

**At the end you will be able to** trace any cell in a curated table
back to a line in a raw source file, quantify exactly how many records
failed which validation check, and read the quality-control aggregates
that summarize data health.

## The path

1. **Read the provenance sections of [The Dorieh approach](../concepts.md)** —
   [fine-grained lineage](../concepts.md#fine-grained-lineage) (how
   column-level and row-level lineage combine into cell-level
   traceability) and the validation and journaling model (the three
   validation checks; failed records journaled with a reason, never
   silently dropped).
2. **Open the [data dictionary and lineage](../MedicareLineage.md)** for
   the Medicare warehouse: a clickable table-level diagram, a page per
   table, a page per column with its derivation formula and lineage
   graph, and an alphabetical column index.
3. **Read how validation is enforced** in
   [Medicare: Building a Data Warehouse from ResDac Files](../Medicare.md):
   the `medicare_audit` schema, the `PRIMARY KEY` / `FOREIGN KEY` /
   `DUPLICATE` reason codes, and the disambiguation rules with their
   `consistent_*` flags (what the pipeline reconciles versus what it
   surfaces as ambiguous).
4. **Interrogate the QC aggregates** — the
   [QC tables section](../Medicare.md#creating-qc-tables) explains
   `qc_enrollments` and `qc_admissions`; run the
   [Medicare example](../medicare-example.md) to compute them on
   synthetic data and see the same measures on its Superset dashboard.
5. **Check reproducibility claims**: every table and view is created
   from a versioned, declarative
   [data model](../Datamodels.md), and each database object carries a
   comment recording the Dorieh version and commit that created it.

## Going deeper

* [Using HLL](../UsingHLL.md) — the QC tables count distinct
  beneficiaries with HyperLogLog sketches; know the approximation
  before citing the numbers.
* [Database Testing Framework](../DBT.md) — regression tests asserting
  that data has not silently changed.
* [About the companion book](../about-the-book.md) — the extended
  treatment of provenance, regulation and trust behind this design.

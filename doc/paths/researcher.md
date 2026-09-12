# Learning Path: Researchers and Analysts

**This path is for you if** you want to *use* a Dorieh warehouse —
query curated health data, understand what each column means and how
trustworthy it is — rather than build pipelines yourself.

**At the end you will be able to** run the complete Medicare example on
synthetic data, query the resulting warehouse, read its quality-control
dashboard, and trace any column back to the raw files it came from.

## The path

1. **Skim [Why a data platform?](../rationale.md)** — five minutes to
   understand what problem Dorieh solves and why reproducibility drives
   its design.
2. **Run the [Medicare example](../medicare-example.md)** end to end.
   It uses a publicly available synthetic dataset, so no data use
   agreement is needed; you will load a full warehouse into PostgreSQL
   on your own machine.
3. **Read [Medicare: Building a Data Warehouse from ResDac Files](../Medicare.md)**
   — now that the tables exist in your database, this page explains
   what each of them is: the Bronze/Silver/Gold layers, the
   `beneficiaries`, `enrollments` and `admissions` tables, and the QC
   aggregates.
4. **Learn to query it**:
   [How to query the database](../SampleQuery.md) for the mechanics,
   [Querying Medicaid Data](../QueringMedicaid.md) for the
   health-data-specific patterns and caveats, and
   [Using HLL](../UsingHLL.md) for the approximate distinct counts the
   QC tables rely on.
5. **Open the QC dashboard** — the
   [Superset section of the Medicare example](../medicare-example.md)
   walks you through importing it. Every consistency percentage on it
   is an ordinary SQL measure you can now recompute yourself.

## Going deeper

* [Data dictionary and lineage for Medicare processing](../MedicareLineage.md) —
  look up the meaning and derivation of any column, down to the raw
  file and line number.
* [The Dorieh approach](../concepts.md) — the concepts behind what you
  have been using: disambiguation rules, journaling, fine-grained
  lineage.
* [Terms and acronyms](../glossary.md) — when the vocabulary gets
  ahead of you.

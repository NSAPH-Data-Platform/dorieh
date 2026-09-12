# Learning Path: Pipeline Developers

**This path is for you if** you want to *build* data pipelines with
Dorieh — define data models in the DSL, orchestrate them with CWL, and
generate their documentation and lineage automatically.

**At the end you will be able to** design a Bronze–Silver–Gold
pipeline, write its data model, wire it into a CWL workflow, validate
and journal bad records, and generate a data dictionary for the result.

## The path

1. **Read [The Dorieh approach](../concepts.md) in full.** It defines
   every load-bearing idea you will use: the split between the workflow
   language and the data-modeling DSL, dataset and field construction
   operators, Medallion layers, disambiguation rules, validation and
   journaling, fine-grained lineage.
2. **Work through the [climate tutorial](../tutorial/climate/index.md)**,
   all three parts, actually running each step. Part 1 builds the
   pipeline; Part 2 generates its workflow documentation; Part 3
   generates the data dictionary and lineage graphs. Everything runs on
   open data.
3. **Keep the DSL reference at hand while you do**:
   [Data Modeling for Dorieh Data Platform](../Datamodels.md) is the
   authoritative directive-by-directive reference, and
   [Data Modeling Extensions](../DataModellingExtensions.md) covers
   federating heterogeneous tables (unions, casts, exclusions).
4. **Read the [Medicare tutorial](../tutorial/medicare/building-medicare-pipeline.md)**
   — the same five design steps applied to a production-scale,
   schema-drifting, access-restricted dataset. This is where the
   patterns earn their keep: federated views, disambiguation,
   validation with journaling, QC aggregates.
5. **Plan your own pipeline** with
   [Adding more data](../adding_data.md) and the practical notes on
   runners and parameters in
   [Data Processing Pipelines](../pipelines.md).

## Going deeper

* [Database Testing Framework](../DBT.md) and
  [Testing workflows](../TestingWorkflows.md) — regression-testing what
  you build.
* The [Domain](../members/domain) class — the DDL generator behind the
  DSL, when you need to know exactly what SQL a directive produces.
* [Platform capabilities](../capabilities.md) — the operational
  how-tos your users will ask you about.

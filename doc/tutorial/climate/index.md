# Climate Tutorial: a Bronze–Silver–Gold Pipeline on Open Data

This tutorial builds a complete Dorieh pipeline — and then generates its
documentation — using only openly available data, so anyone can
reproduce every step without a data use agreement. Starting from
gridded daily temperature (gridMET), the pipeline aggregates the grid
over ZIP Code Tabulation Areas, loads the result into PostgreSQL, and
derives Bronze, Silver and Gold layers with the Dorieh data-modeling
DSL. The same design patterns apply directly to health and claims data;
they are applied to a production-scale case in the
[Medicare claims pipeline tutorial](../medicare/building-medicare-pipeline.md).

The tutorial has three parts, meant to be followed in order:

```{toctree}
---
maxdepth: 2
---
Part 1. Building the pipeline <building-climate-pipeline>
Part 2. Documenting the workflow <documenting-a-workflow>
Part 3. Data dictionaries and lineage graphs <constructing-lineage>
```

Runnable copies of the finished workflow and data model are provided in
[`examples/with-postgres/climate/`](https://github.com/ForomePlatform/dorieh/tree/main/examples/with-postgres/climate);
the simpler file-only (no database) variant of the workflow is described
in
[Example: aggregating a climate variable](../../Example-climate-workflow.md).

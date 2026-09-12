# Health Data: See Also

```{index} Medicare, Medicaid, health data
```

Pages in other sections of this documentation that readers of the
health domain most often need:

* [Data dictionary and lineage for Medicare processing](MedicareLineage.md) —
  the generated reference for every table and column of the Medicare
  warehouse, with clickable lineage diagrams (in the
  [Data Dictionaries](dictionaries.md) section).
* [Example: Medicare Processing Pipeline with Synthetic Data](medicare-example.md) —
  run the full pipeline without a data use agreement.
* [Building the Medicare Claims Pipeline](tutorial/medicare/building-medicare-pipeline.md) —
  the guided tutorial through the pipeline's design and implementation.
* [Querying Medicaid Data](QueringMedicaid.md) — querying patterns and
  caveats for health data (in Platform Capabilities).
* [Approximate distinct counting with HLL](UsingHLL.md) — how the QC
  tables count distinct beneficiaries (in Platform Capabilities).
* [Disambiguation rules](concepts.md#disambiguation-rules) — the
  general pattern behind the `consistent_*` QC flags.

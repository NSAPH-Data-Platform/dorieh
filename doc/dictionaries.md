# Data Dictionaries

```{index} data dictionary, lineage, provenance
```

Dorieh generates a data dictionary for every domain directly from its
data model: a page for every table, a page for every column with its
derivation formula, clickable table-level and column-level lineage
diagrams, and alphabetic indexes of tables and columns. Because the
dictionary is produced from the same definitions that build the
database, it cannot drift from the deployed schema; regenerating it is
part of the documentation build. The concepts behind these artifacts
are described in
[fine-grained lineage](concepts.md#fine-grained-lineage).

```{toctree}
---
maxdepth: 1
caption: Available dictionaries
---
Medicare data warehouse <MedicareLineage>
```

A second, smaller dictionary is generated for the climate tutorial's
Bronze–Silver–Gold model; Part 3 of the tutorial,
[Constructing data dictionaries and lineage graphs](tutorial/climate/constructing-lineage.md),
walks through generating it yourself and explores the
[resulting artifacts](tutorial/climate/mddocs/example1.dot.md), including
the alphabetic
[table list](tutorial/climate/mddocs/table-list.md) and
[column list](tutorial/climate/mddocs/column-list.md).

To generate a dictionary for your own domain, see the
[Data Dictionary Generation tool](members/domain_dictionary.rst) and
the regeneration recipe on the
[Medicare dictionary page](MedicareLineage.md).

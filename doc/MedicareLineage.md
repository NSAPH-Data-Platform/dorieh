# Data dictionary and lineage for Medicare processing

```{index} data dictionary, lineage, Medicare
```

```{toctree}
---
maxdepth: 1
---
lineage/medicare.dot.md
lineage/table-list.md
lineage/column-list.md
members/domain_dictionary.md
```

The dictionary and the data lineage graphs are generated using the 
[Dorieh Data Dictionary tool](members/domain_dictionary).

The dictionary under `doc/lineage/` covers both the raw `cms.*` tables
(MBSF and MEDPAR files, the Bronze layer) and the derived `medicare.*`
tables, and reflects the current data model including the OREC/CUREC
redesign of the QC layer (`consistent_orec` in the `qc_enrl_bene` view,
`consistent_curec` on the `enrollments` table); see
[Entitlement reason codes: OREC and CUREC](Medicare.md#entitlement-reason-codes-orec-and-curec).
The [Medicare data model definition](members/medicare_yaml.md) remains
the authoritative source from which these pages are generated.

```{note}
**These pages are generated at build time.** The dictionary and lineage
pages under `doc/lineage/` are derived entirely from the domain
definitions and are *not* committed to the repository;
`build_documentation.sh` regenerates them on every documentation build
(and refuses to build the site if generation fails). To generate them
locally — for example, to preview the documentation with a plain
`sphinx-build` — run the tool *from the `doc/lineage/` directory* (the
table and column lists are written to the current working directory)
and pass **both** domain files, the raw schemas first, so that
cross-domain lineage resolves:

    cd doc/lineage
    python -m dorieh.platform.dictionary.domain_dictionary \
        --fmt svg --lod min --mode sphinx -o medicare.dot \
        ../../src/python/dorieh/cms/models/medicare_cms.yaml \
        ../../src/python/dorieh/cms/models/medicare.yaml

The `*.eps` files in this directory are point-in-time exports used as
figure sources for the companion book; the tool does not modify them.
```
              
The general structure of the generated dictionary is:

* Main [table-level data lineage diagram](lineage/medicare.dot.md) showing the order of the
  data processing and the dependencies between tables.
* If the diagram is generated using SVG format, then every table
  is clickable, linked to a file with the table description.
* Every table description file includes verbal description, SQL or DDL
  used to create the table and the list of all columns in the table.
  Each column is linked to another file with detailed description
  for this column.
* Each column description file contains a description of the column
  and a lineage diagram for teh column showing what columns in which tables
  have been used to compute the value of this column. The SVG
  diagram is clickable and every element is linked to the description
  file for the column.
* File, containing [alphabetical list of all columns in all tables](lineage/column-list.md).
  For every column a list of tables in which the column is present
  is displayed. During transformation process columns are
  transferred from one table to another, hence a column usually is present in
  multiple tables.

       


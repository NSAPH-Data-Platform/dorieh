# Data Modeling Extensions: Federated Views Across Years

This page is the authoritative reference for the extensions to the
Dorieh data-modeling DSL. The extensions add directives for building
federated views over collections of tables that describe the same
data but differ in column names and types from year to year. The core
DSL — domains, tables, columns, `create` statements, validation — is
documented in [Data Modeling for Dorieh Data
Platform](Datamodels.md); this page covers only the additional
directives. Extensions described here are used by
[](members/mcr_combine_tables).

```{seealso}
**Further reading:** Appendix B of the companion book
[*Research Data that Can Be Trusted*](about-the-book.md) covers the
same DSL extensions. This page is the maintained, authoritative
reference. This documentation is self-contained; the book is optional
enrichment.
```

## Combining multiple sources and optional columns

Source can be an array of columns rather than one column.

The following block will define a column named `ssa3`. The tool
will look for columns named either `cnty_cd`, or `bene_county_cd`, or
`ssa_county` to map to the new `ssa3` column. If none of these three columns 
is found, a new column will be created and filled with NULL values.

Without `optional: true`, if an appropriate source column is not found,
an exception will be raised.

```yaml
- ssa3:
    optional: true
    description: Social Security Administration (SSA) three digit code for county
    reference: https://www.nber.org/research/data/ssa-federal-information-processing-series-fips-state-and-county-crosswalk
    source:
      - cnty_cd
      - bene_county_cd
      - ssa_county
```

The `description` and `reference` keys are documentation metadata:
they are included in the generated data dictionary but do not cause
any data to be fetched. The NBER page cited above documents the
SSA-to-FIPS crosswalk that gives these county codes their meaning;
the crosswalk itself is loaded into the database by the separate
`dorieh.platform.crosswalks.ssa2fips` utility (see the "Linking with
nomenclature" section of
[Data Modeling for Dorieh Data Platform](Datamodels.md)).


## Exclude

The `exclude` key removes specific tables from a federated view even
when their names match the union's inclusion patterns.

The following example creates a view by combining all tables matching either
`cms.mbsf_ab*` or `cms.mcr_bene_*` pattern, but excluding the table named 
`mbsf_ab_2015`:

```yaml
ps:
  create:
    type: view
    from:
      - cms.mbsf_ab*
      - cms.mcr_bene_*
    exclude:
      - mbsf_ab_2015


```

## Cast

It is possible to define custom casts from one type to another. When tables
to be combined into a single view have columns containing corresponding data
but of different types, it is possible to cast all of them to the same type.

In the following example:

```yaml
- dob:
    type: date
    cast:
      "character varying": "public.parse_date({column_name})"
      numeric: "to_date(to_char({column_name}, '00000000'), 'YYYYMMDD')"
      "*": "{column_name}::DATE"
```

* If a source column is of type `DATE`, it will be left as is
* If the source column is of numeric type, the code 

      to_date(to_char({column_name}, '00000000'), 'YYYYMMDD')
  will be used to transform the source value
* If the source column has type `character varying`, then the function
   `public.parse_date` will be called to transform the value
* For all other types a simple PostgreSQL cast will be attempted 

```{note}
The wildcard key `*` must be quoted (`"*"` or `'*'`) to be valid
YAML: an unquoted asterisk starts a YAML alias and fails to parse.
Likewise, values beginning with `{`, such as
`"{column_name}::DATE"`, must be quoted because an unquoted brace
starts a YAML flow mapping. Inside the cast expression,
`{column_name}` is substituted with the name of the actual source
column.
```

If the type of a source column differs from the declared target
`type` and the `cast` mapping contains neither an entry for the
source type nor a `"*"` entry, the tool raises an error stating that
the cast is not defined.

## Validating consistency of data across tables

There is no dedicated "consistency validation" directive in the DSL.
Validating that data is consistent across the combined tables is
achieved by composing features documented on this page and in the
core reference:

* the candidate source lists and [casts](#cast) described above
  harmonize columns that differ in name and type across years into
  single, uniformly typed columns of the federated view;
* [identifier columns and the `{identifiers}`
  token](Datamodels.md#identifier-columns-and-the-identifiers-token)
  let a grouped view count records that
  disagree on the attributes that define an entity's identity (see
  the `discrepancies` column of the `_beneficiaries` view in
  `medicare.yaml`);
* disambiguation rules
  ([defined in The Dorieh approach](concepts.md#disambiguation-rules))
  computed in grouped views surface
  conflicting values instead of silently dropping them: for example,
  in `medicare.yaml` the beneficiary's `dob` is defined as
  `MIN(dob)` while `dob_latest` is non-null only when the source
  records disagree, and the derived `consistent_dob` flag classifies
  each beneficiary as `CONSISTENT`, `AMBIGUOUS` or `MISSING`;
* the `invalid.records` machinery of the core DSL journals records
  that fail primary key, referential integrity or duplicate checks
  into an audit table (see the "Invalid Record" section of
  [Data Modeling for Dorieh Data Platform](Datamodels.md)).

The `qc_*` views of `medicare.yaml` show all of these techniques
working together over a federated view.




# About the Companion Book

This documentation and the book *Research Data that Can Be Trusted*
describe the same open-source platform and are written by the same
authors. The two are designed to complement each other: the
documentation is self-contained and free — every page can be read,
and every example can be run, using only the code and configuration in
this repository together with openly available data (synthetic where the
real data would require a data use agreement) — while the book offers an extended
conceptual treatment of the ideas behind the platform, including data
provenance, the regulatory context for health data, and a taxonomy of
data transformations. The book is optional enrichment; it is never a
prerequisite for anything in this documentation.

## Bibliographic information

* Title: *Research Data that Can Be Trusted*
* Authors: Bouzinier et al.
* Series: SpringerBriefs in Computer Science
* Publisher: Springer, 2026
* Link: <https://tidd.ly/4y1ClDH>

```{image} img/awin_qrcode.png
---
alt: QR code linking to the book Research Data that Can Be Trusted
target: https://tidd.ly/4y1ClDH
width: 160px
---
```

Scan the QR code (or follow the link above) to get the book.

## Chapter-to-documentation map

Each book chapter that describes the platform (Chapters 5–8 and the
appendices) has a single canonical landing page in this documentation;
the earlier chapters cover conceptual background (provenance, the
regulatory context, a taxonomy of transformations) with no direct code
counterpart:

| Book chapter                                                | Documentation page                                                                     |
|-------------------------------------------------------------|----------------------------------------------------------------------------------------|
| Ch. 5, "Language Design"                                    | [Concepts: the Dorieh approach](concepts.md)                                           |
| Ch. 6, "Proof of Concept Implementation"                    | [Concepts: the Dorieh approach](concepts.md)                                           |
| Ch. 7, "Sample Application: Building ML-Ready Datasets"     | [Climate tutorial](tutorial/climate/index.md)                                           |
| Ch. 8, "Dorieh Medicare Claims Data Pipeline"               | [Medicare case study](Medicare.md) and the [Medicare pipeline tutorial](tutorial/medicare/building-medicare-pipeline.md) |
| Appendix A (core YAML DSL syntax)                           | [Data modeling reference](Datamodels.md)                                               |
| Appendix B (DSL extensions)                                 | [Data modeling extensions](DataModellingExtensions.md)                                 |

## Using this documentation without the book

If you do not have the book, the following reading order covers the
same ground end to end:

1. Read [Why a data platform](rationale.md) for the motivation behind
   the platform, then [Concepts: the Dorieh approach](concepts.md) for
   the vocabulary and design ideas used throughout the documentation.
   (If you already know the motivation, start directly with Concepts.)
2. Work through the
   [climate tutorial](tutorial/climate/index.md),
   a runnable Bronze–Silver–Gold pipeline built on open data.
3. Follow the
   [Medicare tutorial](tutorial/medicare/building-medicare-pipeline.md),
   a guided path through the same patterns applied to a
   production-scale health data pipeline (runnable with synthetic
   data), with the [Medicare case study](Medicare.md) as its
   reference.
4. Consult the DSL reference — [Data modeling](Datamodels.md) and
   [Data modeling extensions](DataModellingExtensions.md) — when you
   write your own data models.

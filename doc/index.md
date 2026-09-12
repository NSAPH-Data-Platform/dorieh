# Dorieh Data Platform

Dorieh is an open-source data platform for building trustworthy,
ML-ready datasets for environmental and public health research. The
documentation is organized as a narrative: it starts with why the
platform exists and the ideas behind it, walks through the data
domains and pipelines it supports, teaches the platform with two
worked examples (a climate pipeline tutorial and a Medicare case
study), and closes with the data modeling DSL reference, platform
internals, and operational guides.

The concepts behind the platform are developed in depth in the book
[*Research Data that Can Be Trusted*](https://tidd.ly/4y1ClDH)
(Bouzinier et al., Springer, 2026), written by the Dorieh authors; see
[About the companion book](about-the-book.md) for how its chapters map
to these pages. The documentation is self-contained — the book is
optional enrichment.

**Key pages**

* [The Dorieh approach](concepts.md)
* [Learning paths](paths/index.md) — guided routes for researchers,
  developers, operators, book readers and auditors
* [Climate pipeline tutorial](tutorial/climate/index.md)
* [Medicare tutorial](tutorial/medicare/building-medicare-pipeline.md)
  with [Medicare.md](Medicare.md) as its reference
* [DSL reference](Datamodels.md)
* [About the companion book](about-the-book.md)

```{toctree}
---
maxdepth: 2
caption: Overview
---
Introduction <home>
Why a data platform <rationale>
The Dorieh approach <concepts>
The companion book <about-the-book>
Citing Dorieh <citing>
```

```{toctree}
---
maxdepth: 2
caption: Learning paths
---
Choose your path <paths/index>
```

```{toctree}
---
maxdepth: 2
caption: Data domains and pipelines
---
domains
pipelines
```

```{toctree}
---
maxdepth: 2
caption: Tutorials and worked examples
---
Tutorials
examples
```

```{toctree}
---
maxdepth: 2
caption: Data dictionaries
---
dictionaries
```

```{toctree}
---
maxdepth: 2
caption: Data modeling DSL reference
---
Datamodels
```

```{toctree}
---
maxdepth: 2
caption: Platform
---
Python Packages <packages>
guts
Platform capabilities <capabilities>
```

```{toctree}
---
maxdepth: 2
caption: Operational guides
---
DBT
Adding more data <adding_data>
Executing containerized apps <AppPipelineGenerator>
```

```{toctree}
---
maxdepth: 2
caption: Reference
---
Terms and Acronyms <glossary>
docindices
```

# Citing Dorieh

## Preferred citation: the book

The methodology behind Dorieh is developed in the companion monograph.
If you use the platform or its ideas in academic work, please cite the
book:

> Bouzinier, M., Etin, D., Khoshnevis, N., Shad, M., Yockel, S. (2026).
> *Research Data that Can be Trusted.* SpringerBriefs in Computer
> Science. Springer.
> <https://doi.org/10.1007/978-3-032-21032-6>

```bibtex
@book{bouzinier2026trusted,
  author    = {Bouzinier, Michael and Etin, Dmitry and Khoshnevis, Naeem
               and Shad, Max and Yockel, Scott},
  title     = {Research Data that Can be Trusted},
  series    = {SpringerBriefs in Computer Science},
  publisher = {Springer},
  year      = {2026},
  isbn      = {978-3-032-21031-9},
  doi       = {10.1007/978-3-032-21032-6}
}
```

Individual chapters have their own DOIs
(`10.1007/978-3-032-21032-6_1` … `_14`); the chapters describing the
platform implementation are:

| Chapter | Title | DOI |
|---|---|---|
| 6 | Proof of Concept Implementation | [10.1007/978-3-032-21032-6_6](https://doi.org/10.1007/978-3-032-21032-6_6) |
| 7 | Sample Application: Building ML-Ready Datasets | [10.1007/978-3-032-21032-6_7](https://doi.org/10.1007/978-3-032-21032-6_7) |
| 8 | Dorieh Medicare Claims Data Pipeline | [10.1007/978-3-032-21032-6_8](https://doi.org/10.1007/978-3-032-21032-6_8) |

See [About the companion book](about-the-book.md) for how the book's
chapters map to the pages of this documentation.

## Citing the software itself

To reference a specific release of the code (for example, to state
exactly which version produced a result), use the software archive on
Zenodo. Every GitHub release of Dorieh is archived there.

* **Concept DOI** (always resolves to the latest archived release —
  cite it when referring to Dorieh as an evolving project):
  [10.5281/zenodo.22728722](https://doi.org/10.5281/zenodo.22728722)
* **Version DOI** (one per release — cite it when the exact code
  matters, e.g. reproducibility of a specific analysis); for release
  0.5.1 it is
  [10.5281/zenodo.22728723](https://doi.org/10.5281/zenodo.22728723),
  and the DOI for any other release is listed on the concept DOI's
  landing page.

The DOI badge in the repository
[README](https://github.com/ForomePlatform/dorieh#readme) always
points at the latest archived release. The repository's
`CITATION.cff` powers GitHub's *Cite this repository* button with the
same information.

The package is distributed on PyPI as
[`dorieh`](https://pypi.org/project/dorieh/).

## Citing the tutorials

The [climate pipeline tutorial](tutorial/climate/index.md) and the
[Medicare tutorial](tutorial/medicare/building-medicare-pipeline.md)
complement, respectively, chapters 7 and 8 of the book. Unlike the
book, they continue to evolve with the platform. When they are
published as citable lessons, their DOIs will be listed here; until
then, cite the book chapter together with the software DOI.

## Citing the synthetic dataset

The synthetic Medicare-like dataset used by the examples is published
on Zenodo under concept DOI
[10.5281/zenodo.18915557](https://doi.org/10.5281/zenodo.18915557),
which always resolves to the newest version. Cite the version DOI
shown on the Zenodo landing page for the specific version you used.

# Introduction to the Dorieh Data Platform

This page surveys the platform's building blocks, how to deploy it,
and how to build this documentation. For the ideas behind the
platform, read [Why a data platform](rationale.md); for the vocabulary
that organizes the rest of the documentation, read
[The Dorieh approach](concepts.md).

```{contents}
---
local:
---
```

## Introduction to Data Platform

```{note}
**Using this documentation with (or without) the book.**
This documentation is a self-contained companion to the book
*Research Data that Can Be Trusted* (Bouzinier et al., Springer, 2026):
both describe the same open-source platform, and no page here requires
the book. See [About the companion book](about-the-book.md) for the
chapter-to-page map and a suggested reading order. Read
[Why a data platform](rationale.md) for the motivation, then
[The Dorieh approach](concepts.md) for the vocabulary that organizes
the rest of the documentation.
```

<!-- section Dorieh overview from README -->


A discussion of the aims of this data platform and how reproducible
research benefits from it is provided in
[Why a data platform](rationale).

## Building Blocks
        

### Dorieh Utilities

<!-- section Overview of Utilities from dorieh.utils -->


The dorieh.utils package is intended to hold python 
code that will be useful
across multiple portions of the Dorieh pipelines.

The included utilities are developed to be as independent of
specific infrastructure and execution environment as possible.

Included utilities:

* Interpolation code
* Reading FST files from Python [](members/pyfst)
* Reading FWF files [](members/fwf)
* various I/O wrappers [](members/io_utils)
* An API and CLI framework [](members/context)
* QC Framework



<!-- end of section overview of utilities from dorieh.utils -->

### Core Platform

<!-- section Core platform overview from dorieh.platform -->


### Dorieh GIS Utilities

<!-- section GIS Library Overview from dorieh.gis -->


### Dorieh Documentation Utilities

<!-- section Documentation utilities overview from dorieh.docutils -->



### Data Processing and Loading Pipelines

See [dedicated Pipelines page](pipelines) for additional details.

Fully tested and supported pipelines are listed in the
[Pipelines](pipelines) page. At this moment, we have published processing
pipelines for all [Data Domains](domains) except Demographics. Health
data pipelines are developed against restricted data, but a fully
synthetic Medicare-like dataset is openly published, so the Medicare
pipeline can be run and tested end to end; see the
[Medicare example](medicare-example.md), the
[Medicare tutorial](tutorial/medicare/building-medicare-pipeline.md)
and its reference, the [Medicare case study](Medicare.md).

To include additional data in a deployed data-platform instance 
go to [Adding more data](adding_data) section.

Pipelines can be tested with
[DBT Pipeline Testing Framework](DBT)

## Working with NSAPH containerized apps

<!-- section Introduction from dorieh.AppPipelineGenerator -->


[National Studies on Air Pollution and Health](https://www.hsph.harvard.edu/nsaph/)
organization (NSAPH) publishes containerized applications to produce
certain types of data. These applications are published on the
[NSAPH Data Production GitHub](https://github.com/NSAPH-Data-Processing).

The Pipeline Generator generates a 
[CWL](https://www.commonwl.org/) pipeline to execute the app and ingest
the data it produces into Dorieh Data warehouse.

The process of data ingestion consists of two steps:

1. Generation of the pipeline for data ingestion
2. Execution of the pipeline

             
<!-- end of section introduction from dorieh.apppipelinegenerator -->

## Deployment

Dorieh can be installed as a Python package, run from a prebuilt Docker
image, or deployed as a full Docker-Compose stack (described in
[Why a data platform](rationale.md#architecture)).

The Python package can be installed with a single command:

    pip install dorieh

or, if FST support is desired:

    pip install dorieh[FST]
                      
To run workflows one also needs a [CWL implementation](https://www.commonwl.org/implementations/).

We have tested deployment with the following CWL [implementations](https://www.commonwl.org/implementations/):

* [Toil](https://toil.readthedocs.io/en/latest/running/cwl.html).
* [CWL reference implementation](https://github.com/common-workflow-language/cwltool),
  primarily using [cwlref-runner ](https://pypi.org/project/cwlref-runner/) package
* [CWL-Airflow](https://cwl-airflow.readthedocs.io/en/latest/) that provides a very nice
  Airflow graphical user interface (GUI) for running workflows.

We suggest using [Toil](https://toil.ucsc-cgl.org/). To install Toil just run the following command
in your Python Virtual Environment:

    pip install "toil[cwl,aws]"

A prebuilt Docker image with Dorieh is available from DockerHub. Pull it to your local
machine using

    docker pull forome/dorieh

command. The image is built for Intel/AMD and ARM CPUs. ARM architecture is used in AWS Graviton2
processors that, according to AWS, deliver up to 40% better price performance. ARM CPUs are also used
by latest Mac computers.

If you would like to modify the container please refer to the [README](docker_readme.md) in the docker directory.


## Using the Database

To get started with querying the database, see a
[sample query](SampleQuery) and a discussion of
[querying Medicaid health data](QueringMedicaid).

## Terms and Acronyms 

Included 
[Glossary](glossary.md) provides some information about
acronyms and other terms used throughout this documentation.

Additionally, [General Index](genindex) and [Python Module Index](modindex) 
provide direct access to the Dorieh components. 


## Building Platform documentation

The [documentation](https://foromeplatform.github.io/dorieh/)
combines general pages in
[Markdown](https://www.markdownguide.org/) format with API pages
generated from the source tree; the
[build_documentation](https://github.com/ForomePlatform/dorieh/blob/main/build_documentation.sh)
script builds the combined site published on
[GitHub Pages](https://pages.github.com/).

To build documentation:

1. Clone Dorieh project:

        git clone https://github.com/ForomePlatform/dorieh.git
2. Cd into the project directory:

        cd dorieh
3. Create virtual environment (e.g., named `.dorieh`):

        python -m venv .dorieh
4. Run [build_documentation](https://github.com/ForomePlatform/dorieh/blob/main/build_documentation.sh) shell script:

        source .dorieh/bin/activate && ./build_documentation.sh

To integrate Markdown with [Sphinx](https://www.sphinx-doc.org/en/master/) 
processing we use [MyST Parser](https://jupyterbook.org/en/stable/content/myst.html). 

See [Documentation Utilities](docutils) package. 

## Next steps

Continue with [Why a data platform](rationale.md) for the motivation
behind the platform, then [The Dorieh approach](concepts.md) for the
ideas and vocabulary that organize the rest of this documentation.

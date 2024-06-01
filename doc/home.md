# NSAPH Data Platform: Documentation Home
 **User and Development Documentation**

 [Index](genindex)

```{contents}
---
local:
---
```

## Introduction to Data Platform

<!-- section Dorieh overview from README -->


A discussion on what are the aims of this data platform and how reproducible 
research can benefit from such product is provided in the
[What is Data Platform](rationale) section.

The data platform is deployed as a set of Docker containers orchestrated by
Docker-Compose. Conda (package manager) environment files and Python
requirements are used to build Docker containers satisfying the dependencies.
Specific parameters can be customized via environment files and shell script
callbacks.

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


The data platform provides generic functionality for Dorieh Data Platform
with APIs and command line utilities dependent on the infrastructure
and the environment. For instance, its components assume presence of PostgreSQL
DBMS (version 13 or later) and CWL runtime environment.

Some mapping (or crosswalk) tables are also included in the Core
Platform module. These tables include between different
territorial codes, such as USPS ZIP codes, Census ZCTA codes,
FIPS codes for US states
and counties, SSA codes for codes for US states
and counties. See more information in the
[Mapping between different territorial codes](https://nsaph-data-platform.github.io/nsaph-platform-docs/common/core-platform/doc/TerritorialCodes.html)

<!-- end of section core platform overview from dorieh.platform -->

### Dorieh GIS Utilities

<!-- section GIS Library Overview from dorieh.gis -->


Per [USGS](https://www.usgs.gov/faqs/what-geographic-information-system-gis), 
a Geographic Information System (GIS) is a computer system that 
analyzes and displays geographically referenced information. 
It uses data that is attached to a unique location.

This `dorieh.gis` library contains several modules, aimed to work with US Census shape files. 
They fall into two categories:

* Utilities to download appropriate shapefiles for a given geography type and year
* Utilities to aggregate raster data over given shapefiles 

<!-- end of section gis library overview from dorieh.gis -->

### Dorieh Documentation Utilities

<!-- section Documentation utilities overview from dorieh.docutils -->


Documentation utilities to simplify creation of consistent
documentation for Dorieh platform 
                                                         
* [cwl2md](members/cwl2md) Generates [Markdown](https://www.markdownguide.org/basic-syntax/) 
    documentation for a CWL tool or workflow
* [collector](members/collector) Generates automatic 
    [reStructuredText](https://docutils.sourceforge.io/rst.html) 
    templates for all Python modules 
* [copy_section](members/copy_section)  Copies a specified section from one markdown document
    to another. This way we can collect summaries in one file<!-- end of section documentation utilities overview from dorieh.docutils -->

Documentation utilities to simplify creation of consistent
documentation for Dorieh platform 
                                                         
* [cwl2md](members/cwl2md) Generates [Markdown](https://www.markdownguide.org/basic-syntax/) 
    documentation for a CWL tool or workflow
* [collector](members/collector) Generates automatic 
    [reStructuredText](https://docutils.sourceforge.io/rst.html) 
    templates for all Python modules 
* [copy_section](members/copy_section)  Copies a specified section from one markdown document
    to another. This way we can collect summaries in one file<!-- end of section documentation utilities overview from dorieh.docutils -->


### Data Processing and Loading Pipelines

See [dedicated Pipelines page](pipelines) for additional details.

Fully tested and supported pipelines are listed in the
[Pipelines](pipelines) page. At this moment, we have published processing
pipelines for all [Data Domains](domains) except Demographics. However,
it is not possible to test health data processing pipelines without
access to the same health data that was used for their development.

To include additional data in a deployed data-platform instance 
go to [Adding more data](adding_data) section.

Pipelines can be tested with
[DBT Pipeline Testing Framework](common/core-platform/doc/DBT)

## Working with NSAPH containerized apps

<!-- section Introduction from dorieh.AppPipelineGenerator -->


## Deployment

The deployment repository is based on  
CWL-Airflow Docker Deployment developed
by Harvard FAS RC in collaboration with Forome Association. Essentially, this is a fork of: 
[Apache Airflow + CWL in Docker with Optional Conda and R](https://github.com/ForomePlatform/airflow-cwl-docker)
It follows 
[Infrastructure as Code (IaC)](https://en.wikipedia.org/wiki/Infrastructure_as_code) 
approach.

[Harvard FAS RC Superset] repository is a fork of 
[Apache Superset](https://superset.apache.org/) 
customized for Harvard FAS RC environment.

Detailed description of this deployment is covered in the [NSAPH Data Platform Deployment](common/platform-deployment/doc/index) subsection of the [Data Platform Internals](guts) section.

### Using the Database

For a sample to query the database, please look at
[Sample Query](common/core-platform/doc/SampleQuery)

A discussion of querying of health data can be found in 
[this document](common/cms/doc/QueringMedicaid)

## Terms and Acronyms 

Included 
[Glossary](glossary.md) provides some information about
acronyms and other terms used throughout this documentation.

Additionally, [General Index](genindex) and [Python Module Index](modindex) 
provide direct access to the Dorieh components. 


## Building Platform documentation

The [documentation](https://nsaph-data-platform.github.io/dorieh/)
contains general documentation pages in 
[MarkDown](https://www.markdownguide.org/) 
format and a build script that goes over all other platform 
repositories in the platform
and creates a combined [GitHub Pages](https://pages.github.com/) site.
The script supports links between repositories. 

To build documentation:

1. Clone Dorieh project:

        git clone https://github.com/NSAPH-Data-Platform/dorieh.git
2. Cd into the prject directory:

        cd dorieh
3. Create virtual environment (e.g., named `.dorieh`):

        python -m venv .dorieh
4. Run [build_documentation](https://github.com/NSAPH-Data-Platform/dorieh/blob/main/build_documentation.sh) shell script:

        source .dorieh/bin/activate && ./build_documentation.sh

To integrate Markdown with [Sphinx](https://www.sphinx-doc.org/en/master/) 
processing we use [MyST Parser](https://jupyterbook.org/en/stable/content/myst.html). 

See [Documentation Utilities](docutils) package. 

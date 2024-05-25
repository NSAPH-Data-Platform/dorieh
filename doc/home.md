# NSAPH Data Platform: Documentation Home
 **User and Development Documentation**

 [Index](genindex)

```{contents}
---
local:
---
```

## Introduction to Data Platform

This data platform is intended for development and deployment of 
ETL/ELT pipelines that includes complex data processing and data 
cleansing workflows. Complex workflows require a workflow language, 
and we have chosen 
[Common Workflow Language (CWL)](https://www.commonwl.org/).
For deployment, we have selected CWL-Airflow to take advantage of the excellent
user interface allowing for the control of the actual execution process. 
The data is eventually stored in a PostgreSQL DBMS; many processing steps 
in the [included data processing pipelines](pipelines) 
are being run inside the database itself. 

The data platform is based on a combination of an 
[Infrastructure as Code (IaC) approach](https://en.wikipedia.org/wiki/Infrastructure_as_code) 
and CWL. Beside tools written in widely used languages such as 
Python, C/C++ and
Java, the platform also supports tools written in R and PL/pgSQL.
Data platform consists of several [python packages](packages), 
a [package to deploy the platform](#deployment)
using [CWL-Airflow](https://cwl-airflow.readthedocs.io/en/latest/)
and a number of data ingestion pipelines. 
[Data ingestion pipelines](pipelines)
process data from external sources and load it into the database.

A discussion on what are the aims of this data platform and how reproducible research can benefit from such product is provided in the
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


### Dorieh GIS Utilities

<!-- section GIS Library Overview from dorieh.gis -->


### Dorieh Documentation Utilities

<!-- section Documentation utilities overview from dorieh.docutils -->



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

Additionaly, [General Index](genindex) and [Python Module Index](modindex) englobe all the pieces of the Data Platform together.


## Building Platform documentation

The [documentation](https://nsaph-data-platform.github.io/dorieh/)
contains general documentation pages in 
[MarkDown](https://www.markdownguide.org/) 
format and a build script that goes over all other platform 
repositories in the platform
and creates a combined [GitHub Pages](https://pages.github.com/) site.
The script supports links between repositories. The 
[README.md](../README.md) file contains
Build instructions.

To integrate Markdown with [Sphinx](https://www.sphinx-doc.org/en/master/) 
processing we use [MyST Parser](https://jupyterbook.org/en/stable/content/myst.html). 

See [Documentation Utilities](docutils) package. 

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
        
The building blocks of the data platform are packaged in several repositories:

* The **NSAPH utilities** repository https://github.com/NSAPH-Data-Platform/nsaph-utils
* The **core platform** repository https://github.com/NSAPH-Data-Platform/nsaph-core-platform
* The **GIS utilities** repository https://github.com/NSAPH-Data-Platform/nsaph-gis
* The **pipeline** repositories. Five pipelines, each focused in a different data domain have been implemented:
    + The **cms** repository https://github.com/NSAPH-Data-Platform/nsaph-cms
    + The **EPA** repository https://github.com/NSAPH-Data-Platform/nsaph-epa
    + The **gridmet** repository https://github.com/NSAPH-Data-Platform/nsaph-gridmet
    + The **census** repository https://github.com/NSAPH-Data-Platform/nsaph-census
* The **deployment** repository https://github.com/NSAPH-Data-Platform/nsaph-platform-deployment

General details of the building blocks are provided next. 

### NSAPH Utilities

<!-- section overview from dorieh.platform_utils -->


The nsaph_utils package is intended to hold python 
code that will be useful
across multiple portions of the NSAPH pipelines.

The included utilities are developed to be as independent of
specific infrastructure and execution environment as possible.

Included utilities:

* Interpolation code
* Reading FST files from Python
* various I/O wrappers
* An API and CLI framework
* QC Framework
* Documentation utilities to simplify creation of consistent 
 documentation for NSAPH platform 


<!-- end of section overview from dorieh.platform_utils -->

### Core Platform

<!-- section overview from dorieh.platform -->

The data platform provides generic infrastructure for NSAPH Data Platform
It depends on nsaph_util package, but it augments it
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

<!-- end of section overview from dorieh.platform -->

### GIS Utilities

<!-- section overview from gis -->


This library contains several packages, aimed to work with census shape files.

<!-- end of section overview from gis -->

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

The [documentation](https://github.com/NSAPH-Data-Platform/nsaph-platform-docs)
contains general documentation pages in 
[MarkDown](https://www.markdownguide.org/) 
format and a build script that goes over all other platform 
repositories in the platform
and creates a combined [GitHub Pages](https://pages.github.com/) site.
The script supports links between repositories. The 
[README.md](https://github.com/NSAPH-Data-Platform/nsaph-platform-docs/blob/main/README.md) file contains
Build instructions.

To integrate Markdown with [Sphinx](https://www.sphinx-doc.org/en/master/) 
processing we use [MyST Parser](https://jupyterbook.org/en/stable/content/myst.html). 

Documentation utilities are contained in 
[nsaph-utils](https://github.com/NSAPH-Data-Platform/nsaph-utils)
in 
[docutils](https://github.com/NSAPH-Data-Platform/nsaph-utils/tree/master/nsaph_utils/docutils)
package. 
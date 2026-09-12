# Why a data platform

```{contents}
---
local:
---
```

## Why we need a Data Platform 

Reproducible research is a keystone of modern scientific work. In data
engineering for data science it presents a challenge on two sides. On the one
hand, data is often retrieved from public and proprietary data sources that are
being continuously updated, requiring special attention to ensure that for
reproducibility purposes the same exact data sources are used. On the other
hand, data processing involves heavy floating-point computations which are very
sensitive to the exact computational environment. Differing operating systems
and/or versions of the tools and libraries might affect the result. Several
scientific communities proposed various standards to define portable
reproducible data processing workflows, with Common Workflow Language (CWL) 
having the widest adoption in both commercial and academic settings.

CWL defines pipelines declaratively rather than imperatively.
Reproducibility challenges are exacerbated when the research involves healthcare
data that is inherently confidential and cannot be shared publicly to ensure
reproducibility. A possible solution to this problem is to share infrastructure
instead, giving institutions the option to reproduce each other's results on
their own data in compliance with their own data usage agreements. In this
setting Infrastructure as Code (IaC) provides a handy way to ensure that the
infrastructure is identical during data processing.

## Architecture                                                 


Dorieh is based on a combination of an IaC approach and CWL. Besides
tools written in widely used languages such as Python, C/C++ and Java, it also
supports tools written in R and PL/pgSQL, making it, to the best of our
knowledge, one of the first deployment-ready platforms appropriate for ETL/ELT
pipelines. Dorieh workflows run on any open-source production-ready CWL
implementation, such as Toil, cwltool or CWL-Airflow. We initially adopted
CWL-Airflow for its graphical user interface, but in practice it proved
insufficiently stable and feature-complete, and its UI added only marginal
value; the platform has since moved to Toil, which — although it has no UI —
is fully functional and is the recommended runner (see
[Deployment](home.md#deployment)). The data is eventually
stored in a PostgreSQL DBMS; many processing steps are being run inside the
database itself. The data platform is deployed as a set of Docker containers
orchestrated by Docker-Compose. Conda (package manager) environment files and
Python requirements are used to build Docker containers satisfying the
dependencies. Specific parameters can be customized via environment files and
shell script callbacks.

One of the most important features of the data platform is support for advanced
security. We assume that the platform resides behind a strict firewall without
direct access to the Internet.

We use Git submodules to describe project dependencies and fetch all the code to
the local system before building the Docker containers.
         
## Supported Programming Languages and Tools

The execution environment requires a PostgreSQL database to function. While DBMS
can be automatically installed as a separate Docker container, it makes little
sense with a production database that is usually administered separately.
Therefore, a connection to an external DBMS server can be specified as an
alternative to the built-in containerized option. Optionally, we support Conda
package manager as a runtime environment, hence, individual CWL tools can be
written in the R programming language. We also support commands that are
executed inside PostgreSQL database, with tools written in one of the languages
supported by PostgreSQL runtime including PL/pgSQL. Other languages supported
for in-database data manipulation include PL/Tcl, PL/Perl, PL/TclU, PL/PerlU,
and PL/PythonU. Such tools can be executed either through a Python wrapper or
using psql utility that is by default installed in all containers. It is
possible to pre-build multiple Conda environments and/or multiple Python virtual
environments in all of the containers. One of the defined environments can be
designated as default, though individual workflows have an option to select a
different environment for their execution.
                   
## Development Mode

In addition to production mode, the platform is designed to be used in
development mode. To enable development mode, users can define user projects and
place them in a special project subdirectory. User projects can be either
connected as Git submodules or copied to project subdirectory with any other
utility. They are automatically prebuilt into all of the runtime containers but
can also be updated in the running containers without rebuilding. We use user
projects to define specific pipelines.
    
## Where it can be deployed 

The platform has been deployed in the Harvard University’s FAS RC
high-performance computing (HPC) cluster on CentOS 7, on various versions of
Ubuntu and in the RedHat OpenShift cluster on IBM Cloud. At FAS RC, we use
Puppet to provision specific resources, while on IBM cloud, resource
provisioning is done with Terraform. 

## What makes Dorieh different

The sections above describe the infrastructure Dorieh runs on; what
distinguishes Dorieh from other IaC-plus-workflow stacks is what runs
on that infrastructure.

Dorieh pairs a declarative data-modeling language with a standard
workflow language. Data models — tables, columns, how each column is
derived, what constitutes a valid record — are written as YAML
definitions, while the orchestration of downloads, ingestion and
database steps is expressed in Common Workflow Language (CWL). Because
both layers are declarative, every transformation the platform performs
can be read and reviewed directly in the definitions, rather than being
buried inside ad-hoc scripts. The vocabulary used to describe these
definitions throughout this documentation is introduced in
[Concepts: the Dorieh approach](concepts.md).

The same definitions that execute also document themselves. The
[data dictionary tool](members/domain_dictionary.rst) reads the YAML
data model and the CWL workflow and generates human-readable
documentation, data dictionaries and lineage diagrams from them — for
example, the [Medicare data dictionary](MedicareLineage.md) and the
lineage pages produced in the
[climate tutorial](tutorial/climate/constructing-lineage.md). There is
no separately maintained specification that can drift away from the
code, because the specification *is* the code.

Validation failures are journaled, not silently dropped. When a record
fails ingestion — because it violates primary key integrity, breaks
referential integrity, or duplicates another record — the data model
can direct the loader to insert it into an audit table together with
the reason for the failure and a timestamp, instead of discarding it or
aborting the run. The rejected data remains queryable, so data-quality
problems can be quantified and investigated after the fact.

Lineage reaches down to the column and the row. Generated lineage
diagrams trace how each output column is computed from input columns
across pipeline layers, and the `file` and `record` column types record,
for every ingested row, the source file it came from and its position
within that file. Combined, these give cell-level provenance: for any
value in the warehouse it is possible to establish both the computation
that produced it and the raw input records it was derived from.

These properties are what the documentation means when it calls the
resulting data *trustworthy*: the same theme is developed at book
length in the companion volume — see
[About the companion book](about-the-book.md).

# Why Data Platform and what does it do?

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
having the widest adoption in both commercial and academic settings. CWL can be
used to define pipelines in imperative rather than procedural ways.
Reproducibility challenges are exacerbated when the research involves healthcare
data that is inherently confidential and cannot be shared publicly to ensure
reproducibility. A possible solution to this problem is to share infrastructure
instead, making an option for institutions to reproduce each other's results on
their own data in compliance with their own data usage agreements. In this
setting Infrastructure as Code (IaC) provides a handy way to ensure that the
infrastructure is identical during data processing.

## Architecture                                                 


The data platform is based on a combination of an IaC approach and CWL. Besides
tools written in widely used languages such as Python, C/C++ and Java, it also
supports tools written in R and PL/pgSQL, making it, to the best of our
knowledge, one of the first deployment-ready platforms appropriate for ETL/ELT
pipelines. Out of the four open-source production-ready CWL implementations, we
have selected CWL-Airflow to take advantage of the excellent user interface
allowing for the control of the actual execution process. The data is eventually
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

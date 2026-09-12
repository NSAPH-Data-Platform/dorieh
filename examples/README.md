# Examples of using Dorieh

These examples are also described in the Dorieh documentation: 
[Examples Documentation](https://foromeplatform.github.io/dorieh/examples.html).

<!-- toc -->

- [What is included](#what-is-included)
- [Installing Dorieh and testing the installation](#installing-dorieh-and-testing-the-installation)
  * [Running Python examples](#running-python-examples)
  * [Running CWL examples](#running-cwl-examples)

<!-- tocstop -->

## What is included

There are three types of examples:

* Using Dorieh without any database backend. There are limited operations
  that Dorieh can perform without a backend, for example spatial
  aggregations. These examples are in [no-db](no-db) directory.
* Using Dorieh with a PostgreSQL instance as a backend. With PostgreSQL as a
  backend, Dorieh is fully functional data
  platform. These examples are in [with-postgres](with-postgres) directory.

  If you just want to try Dorieh in non-production mode you can use included
  [docker-compose.yml](../docker/pg-hll/docker-compose.yml) to start a
  lightweight PostgreSQL instance. Corresponding connection configuration
  file [database.ini](with-postgres/database.ini) is included with the
  examples.

  The [with-postgres/climate](with-postgres/climate) example is the
  runnable Bronze/Silver/Gold (medallion) climate pipeline: it downloads
  gridded daily temperature data, aggregates it over ZCTA polygons, loads
  the result into PostgreSQL and builds the Bronze, Silver and Gold layers
  with the Dorieh data-modeling DSL. Its canonical, narrated version is the
  tutorial
  [Building a Bronze–Silver–Gold Climate Pipeline](https://foromeplatform.github.io/dorieh/tutorial/climate/building-climate-pipeline.html).

* Using Dorieh with [Apache Spark](https://spark.apache.
  org/docs/latest/index.html) as a 
  backend. Supporting Spark is a work in progress and only limited
  functionality is currently supported. We will be gradually adding more 
  features supported with PostgreSQL to Spark. Dorieh does not require 
  setting up an SQL Warehouse to use Spark, but if you need other 
  clients to connect to the backend and perform SQL queries, you might 
  consider using [Hive Metastore](https://spark.apache.
  org/docs/latest/sql-data-sources-hive-tables.html), or [Databricks]
  (https://www.databricks.com/), or [Trino](https://trino.io/). Spark
  examples are in [with-spark](with-spark) directory.

## Installing Dorieh and testing the installation

### Running Python examples

Before you try any of the examples, you need to ensure that Dorieh
is properly installed.

To run Python commands, you need to install Dorieh package in your
Python environment. We recommend creating a virtual environment or Conda
environment. You can use the following commands to do it (replace $path 
with some actual path on your local file system):

```shell
python3 -m venv $path
source $path/bin/activate
pip install "dorieh[FTS,spark]"
# Or
# pip install dorieh # without support for FST and Spark
```

Then you can run the following command to test the installation:

```shell
dorieh_version
```

If for any reason you cannot install Dorieh in your Python environment,
you can still use a Docker container:

```shell
docker run forome/dorieh dorieh_version
```
                                       
The above command can be run without Python, but needs Docker to be 
installed on your host system (e.g., your laptop or desktop or a cloud 
VM you are using).

### Running CWL examples
                     
To run CWL workflows you must have Python and install either 
[CWL Reference runner](https://cwltool.readthedocs.io/en/latest/) or 
[Toil](https://toil.readthedocs.io/en/latest/gettingStarted/install.html)
(or any other 
[CWL implementation](https://www.commonwl.org/implementations/)) in your  
virtual environment. 

Here we will guide you with Toil installation (replace $path 
with some actual path on your local file system):

```shell
python3 -m venv $path
source $path/bin/activate
pip install "toil[cwl,aws]"
```

There is no need to install Dorieh, though you can do it using commands 
above, in teh same virtual environment as Toil.

Run the following commands to test your installation:

```shell
toil-cwl-runner https://raw.githubusercontent.com/ForomePlatform/dorieh/refs/heads/main/src/workflows/version.cwl
```

and look for output like:

```text
=========>
	{"version": "0.4.0", "url": "https://github.com/ForomePlatform/dorieh", "commit": null}
<=========
```


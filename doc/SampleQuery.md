# How to query the database

```{contents}
---
local:
---
```

Here we show how to query the Dorieh database from Python.

We use public data (climate, pollution, census) in the query,
hence it can be executed in any environment.

## Setup
                             
To set up your execution environment, one can use either
Python Virtual Environment or Conda environment.

### Create Python Virtual Environment

First, we need to create a Python virtual environment. This can
be done with commands like:

```shell
python3 -m venv .dorieh
source .dorieh/bin/activate
```
                                                                    

### Creating Conda environment

To run the software on older operating systems, use Conda environment.

### Install Dorieh package

Next, we need to install Dorieh core packages. This can be done
using GitHub install:

```shell
python -m pip install dorieh
```

If you are getting errors installing dorieh package with FST format support (`dorieh[FST]`), if you see
errors like "R Home is not defined", you might need to set up
[Conda environment](#creating-conda-environment) 
instead of Python Virtual Environment.


## Create connection definition file

See also: [](DBConnections).

We need to create or update a database.ini file that stores connections
to the database. Here is a sample database.ini file:

```ini
[mimic]
host=localhost
database=mimicii
user=postgres
password=*****

[nsaph2]
host=dorieh.platform.cluster.uni.edu
database=nsaph
user=dbuser
password=*********
ssh_user=johndoe

[dorieh]
database=dorieh
secret=aws:region=us-east-1:name=nsaph/public/dorieh/

```

> Note that the first connection uses a local instance of PostgreSQL.
> The second connects to a database that is not accessible from a local machine.  
> It is using ssh
> tunnel to connect to a remote host that - this is defined by adding ssh_user parameter.
> The third connection uses 
> [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)
> to retrieve connection credentials.
>
> **johndoe** is a username for ssh while **dbuser** is a username for the database.


## Executing the query

We will use the following sample Python program to execute
a query (with public data) on a Dorieh database:
[query.py](members/sample_query)

Copy the file into your local directory and execute it:

```shell
python -u query.py database.ini nsaph2
```

## Using EXPLAIN to optimize queries

You do not want to run a query that will take a week to execute. When we have
hundreds of millions of records, this can easily happen. SQL is a declarative
language, hence, an SQL statement describes what you want to do. DBMS optimizer
decides how to do it. It should understand your query correctly. To ensure, it
did, use EXPLAIN query before trying to execute. See documentation for EXPLAIN.

Here are a few more links that might be useful:

* How to read [query plans](https://thoughtbot.com/blog/reading-an-explain-analyze-query-plan) produced by EXPLAIN
* [What is cost](https://scalegrid.io/blog/postgres-explain-cost/)

Unfortunately, less useful is the
[tutorial](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-explain/)
The queries below (given as examples) take 4 to 8 minutes each. I suggest
running them with EXPLAIN first, note the costs and compare them with any costs
of the queries you will write. Pay attention how indices are used: the most
expensive part is scan.


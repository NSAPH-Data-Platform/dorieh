# Managing database connections
                          
One of the most important functionalities of Dorieh data platform
is support for creating a data warehouse for storing an analysis of large
volumes of data. Moreover, Dorieh supports a rich set of in-database 
data transformations 
(see [Modelling data in Dorieh](Datamodels)). Dorieh assumes that the DBMS
used for data warehousing is an instance of  
[PostgreSQL](https://www.postgresql.org/docs/current/index.html)
version 13 or higher.

A preferred way to manage connections to a database is through a `.ini` file.  The following keys can
be used in the `.ini` file:

| Key              | Description                                                                                                   |
|------------------|---------------------------------------------------------------------------------------------------------------|
| host             | Specifies the host name of the machine on which the server is running                                         |
| database         | Specifies the name of the database to connect to                                                              | 
| user             | Connect to the database as the user `user`                                                                    |
| password         | Password to connect to the database                                                                           |
| ssh_user         | First, connect to the host using ssh and establish a tunnel. Connect as user `ssh_user`                       |
| application_name | Application name that is used by the server to identify processes initiated by this connection                |
| secret           | Use a secret manager to retrieve host, database, user and password. Currently AWS secret manager is supported |
   

Such a file contains URIs and credentials for database connections and can store multiple
entries. These entries can be either in a clear text or a reference to a Vault or a Secret Manager.

Dorieh supports connection that require creating an ssh tunnel to connect to a host 
on the same network as the DBMS.

Below is an example of database connection file storing 3 different ways to connect to 
a database.

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
application_name=my_awesome_app

[dorieh]
database=dorieh
secret=aws:region=us-east-1:name=nsaph/public/dorieh/

```

The first connection uses a local instance of PostgreSQL containing a copy of
[MIMIC-III Clinical Database](https://physionet.org/content/mimiciii/1.4/).

The second connects to a database that is not accessible from a local machine.  
It is using an ssh tunnel to connect to a remote host that has direct access. 
The tunnel is defined by adding an `ssh_user` parameter.
In this example **johndoe** is a username for ssh while **dbuser** is a username for the database.

This section also provides a custom application name that is sent to the DBMS server
to identify processes initiated by this connection. When application_name
is not provided it is constructed as `dorieh:{script or module name}`.

One can use [Database Monitor](MonitoringDB.md) to monitor in-database processes.
                                                
These options are appropriate for development and debugging, but are not secure enough for any 
production. The third connection uses
[AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)
to retrieve connection credentials. In this case security is provided by AWS.

> Note: in some cases it might be required to specify an 
> [AWS profile](https://docs.aws.amazon.com/cli/v1/userguide/cli-configure-files.html)
> to be able to access the Secrets Manager. This is done by setting an environment variable.
> See the following example:

     export AWS_PROFILE=dorieh
                              
> defines that an AWS profile named `dorieh` will be used to retrieve credentials from
> the Secrets Manager.



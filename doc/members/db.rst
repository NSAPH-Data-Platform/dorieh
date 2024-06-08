Database connection API
=======================

Use ini file to define database connections. The first block
in the example below connect directly to the database, while the
second block uses ssh tunnel to connect to database host. The third
example retrieves database connection credentials from
AWS Secrets Manager.

For details, see `Managing databases connections <DBConnections>`_

.. code-block:: ini
   :caption: Example of database.ini file

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

.. automodule:: dorieh.platform.db
   :members:
   :undoc-members:


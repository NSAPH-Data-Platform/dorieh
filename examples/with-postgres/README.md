# Using Dorieh with PostgreSQL Backend

If you just want to try Dorieh in non-production mode you can use included
[docker-compose.yml](../../docker/pg-hll/docker-compose.yml) to start a
lightweight PostgreSQL instance. Corresponding connection configuration
file [database.ini](database.ini) is included with the
examples.

If you have a running instance of PostgreSQL, please create your own
`database.ini` file as described in the 
[documentation](https://foromeplatform.github.io/dorieh/DBConnections.html).
                                                                            
The following commands assume that you are using the provided 
lightweight PostgreSQL server.

> **Disk space:** when loading a sizable dataset (for example the
> [Medicare example](medicare/README.md)), make sure Docker has enough
> disk allocated. On Docker Desktop the limit that matters is the virtual
> machine disk (Settings → Resources → Disk usage limit), not the free
> space on your host. If PostgreSQL runs out of space mid-load it enters a
> recovery crash loop and refuses connections; the symptom and the recovery
> steps are described in the Medicare example's
> [troubleshooting section](medicare/README.md#31-troubleshooting-postgresql-runs-out-of-disk-space).

Start the server (Docker and `git` must be installed; replace $workdir with 
some actual path on your local file system):

```shell
cd $workdir
git clone https://github.com/ForomePlatform/dorieh.git 
cd docker/pg-hll/
docker compose up
# Or: docker compose up -d # to run in the background 
```

Now, test that you can connect to the database:

```shell
cd $workdir/dorieh/examples/with-postgres 
# Or, if you ran the previous block with `-d` option:
# cd ../../examples/with-postgres/
docker run -v ./database.ini:/tmp/database.ini forome/dorieh python -m dorieh.platform.util.psql  --connection dorieh --db /tmp/database.ini 'SELECT version();'
```

Alternatively, if you have Dorieh installed locally in a virtual 
environment, you do not need `docker`. See [General README](../README.md)
for installation tips. Then you can run:

```shell
cd $workdir/dorieh/examples/with-postgres
source $pat_to_dorieh_virtual_env/bin/activate 
python -m dorieh.platform.util.psql  --connection localhost --db database.ini 'SELECT version();'
```

Finally, if you do not have Dorieh installed but have a CWL implementation,
e.g., Toil (see [General README](../README.md)) or just want to test 
that you can connect to the database from your workflows, use the 
following commands:

```shell
cd $workdir/dorieh/examples/with-postgres
source $pat_to_toil_virtual_env/bin/activate 
toil-cwl-runner https://raw.githubusercontent.com/ForomePlatform/dorieh/refs/heads/main/src/workflows/handshake.cwl --database database.ini --connection dorieh 
cat grant.log
```





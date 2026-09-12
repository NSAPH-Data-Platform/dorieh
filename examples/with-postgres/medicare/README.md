# Running the sample Medicare processing workflow (with PostgreSQL)

> **Note:** The canonical, always-current copy of this guide is
> [Example: Medicare Processing Pipeline (with PostgreSQL)](https://foromeplatform.github.io/dorieh/medicare-example.html)
> on the documentation site (source: [`doc/medicare-example.md`](../../../doc/medicare-example.md)).

<!-- toc -->


The Medicare example demonstrates a full Dorieh data processing pipeline 
against a **synthetic** dataset. 

## 1. Prerequisites

Before starting, make sure you have:

1. Followed the PostgreSQL setup in 
   [Using Dorieh with PostgreSQL Backend](../README.md) 
   (PostgreSQL running,   `database.ini` available).
2. Installed Toil and tested it as in [Examples of using Dorieh](../../README.md)
3. Cloned the `dorieh` repository under `$WORKDIR`.
4. **Enough disk space allocated to Docker.** The synthetic 5M-beneficiary
   dataset grows the PostgreSQL data volume past 20 GB during ingestion,
   plus WAL. On Docker Desktop the limit that matters is the *virtual
   machine* disk (Settings → Resources → Disk usage limit), not the free
   space on your host: allocate at least 100 GB before running this
   example. See [Troubleshooting](#31-troubleshooting-postgresql-runs-out-of-disk-space)
   below for what the failure looks like.

Then go to the Medicare example directory:

```bash
cd $WORKDIR/dorieh/examples/with-postgres/medicare
```


## 2. Download synthetic sample data from Zenodo

The synthetic Medicare‑like database from Zenodo:

- Mimics raw fixed‑width files
- Reproduces the structure of the ResDAC File Transfer Summary (FTS) layouts
- Contains **no real PHI/PII**, so it’s safe for testing and demonstrations

Download and unpack it:

```bash
curl -fLo medicare-synthetic-database.zip \
  'https://zenodo.org/records/18915558/files/medicare-synthetic-database-v1.zip?download=1'

unzip medicare-synthetic-database.zip
```

The archive unpacks into `data/<cohort>/<year>/` with the fixed-width `.dat`
files and, next to each of them, the ResDAC-style FTS layout file the loader
reads. The layouts ship inside every dataset bundle (their source of truth is
the synthetic data generator), so nothing else needs to be present under
`data/` — do not unpack the archive *inside* an existing `data/` directory,
or the files end up nested one level too deep (`data/data/...`).

> **Note:** This pins **version 1** of the dataset (about 770 MB, roughly
> 600,000 synthetic beneficiaries) so the results are reproducible. Newer,
> larger versions — including v0.2.0 with five million beneficiaries (about
> 9 GB compressed) — are published under the same concept DOI
> <https://doi.org/10.5281/zenodo.18915557>. Any version runs through the
> same pipeline commands; only the download URL, size, run time, and
> resulting counts differ.

### Using the latest dataset version instead

The link above pins a specific version for a reproducible walkthrough.
The dataset's **concept DOI**,
<https://doi.org/10.5281/zenodo.18915557>, always resolves to the
newest version — open it in a browser to see (and download) the latest
release. To fetch the latest version's archive from the command line,
resolve it through the Zenodo API:

```bash
LATEST_ZIP=$(curl -sL https://zenodo.org/api/records/18915557 \
  | python3 -c "import sys,json; \
      f=[f for f in json.load(sys.stdin)['files'] if f['key'].endswith('.zip')][0]; \
      print(f['links']['self'])")
curl -fLo medicare-synthetic-database.zip "$LATEST_ZIP"
unzip medicare-synthetic-database.zip
```

(`https://zenodo.org/api/records/18915557` is the concept record: Zenodo
redirects it to the latest version, whatever it is at the time.) Newer
versions are larger — see the disk-space prerequisite above — and run
through the same pipeline commands; only sizes, run times, and resulting
counts differ.


### 3. Run the Medicare processing pipeline

Activate your Toil environment:

```bash
source $TOIL_VENV/bin/activate
```

Run the Medicare workflow:

```bash
toil-cwl-runner \
  --jobStore j1 \
  --retryCount 1 \
  --cleanWorkDir never \
  --outdir outputs \
  --workDir . \
  https://raw.githubusercontent.com/ForomePlatform/dorieh/refs/heads/main/src/workflows/medicare.cwl \
  --input data/ \
  --database https://raw.githubusercontent.com/ForomePlatform/dorieh/refs/heads/main/examples/with-postgres/database.ini \
  --connection_name dorieh
```

> **Note:** `src/workflows/medicare.cwl` (used in the command above) and
> `src/cwl/medicare.cwl` (cited elsewhere, including in the companion book)
> are the same workflow — the files are byte-identical except for a single
> leading blank line — and both paths are kept in the repository.

After completion:

- Processed data will be stored in your PostgreSQL backend.
- Additional outputs may be written to the `outputs/` directory, depending on the workflow definition.



### 3.1 Troubleshooting: PostgreSQL runs out of disk space

If the ingestion step (`load_medicare_data`) fails with:

```
psycopg2.OperationalError: connection to server ... failed:
FATAL:  the database system is not yet accepting connections
DETAIL:  Consistent recovery state has not been yet reached.
```

the PostgreSQL container has almost certainly filled its disk. Confirm with
`docker logs <postgres container>` — the telltale sign is a *crash loop*:
recovery completes, then the end-of-recovery checkpoint dies, repeatedly:

```
PANIC:  could not write to file "pg_logical/replorigin_checkpoint.tmp": No space left on device
LOG:  checkpointer process ... was terminated by signal 6: Aborted
LOG:  database system was not properly shut down; automatic recovery in progress
```

On Docker Desktop this means the *Docker VM* disk is full even when the host
has plenty of space; check with:

```bash
docker system df                       # what is using the space
docker run --rm alpine df -h /        # free space inside the Docker VM
```

To recover:

1. Free any amount of space — PostgreSQL recovers by itself as soon as the
   checkpoint can be written; no data committed before the failure is lost.
   Safe reclaims that touch no data volumes:

   ```bash
   docker buildx prune -a    # build cache
   docker image prune        # dangling images
   ```

2. Raise the Docker Desktop disk limit (Settings → Resources → Disk usage
   limit) before restarting the workflow, or the ingestion will fill the
   disk again.

3. Restart the failed workflow (the Toil job store from the failed run can
   be reused with `--restart`).

## 4. (Optional) Explore the Medicare data in Superset

You can visually explore the processed Medicare data using a pre‑built 
**Superset** dashboard.      

### 4.1 Stop the simple PostgreSQL container (if running)

If you previously started the simple PostgreSQL setup 
as described in [Using Dorieh with PostgreSQL Backend](../README.md), do:

```bash
cd $WORKDIR/dorieh/docker/pg-hll/
docker compose down
```

You will now start a more complete stack: PostgreSQL orchestrated together with Superset.

### 4.2 Start PostgreSQL + Superset via Docker Compose

From the same directory, first create the `.env` file that the Superset
stack requires. `SUPERSET_SECRET_KEY` has no default and Compose will refuse
to start without it:

```bash
cd $WORKDIR/dorieh/docker/pg-hll/
cp .env.template .env
# Generate a secret key and write it into .env:
python -c "import secrets; print(secrets.token_hex(42))"
# then edit .env and replace the ???? placeholder on the SUPERSET_SECRET_KEY line
```

`.env` is deliberately excluded from version control, so this step is
required on every fresh clone. Every other variable in `.env.template`
(ports, Superset version, admin credentials) already has a working default.

Then:

```bash
cd $WORKDIR/dorieh/docker/pg-hll/
docker compose -f docker-compose-superset.yml up --build
# Or, to run detached:
# docker compose -f docker-compose-superset.yml up -d
```


**If PostgreSQL was ever started in this directory before** (either compose
stack), the `pgdata` volume already exists and PostgreSQL will *not* re-run
the `init-db/` scripts — they execute only when the data directory is
initialized for the first time. In that case the `superset` metadata database
is missing and Superset fails with `FATAL: database "superset" does not
exist`. Create it manually in the running `postgres` container:

```bash
docker compose exec postgres psql -U dorieh -d dorieh -c 'CREATE DATABASE superset WITH OWNER dorieh;'
```

This brings up:

- PostgreSQL
- Superset web UI
- Superset worker services


### 4.3 Initial Superset login and admin setup

Once the services are up, open:

- `http://localhost:8088/` in your browser.

On a successful first‑time initialization, you should be able to log in with:

- **Username:** `admin`  
- **Password:** `admin`  

(These defaults are defined in 
[docker-compose-superset.yml](../../../docker/pg-hll/docker-compose-superset.yml)
.)

If initialization did not complete and you cannot log in, create the admin user manually:

```bash
cd $WORKDIR/dorieh/docker/pg-hll/
docker compose exec superset superset fab create-admin \
  --username admin \
  --firstname Admin \
  --lastname User \
  --email admin@example.com \
  --password admin
```

Then log in at `http://localhost:8088/` with the admin credentials.


### 4.4 Configure the Dorieh database connection in Superset

In the Superset web UI:

1. In the top right corner, open **Settings → Database Connections**  
   (below  *Security*, under *Data*, above *Manage*).
2. Click the **+ DATABASE** button.
3. Choose **PostgreSQL**.
4. When the configuration dialog opens, scroll to the bottom and click  
   **“Connect this database with a SQL Alchemy URL string instead”**.
5. Enter:

   - **DISPLAY NAME:** `DORIEH`  
   - **SQLALCHEMY URI:** `postgresql+psycopg2://dorieh:dorieh_secret@postgres:5432/dorieh`

6. Click **TEST CONNECTION**.  
   If the test succeeds, click **CONNECT** in the bottom right corner of 
   the dialogue.


### 4.5 Import the pre‑built Medicare quality‑control dashboard

The dashboard is committed as a native Superset bundle under
`examples/with-postgres/medicare/superset/medicare_quality_dashboard/`. Import
it by running the `dorieh.platform.superset.import_dashboard` module, which resolves
your `DORIEH` connection by name, re‑points the bundle onto it on the fly, and
imports it via Superset's REST API (the native importer the UI uses — the legacy
`superset import-dashboards` CLI silently drops the charts from native bundles):

```bash
python3 -m dorieh.platform.superset.import_dashboard \
  $WORKDIR/dorieh/examples/with-postgres/medicare/superset/medicare_quality_dashboard \
  --base-url http://localhost:8088/ --username admin
```

You'll be prompted for the admin password (`admin` by default). The importer
uses only the Python standard library — no extra packages beyond Dorieh.

Notes:

- It binds to the connection named `DORIEH` that you created in § 4.4 (override
  with `--connection-name`). Because each Superset instance assigns its own
  connection UUID, the command looks the UUID up by name at import time rather
  than relying on a value baked into the bundle — so the same committed bundle
  imports on any machine.
- Re‑running updates the same dashboard in place instead of creating a
  duplicate (object uuids are preserved, so the import is idempotent — it never
  multiplies charts or datasets).
- To stand up a *second* dashboard on a different connection (e.g. a `DORIEH2`
  comparison while developing), add `--copy`: `--copy --connection-name DORIEH2
  --dashboard-name "…"`. `--copy` regenerates the object uuids so the dev copy
  coexists with — rather than overwrites — the canonical one. (Without `--copy`
  it would update the same objects, just repointed to the other connection.)
- The companion `export_dashboard <dashboard-id>` command exports a dashboard
  back to a native bundle (e.g. to refresh this committed one).


### 4.6 Explore the dashboard

In the Superset UI:

1. Click on the **Dashboards** tab.
2. You should see a dashboard named **“Medicare Demo Quality Dashboard”**.
3. Open it and explore the available charts and filters to examine data quality and other aspects of the synthetic Medicare data processed by Dorieh.




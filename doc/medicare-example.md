# Example: Medicare Processing Pipeline with Synthetic Data

```{contents}
---
local:
---
```

```{seealso}
* [Medicare: Building a Data Warehouse from ResDac Files](Medicare.md) —
  the case-study reference documentation
* [Building the Medicare Claims Pipeline](tutorial/medicare/building-medicare-pipeline.md) —
  the guided tutorial
* [Using HLL for Approximate Count Distinct](UsingHLL.md) — how the QC
  tables count distinct beneficiaries
* [Using Dorieh with PostgreSQL Backend](https://github.com/ForomePlatform/dorieh/tree/main/examples/with-postgres) —
  environment setup for all PostgreSQL examples
```

This example demonstrates a full Dorieh data processing pipeline running
against a local PostgreSQL database, using a **publicly available synthetic**
Medicare-like dataset.  Because the data are
synthetic and published openly on [Zenodo](https://doi.org/10.5281/zenodo.18915557),
no institutional data access agreement is required to follow this example.
It covers:

* Downloading synthetic sample data from Zenodo
* Running the Medicare CWL workflow with [Toil](https://toil.readthedocs.io/en/latest/)
  against a local PostgreSQL instance
* (Optional) Exploring the results in a pre-built
  [Apache Superset](https://superset.apache.org/) dashboard

The source files for this example live in
[`examples/with-postgres/medicare/`](https://github.com/ForomePlatform/dorieh/tree/main/examples/with-postgres/medicare).

---

## Prerequisites

Before starting, make sure you have:

1. **PostgreSQL running** and a `database.ini` ready — follow the steps in
   [Using Dorieh with PostgreSQL Backend](https://github.com/ForomePlatform/dorieh/tree/main/examples/with-postgres).
   If you want a quick non-production setup, use the bundled Docker Compose file:

   ```bash
   cd $WORKDIR/dorieh/docker/pg-hll/
   docker compose up -d
   ```

2. **Toil installed** and tested — see the [Examples](examples.md) page
   for installing Dorieh and testing the installation.

3. The **`dorieh` repository cloned** under `$WORKDIR`:

   ```bash
   git clone https://github.com/ForomePlatform/dorieh.git $WORKDIR/dorieh
   ```

4. **Enough disk space allocated to Docker.** The synthetic 5M-beneficiary
   dataset grows the PostgreSQL data volume past 20 GB during ingestion,
   plus WAL. On Docker Desktop the limit that matters is the *virtual
   machine* disk (Settings → Resources → Disk usage limit), not the free
   space on your host: allocate at least 100 GB before running this example.
   The failure mode when space runs out is described in
   [Troubleshooting](#troubleshooting-postgresql-runs-out-of-disk-space)
   below.

Then move into the Medicare example directory:

```bash
cd $WORKDIR/dorieh/examples/with-postgres/medicare
```

---

## Step 1 — Download synthetic sample data

The synthetic Medicare-like dataset is hosted on
[Zenodo](https://zenodo.org/records/18915558) and is **publicly available** —
no data use agreement or institutional access is required.  It:

* Mimics the raw fixed-width files (`.dat`) delivered by ResDAC
* Reproduces the File Transfer Summary (FTS) layout metadata
* Contains **no real PHI / PII** — it is safe for testing, demonstrations,
  and sharing

Download and unpack it (about a 770 MB download):

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

```{note}
This example pins **version 1** of the dataset (about 770 MB, roughly 600,000
synthetic beneficiaries) so that the numbers in this walkthrough — and the
golden test values shipped with Dorieh — are reproducible. Newer, larger
versions, including v0.2.0 with five million beneficiaries (about 9 GB
compressed), are published under the same concept DOI:
<https://doi.org/10.5281/zenodo.18915557>. Any version runs through the same
pipeline commands; only the download URL, size, run time, and resulting
counts differ.

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
```

The extracted directory tree follows the layout expected by the ingestion
pipeline — one sub-directory per year, each containing `.fts` metadata files
and the corresponding `.dat` data files.

---

## Step 2 — Run the Medicare processing pipeline

Activate your Toil virtual environment:

```bash
source $TOIL_VENV/bin/activate
```

Run the Medicare CWL workflow:

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

```{note}
`src/workflows/medicare.cwl` (used in the command above) and
`src/cwl/medicare.cwl` (cited elsewhere, including in the companion book)
are the same workflow — the files are byte-identical except for a single
leading blank line — and both paths are kept in the repository.
```

After the workflow completes:

* Processed data is stored in your PostgreSQL backend under the `medicare`
  schema (beneficiaries, enrollments, admissions, and QC tables).
* Any additional output files are written to the `outputs/` directory.

For a detailed description of the pipeline steps, see
[Medicare: Building a Data Warehouse from ResDac Files](Medicare.md).


### Troubleshooting: PostgreSQL runs out of disk space

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

---

## Step 3 (Optional) — Explore results in Apache Superset

A pre-built **Medicare Quality Control** Superset dashboard is included with
the example.  The steps below show how to launch PostgreSQL together with
Superset using Docker Compose and import the dashboard.

### 3.1 — Stop the simple PostgreSQL container (if running)

If you started the basic `docker-compose.yml` stack earlier, bring it down
first:

```bash
cd $WORKDIR/dorieh/docker/pg-hll/
docker compose down
```

### 3.2 — Start PostgreSQL + Superset

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

Then start the extended stack:

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

* A PostgreSQL instance (with the HLL extension)
* The Superset web UI
* Superset background worker services

### 3.3 — Log in to Superset

Once the services are running, open `http://localhost:8088/` in your browser.

Default credentials (defined in `docker-compose-superset.yml`):

| Field    | Value   |
|----------|---------|
| Username | `admin` |
| Password | `admin` |

If initialization did not complete and you cannot log in, create the admin
user manually:

```bash
cd $WORKDIR/dorieh/docker/pg-hll/
docker compose exec superset superset fab create-admin \
  --username admin \
  --firstname Admin \
  --lastname User \
  --email admin@example.com \
  --password admin
```

### 3.4 — Add the Dorieh database connection

In the Superset UI:

1. Open **Settings → Database Connections** (under *Data*).
2. Click **+ DATABASE** and choose **PostgreSQL**.
3. At the bottom of the dialog click
   **"Connect this database with a SQL Alchemy URL string instead"**.
4. Fill in:
   * **Display Name:** `DORIEH`
   * **SQLAlchemy URI:** `postgresql+psycopg2://dorieh:dorieh_secret@postgres:5432/dorieh`
5. Click **TEST CONNECTION** — if it succeeds, click **CONNECT**.

### 3.5 — Import the Medicare QC dashboard

The dashboard is committed as a native Superset bundle under
`examples/with-postgres/medicare/superset/medicare_quality_dashboard/`. Import
it by running the `dorieh.platform.superset.import_dashboard` module, which resolves
your `DORIEH` connection by name, re-points the bundle onto it on the fly, and
imports it through Superset's REST API (the native importer the UI uses):

```bash
python3 -m dorieh.platform.superset.import_dashboard \
  $WORKDIR/dorieh/examples/with-postgres/medicare/superset/medicare_quality_dashboard \
  --base-url http://localhost:8088/ --username admin
```

Enter the admin password when prompted (`admin` by default). The importer
is standard-library-only. Because each Superset instance assigns its own
connection UUID, it looks the UUID up by name at import time rather than relying
on a value baked into the bundle, so the same committed bundle imports on any
machine. Re-running updates the dashboard in place (uuids are preserved, so the
import is idempotent and never multiplies charts or datasets); add `--copy`
(with `--connection-name` / `--dashboard-name`) to stand up an independent
coexisting copy on another connection. The companion
`export_dashboard <dashboard-id>` command exports a dashboard back to a native
bundle.

### 3.6 — Explore the dashboard

In the Superset UI:

1. Click the **Dashboards** tab.
2. Open **"Medicare Demo Quality Dashboard"**.
3. Use the available charts and filters to examine data quality across
   enrollments and admissions for the synthetic dataset.

The dashboard surfaces the QC metrics described in
[Creating QC Tables](Medicare.md#creating-qc-tables), including:

* Percent of beneficiaries with consistent date-of-birth / date-of-death
  records
* Percent of valid admission records (passed primary-key, foreign-key, and
  duplicate checks)
* Approximate distinct-beneficiary counts computed with
  [HLL sketches](UsingHLL.md)

Note that all numbers shown are produced from the synthetic dataset and
differ from any figures computed on real Medicare data.

---

## What the pipeline produces

After a successful run the following tables and views are available in the
`medicare` schema of your PostgreSQL database:

| Object                    | Type              | Description                                      |
|---------------------------|-------------------|--------------------------------------------------|
| `medicare.ps`             | View              | Federated patient summary across all raw years   |
| `medicare.beneficiaries`  | Table             | One row per unique beneficiary (deduplicated)    |
| `medicare.enrollments`    | Table             | Yearly enrollment records per beneficiary/state  |
| `medicare.admissions`     | Table             | Validated inpatient admission records            |
| `medicare_audit.admissions` | Table           | Records that failed validation (with reason)     |
| `medicare.qc_enrollments` | Materialized View | Aggregate QC dimensions for enrollments          |
| `medicare.qc_admissions`  | Materialized View | Aggregate QC dimensions for admissions           |

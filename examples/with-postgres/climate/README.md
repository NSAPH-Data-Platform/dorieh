# Climate Medallion Example: Bronze / Silver / Gold Pipeline

> **Canonical source.** The canonical, narrated version of this example is
> the tutorial
> [doc/tutorial/climate/building-climate-pipeline.md](../../../doc/tutorial/climate/building-climate-pipeline.md)
> (docs site:
> [tutorial/climate/building-climate-pipeline.html](https://foromeplatform.github.io/dorieh/tutorial/climate/building-climate-pipeline.html));
> the `.cwl`/`.yml` files here are verbatim copies of the files there —
> if they ever differ, the `doc/tutorial/climate` copies win.

## What this example builds

The workflow [example1.cwl](example1.cwl) orchestrates the complete
pipeline developed in the tutorial:

1. Data download (gridded daily climate data, band `tmmx` —
   maximum daily temperature).
2. Shape download (ZCTA shapefiles from the US Census website).
3. Spatial aggregation of the gridded data over ZCTA polygons.
4. Database initialization.
5. Bronze ingestion.
6. Silver view creation.
7. Gold materialized view creation.

The data model [example1_model.yml](example1_model.yml) defines the
`tutorial` domain with three relations:

* `bronze_temperature` — a table with 3 columns: `tmmx` (Kelvin),
  `date`, `zcta`; the aggregated data loaded as-is.
* `silver_temperature` — a view with 7 columns: the 3 Bronze columns
  plus `temperature_in_C`, `temperature_in_F`, `us_state`, `city`.
* `gold_temperature_by_state` — a materialized view with 5 columns:
  `us_state`, `date`, `t_span`, `t_mean_in_C`, `t_mean_in_F`, grouped
  by state and date.

Note: as shipped, the ingestion and creation steps in `example1.cwl`
resolve the data model from the raw GitHub URL of
`doc/tutorial/climate/example1_model.yml` (the canonical copy). The
`example1_model.yml` in this directory is a verbatim reference copy.

## Prerequisites

* A Unix-like environment (Linux or macOS).
* Python 3.12+.
* A CWL runner, e.g. `toil-cwl-runner` (used below) or `cwltool`.
* PostgreSQL, or Docker to use the provided container image.

Install Toil and Dorieh into a virtual environment (replace `$path`
with an actual path on your local file system):

```shell
python3 -m venv $path
source $path/bin/activate
pip install "toil[cwl,aws]"
pip install dorieh
```

## Database configuration

If you do not have a running PostgreSQL instance, start the provided
lightweight container:

```shell
git clone https://github.com/ForomePlatform/dorieh.git
cd dorieh/docker/pg-hll
docker compose up -d
```

The connection configuration file [../database.ini](../database.ini)
defines two connections to this container (both on port 55432):

* `localhost` — `host=localhost`, for commands running directly on
  your host;
* `dorieh` — `host=host.docker.internal`, for commands running inside
  a Docker container.

The workflow's `database` input defaults to the copy of
`examples/with-postgres/database.ini` on GitHub, and `connection_name`
defaults to `localhost`, so when you run against the provided container
from your host you do not need to pass either parameter. To use your
own PostgreSQL instance, create your own `database.ini` as described in
the [database connections documentation](https://foromeplatform.github.io/dorieh/DBConnections.html)
and pass `--database path/to/database.ini --connection_name <section>`.

## Run: a single-day "toy" run

The workflow is parameterized by a `date` so it can run on a toy
dataset — a single day — for quick feedback:

```shell
toil-cwl-runner --retryCount 3 --cleanWorkDir never --outdir outputs example1.cwl --workDir . --band tmmx --date 2019-01-15 --geography zcta
```

If successful, the output directory contains a gzipped CSV file
(`tmmx_zcta_polygon_2019.csv.gz`, columns: `date`, `zcta`, `tmmx`) and
the database contains the three relations listed above. If the run
fails, follow the
[troubleshooting documentation](https://foromeplatform.github.io/dorieh/pipelines.html#troubleshooting-workflows-run-by-toil).

## Verify the results

Run the following queries with any SQL client, or with the Dorieh
utility, e.g. from this directory:

```shell
python -m dorieh.platform.util.psql --connection localhost --db ../database.ini 'SELECT * FROM bronze_temperature ORDER BY date, zcta LIMIT 10;'
```

The verification queries from the tutorial:

```sql
-- Inspect Bronze
SELECT * FROM bronze_temperature
ORDER BY date, zcta
LIMIT 10;

-- Inspect Silver
SELECT date, zcta, temperature_in_C, us_state, city
FROM silver_temperature
ORDER BY date, zcta
LIMIT 10;

-- Inspect Gold: which state was hottest on 2019-01-15?
SELECT us_state, t_mean_in_C, t_span
FROM gold_temperature_by_state
WHERE date = '2019-01-15'
ORDER BY t_mean_in_C DESC
LIMIT 10;
```

## See also

* The narrated tutorial:
  [Building a Bronze–Silver–Gold Climate Pipeline](https://foromeplatform.github.io/dorieh/tutorial/climate/building-climate-pipeline.html).
* A database-free variant of the climate workflow (stops at the CSV
  file): [../../no-db](../../no-db).
* General notes on running examples against PostgreSQL:
  [../README.md](../README.md).

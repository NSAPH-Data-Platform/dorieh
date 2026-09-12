# Tutorial: Building a Bronze–Silver–Gold Climate Pipeline with Dorieh

```{contents}
---
local:
---
```

```{seealso}
[Example: aggregating a climate variable](../../Example-climate-workflow.md)
```
            
## Introduction 

This tutorial walks you through building a small, but complete, 
Dorieh‑based data processing workflow. It attempts to model a realistic 
process of incrementally adding features to a workflow, keeping the 
workflow runnable at every step but with the ultimate goal of producing 
a production-ready dataset.

The eventual pipeline:

* Downloads gridded daily climate data.
* Aggregates it over ZIP Code Tabulation Areas (ZCTAs).
* Loads the result into PostgreSQL.
* Builds Bronze, Silver, and Gold layers using the Dorieh data‑modeling DSL.
* Generates documentation and data lineage diagrams.

The same design patterns apply directly to health and claims data 
pipelines; here we use open climate data so anyone can reproduce the 
example.   

```{seealso}
**Further reading:** Chapter 7 ("Sample Application: Building ML-Ready
Datasets") of the companion book
[*Research Data that Can Be Trusted*](../../about-the-book.md) develops the
ideas behind this page in depth. This documentation is self-contained; the
book is optional enrichment.
```


## Prerequisites

You will need:

* A Unix‑like environment (Linux or macOS).
* Python 3.12+.
* A CWL runner, e.g.:
  * toil-cwl-runner (used in examples), 
  * or cwltool.
* PostgreSQL or Docker to use the provided container image
* graphviz (for lineage diagrams) and pandoc (optional, for HTML docs).

Dorieh must be installed as described in the 
[Example](../../Example-climate-workflow.md#prepare-to-run-a-workflow).

For convenience, the full list of commands is also provided below:

```bash
# Create a virtual environment and activate it.
python3 -m venv $path
source $path/bin/activate

# Install Toil and its dependencies.
pip install "toil[cwl,aws]"

# Install Dorieh and its dependencies.
pip install dorieh
```

## Design overview
We briefly outline the pipeline design before touching any code.

### Inputs

* Climate variable: daily maximum temperature (tmmx) from a gridded 
dataset (e.g., GRIDMET / TerraClimate via Google Earth Engine / NKN).

```{Important}
As we will be progressing with the building of the workflow we 
will see that we also need an additional input: shapefile with 
ZIP Code Tabulation Areas (ZCTAs).
```

### Outputs
* **File output**: a compressed CSV with columns: date, zcta, and tmmx 
(Kelvin).
* **Database outputs**:
  * Bronze table: bronze_temperature(date, zcta, tmmx).
  * Silver view: silver_temperature with:
     * temperature_in_C, temperature_in_F
     * us_state, city
  * Gold materialized view: gold_temperature_by_state with three
    computed columns per state/day:
     * t_mean_in_C (mean temperature in Celsius)
     * t_mean_in_F (mean temperature in Fahrenheit)
     * t_span (temperature span, i.e. the spread between the warmest
       and the coldest ZCTA in the state on that day)

### Architecture
We will:

* Use **CWL** to orchestrate:
  * climate download → shape download → spatial aggregation → DB init 
   → ingestion → Silver/Gold creation.
* Use the **Dorieh data‑modeling DSL (YAML)** to define:
  * Bronze/Silver/Gold schema and transformations.
* Use Dorieh utilities to generate:
  * Workflow documentation (from CWL).
  * Data dictionaries and lineage diagrams (from YAML).

### How this pipeline was designed

The design starts from the data itself. The climate variable comes from
gridMET, a gridded daily surface meteorological dataset produced by the
University of Idaho. The workflow downloads it as one NetCDF file per year
from the Northwest Knowledge Network (the download step in `example1.cwl`
composes a URL of the form
`https://www.northwestknowledge.net/metdata/data/<band>_<year>.nc`), and the
band vocabulary — `tmmx` is the daily maximum temperature, stored in
Kelvin — follows the gridMET catalog published on
[Google Earth Engine](https://developers.google.com/earth-engine/datasets/catalog/IDAHO_EPSCOR_GRIDMET#bands).

Next comes the question of who consumes the result and in what form. This
pipeline serves two kinds of consumers: file-oriented users (for example, ML
feature engineering scripts) receive a compressed CSV keyed by date and ZCTA,
while SQL users receive tables in PostgreSQL organized as Medallion layers —
a Bronze table holding the ingested data as-is, a Silver view that cleans and
enriches it, and a Gold materialized view, `gold_temperature_by_state`, that
is directly ready for analysis.

Working backward from the outputs listed above tells us which transformations are
essential. Gridded NetCDF rasters cannot be ingested directly into most
DBMSs, so the grid must be aggregated over ZCTA polygons *outside* the
database, before ingestion — this is the aggregation step. That step, in
turn, surfaces a need that was not obvious at the outset: aggregating over
ZCTAs requires their boundaries, so the design acquires TIGER/GENZ
shapefiles from the US Census website as an additional input, discovered
while examining the aggregation tool's parameters. Everything after
ingestion is expressed declaratively in the data model: unit conversions
from Kelvin to Celsius and Fahrenheit, enrichment of ZIP codes with state
abbreviations and city names through the built-in `zip_to_state` and
`zip_to_city` functions, and finally the state-level aggregation that
produces the Gold layer.

With sources, outputs, and transformations fixed, the topology follows
almost mechanically: two independent acquisitions (the year's NetCDF and
the year's shapefiles) feed the spatial aggregation, whose output is then
ingested and refined layer by layer — exactly the chain shown in the
[Architecture](#architecture) list above.

Quality control and provenance are designed in rather than bolted on. The
Bronze table declares a primary key (`zcta`, `date`), so key integrity is
enforced at the ingestion boundary; each layer is defined only from the
layer directly below it (Silver from Bronze, Gold from Silver), so the
model file records the full derivation of every column and Dorieh can
render it as data dictionaries and lineage diagrams (see
[Constructing lineage](constructing-lineage.md)). Every step also emits its
logs as workflow outputs, so each run leaves a record of what was done.

The rest of this tutorial constructs exactly this workflow, one step at
a time.

## Directory layout

Create a working directory for this tutorial, for example:

```bash
cd tmp
mkdir -p dorieh/tutorials/climate
cd dorieh/tutorials/climate
```
We will place:

* example1.cwl – the CWL workflow.
* example1_model.yml – the domain definition for Bronze/Silver/Gold.
* (Optionally) a local database.ini if you need to adjust it for your 
   environment.
                                        
## Step 1. Create a minimal CWL workflow skeleton

We will start with a minimal CWL workflow definition containing the 
first two main steps—data acquisition and aggregation. 
At this stage, placeholders can be used for inputs and outputs; 
these will be filled in as more details on the required tool 
parameters are gathered.    

Dorieh provides a library of prebuilt CWL tool definitions, 
streamlining common steps such as downloading remote files and 
running aggregations. Corresponding tools are:

* [download.cwl](../../pipeline/download.md)
* [aggregate.cwl](../../pipeline/aggregate_daily.md)



The initial workflow skeleton can look like:

:::{toggle} Expand Code Block
```{literalinclude} steps/step1/example1.cwl
:linenos:
:language: yaml
```
:::


This skeleton is not yet runnable. It defines two steps but no 
inputs, outputs, or wiring.                

## Step 2. Iteratively Defining Steps and Parameters

At this implementation step we need to:

* For each workflow step, consult the underlying tool’s 
  documentation or CWL file to determine:
  * Required input parameters
  * Output files and directory structure
* Incrementally add inputs (e.g., band, year, geography), outputs, 
  and wiring between steps (using CWL’s in and out sections).

Dorieh’s cwl_collect_outputs utility helps automating extraction of 
output specifications and minimizing errors. 

To illustrate the process, we will first look at the download step.
The tool we are using is 
[Dorieh download.cwl](../../pipeline/download.md)

We see that it takes 3 input parameters: 

* proxy settings, 
* year, for which we will be performing data aggregation 
* meteorological band or variable that we would like to aggregate. 

If you are using a system with direct access to the Internet, you 
probably do not need a proxy. However, we need to take care of 
‘year’ and ‘band’.    

After adding these two input parameters to the ‘ inputs ’ section and 
‘download’ step, the workflow file will look like:  

:::{toggle} Expand Code Block
```{literalinclude} steps/step2/example1-1.cwl
:linenos:
:language: yaml
```
:::

Though we have now defined the inputs for the first step, the 
workflow is still not runnable because we have not yet defined the 
outputs. As mentioned, Dorieh’s cwl_collect_outputs utility assists 
with this task. You can run: 
                             
```bash
python -m dorieh.platform.util.cwl_collect_outputs download https://raw.githubusercontent.com/ForomePlatform/dorieh/refs/heads/main/src/cwl/download.cwl
```

The command should produce the following output:

```text
    out:
      - log
      - data
      - errors
## Generated by dorieh.platform.util.cwl_collect_outputs from download.cwl:
  download_log:
    type: File?
    outputSource: download/log
  download_data:
    type: File?
    outputSource: download/data
  download_errors:
    type: File
    outputSource: download/errors
```

From the standard output of this command, copy the “out” section to 
the step and the rest to the “outputs” section. You can exclude the 
outputs you want to ignore. The resulting workflow file should look 
like:    

:::{toggle} Expand Code Block
```{literalinclude} steps/step2/example1-2.cwl
:linenos:
:language: yaml
```
:::


Now we will repeat the process for the `aggregate` step. Looking at the 
tool we are using 
[aggregate.cwl](../../pipeline/aggregate_daily.md).
we notice that besides the input parameters we already discussed, it
also requires Shapefiles. Dorieh provides another CWL tool to 
download the shapefiles for US geographies (ZCTAs and counties) from 
the US Census website: [get_shapes.cwl](../../pipeline/get_shapes.md).  

Therefore, we need to add a third step to the 
existing two:

```yaml
  get_shapes:
    run: https://raw.githubusercontent.com/ForomePlatform/dorieh/main/src/cwl/get_shapes.cwl
```
                        
Which will bring us to the following workflow definition:

:::{toggle} Expand Code Block
```{literalinclude} steps/step2/example1-3.cwl
:linenos:
:language: yaml
```
:::


After repeating the process described above for the remaining two steps 
(`get_shapes` and `aggregate`) we finally have a runnable workflow 
definition:

:::{toggle} Expand Code Block
```{literalinclude} steps/step2/example1-4.cwl
:linenos:
:language: yaml
```
:::

At this point, the workflow can aggregate a full year of data, but 
that is slow for development. Next we add a “toy slice” mode. 

If you prefer to test the current workflow, and if you do not mind 
waiting hours for its completion, you can run it with the following 
command: 

```shell
toil-cwl-runner --retryCount 3 --cleanWorkDir never --outdir outputs example1.cwl --workDir . --band tmmx --year 2019 --geography zcta

```

## Step 3. Parameterize for a single day (“toy” run)

To speed up development and debugging, we can parameterize the 
workflow so that it can run on “toy” datasets—for example, filtering 
a single day (e.g., 2019-01-15) instead of an entire year. Running 
your pipeline on a minimal dataset ensures quick feedback, uncovers 
errors early, and avoids wasting compute resources.     

First, we need to modify the `inputs` section of the workflow:

```yaml
inputs:
  band:
    type: string
  date:
    type: string    # e.g. "2019-01-15"
  geography:
    type: string    # "zcta" or "county"
```

We must keep in mind that such parametrization often requires 
additional input transformations 
(e.g., extracting year from a date); hence, we need to insert 
transformation steps, chaining outputs via CWL’s valueFrom mechanism.       

In our case, to allow the workflow to run on a toy dataset, we will 
first replace the input parameter `year` with `date`. Our downstream 
steps, however, require a year, e.g., to download the right shape 
file. Hence, we will add an additional step to extract the year from 
the date:        
                
```yaml
  extract_year:
    run: https://raw.githubusercontent.com/ForomePlatform/dorieh/main/src/cwl/parse_date.cwl
    in:
      date: date
    out:
      - year
```

With these changes in place, the workflow is now:

:::{toggle} Expand Code Block
```{literalinclude} steps/step3/example1.cwl
:linenos:
:language: yaml
```
:::


It can be run with the following command:

```shell
toil-cwl-runner --retryCount 3 --cleanWorkDir never --outdir outputs example1.cwl --workDir . --band tmmx --date 2019-01-15 --geography zcta
```

If successful, you should find a gzipped CSV file 
`tmmx_zcta_polygon_2019.csv.gz` in the `outputs` directory, 
containing the following columns:    

* date
* zcta
* tmmx

This is exactly what we will ingest into the **Bronze layer**.

If the workflow fails, follow the troubleshooting steps described in 
the 
[Troubleshooting](../../pipelines.md#troubleshooting-workflows-run-by-toil) 
documentation.
         
## Step 4. Add database integration (PostgreSQL)

### Start or check PostgreSQL

If you already have a PostgreSQL database running, you will need to
create a `database.ini` file as described in the 
[Documentation](../../DBConnections.md). 

Otherwise, you can start a PostgreSQL container using Docker:

```shell
git clone https://github.com/ForomePlatform/dorieh.git
cd dorieh/docker/pg-hll
docker compose up -d
```
   
In the latter case use the provided 
[`database.ini`](https://github.com/ForomePlatform/dorieh/blob/main/examples/with-postgres/database.ini) 
file.

### Add PostgreSQL integration to the workflow

Back in the tutorial directory you created in 
[Directory layout](#directory-layout) (e.g. `dorieh/tutorials/climate`), 
add two new workflow inputs to example1.cwl: 

```yaml
inputs:
  band:
    type: string
  date:
    type: string
  geography:
    type: string
  database:
    type: File
    default:
      class: File
      location: https://raw.githubusercontent.com/ForomePlatform/dorieh/main/examples/with-postgres/database.ini
  connection_name:
    type: string
    default: "localhost"
```

### Add the Database initialization step

Another required action is to ensure that the database contains the 
latest Dorieh code for PostgreSQL. This is done by adding `init_db` 
step:  

```yaml
initdb:
    run: https://raw.githubusercontent.com/ForomePlatform/dorieh/main/src/cwl/initcoredb.cwl
    in:
      database: database
      connection_name: connection_name
    out:
      - log
      - err
```

Optionally, though we recommend it, add the outputs of the 
`initdb` to the pipeline outputs:
            
```yaml
outputs:
  # ... existing outputs ...

  initdb_log:
    type: File
    outputSource: initdb/log
  initdb_err:
    type: File
    outputSource: initdb/err
```
          
### Defining Data Model

However, to load the data into a database, we also need to define 
the database schema. It is possible to automatically infer schema 
using Dorieh tools like 
[Project Loader](../../ProjectLoader.md) and 
[Introspector](../../members/introspector). But for a Medallion 
architecture the schema should be explicitly defined; we will define it 
in a data model file and use it with the 
[Data Loader](../../DataLoader.md) tool.

```{seealso}
[Data modeling vs data introspection](../../adding_data.md#data-modeling-vs-data-introspection)
```

The data model definition language is described in the 
[Data Model](../../Datamodels.md) documentation. 

Initially, we 
will define a simple schema for the Bronze layer:

:::{toggle} Expand Code Block
```{literalinclude} steps/step4/example1_model.yml
:linenos:
:language: yaml
```
:::


It defines a data domain named “tutorial” and in it a table named 
“bronze_temperature” with 3 columns: `tmmx`, `date` and `zcta`. We will 
assume that the file name is `example1_model.yml`.

### Adding Ingestion Step
                                
Now we can add the actual ingestion step to the workflow using the 
Dorieh [ingest tool](../../pipeline/ingest.md):

```yaml
  ingest:
    run: https://raw.githubusercontent.com/ForomePlatform/dorieh/main/src/cwl/ingest.cwl
    in:
      depends_on: initdb/log
      registry:
        default:
          class: File
          location: "https://raw.githubusercontent.com/ForomePlatform/dorieh/main/doc/tutorial/climate/example1_model.yml"
      domain:
        valueFrom: "tutorial"
      table:
        valueFrom: "bronze_temperature"
      input: aggregate/data
      database: database
      connection_name: connection_name
    out:
      - log
      - errors
```

Note the `depends_on: initdb/log` line. CWL is a dataflow language: a
runner starts a step as soon as its inputs are available and may run
independent steps in parallel — there is no explicit "run after" clause.
Nothing else connects `ingest` to `initdb`, so without this line `ingest`
could start before `initdb` has finished preparing the database, and a
run against a fresh database could fail intermittently. To enforce
ordering, Dorieh database tools expose an optional `depends_on` input
that the tool itself ignores: wire it to a log output of the step that
must complete first. Use this pattern whenever two steps touch the same
database but do not exchange data.

After adding ingestion to **steps** and the logs it produces to the 
**outputs**, the resulting workflow file should look like:

:::{toggle} Expand Code Block
```{literalinclude} steps/step4/example1.cwl
:linenos:
:language: yaml
```
:::

                        
The same command as before can be used to run the workflow:

```shell
toil-cwl-runner --retryCount 3 --cleanWorkDir never --outdir outputs example1.cwl --workDir . --band tmmx --date 2019-01-15 --geography zcta
```

If you chose to perform this run, beside the CSV file, you will see the 
data in the database in the table `bronze_temperature`.
                                         
## Step 5. Building Medallion Layers (Bronze, Silver, Gold)

Medallion architecture defines three layers:

* **Bronze Layer**: Load as-is, minimally processed data to database 
  from pipeline outputs. 
  * In this climate data example, the “raw” data is not strictly 
    straight-from-source: as discussed under 
    [How this pipeline was designed](#how-this-pipeline-was-designed), 
    NetCDF rasters must be aggregated into a more conventional 
    tabular format before ingestion — the exact operation performed 
    by the aggregation step.      
* **Silver Layer**: Clean, harmonize, and enrich data.
  * Built from Bronze layer (no external inputs are allowed).
  * Add derived columns (e.g., Celsius/Fahrenheit conversions, state 
    & city annotation via ZIP lookup). 
  * Define as a view on top of the bronze table in your data model YAML.
* **Gold Layer**: Produce analytic/ML-ready outputs.
  * Built from Silver Layer.
  * Perform groupings and summaries (e.g., aggregating by state and 
    date). 
  * Use materialized views where performance and reusability are 
    required. 

Silver layer usually is responsible for normalization, harmonization 
and cleansing of the data. In our example the data does not require 
cleansing, as it is already clean, normalized, and does not require 
harmonization because it is coming from a single source. However, 
even if source data is already clean, enriching it with derived 
fields or external metadata (such as regional names) increases 
analytic utility and facilitates downstream ML feature engineering. 
Hence, we illustrate enriching the data by adding columns, 
displaying the temperature in different units and annotating zip 
codes with the US State abbreviations and the names of the cities 
for those areas that lie within a city.         

Based on the discussion above, for the silver layer we will add a 
corresponding step:   

```yaml
  build_silver:
    run: https://raw.githubusercontent.com/ForomePlatform/dorieh/main/src/cwl/create.cwl
    in:
      depends_on: ingest/log
      registry:
        default:
          class: File
          location: "https://raw.githubusercontent.com/ForomePlatform/dorieh/main/doc/tutorial/climate/example1_model.yml"
      domain:
        valueFrom: "tutorial"
      table:
        valueFrom: "silver_temperature"
      database: database
      connection_name: connection_name
    out:
      - log
      - errors
```

This step builds a view named `silver_temperature`. We also need to 
describe it in the data model file. Best Practice is to keep 
your Silver and Gold layer table/view definitions together in a 
versioned domain YAML file, checked into source control along with 
your workflow scripts.    

Hence, we will add the following definition to 
`example1_model.yml`: 

<!-- Kept in sync with doc/tutorial/climate/example1_model.yml — edit the model file first -->
```yaml
    silver_temperature:
      description: |
        Maximum daily temperature for US Zip Code Tabulation Areas, enriched and harmonized
      create:
        type: view
        from: bronze_temperature
      columns:
        - tmmx
        - date
        - zcta
        - temperature_in_C:
            type: float
            description: Temperature in Celsius
            source: (tmmx - 273.15)
        - temperature_in_F:
            type: float
            description: Temperature in Fahrenheit
            source: ((tmmx - 273.15)*9/5 + 32)
        - us_state:
            type: VARCHAR(2)
            description: US State
            source:  "public.zip_to_state(EXTRACT(YEAR FROM date)::INT, zcta)"
        - city:
            type: VARCHAR(128)
            description: >
              Name of a representative city for the ZIP Code Tabulation Area (ZCTA); 
              for ZCTAs spanning multiple cities, this is the city covering the largest 
              portion of the area or population.
            source:  "public.zip_to_city(EXTRACT(YEAR FROM date)::INT, zcta)"
```                

This silver view retains all 3 bronze columns and adds 4 new:

* Temperature expressed in degrees Celsius for the benefit of 
  readers outside of the United States. It is computed by the 
  trivial formula.   
* Temperature expressed in degrees Fahrenheit for the benefit of the 
  United States reader. It is computed by the known conversion 
  formula.  
* A code (2 letter abbreviation) for the state, in which the area 
  lies. It is computed by calling Dorieh built-in function 
  `zip_to_state`.  
* A name of the city for the zip code for urban areas, also computed 
  by calling Dorieh built-in function `zip_to_city`.  

After you made these changes to both files (`example1.cwl` and 
`example1_model.yml`), you are welcome to run the pipeline again, 
using the same command as above. It will now 
build the silver layer. 

Alternatively, we can add the Gold layer before testing.   

In the Gold layer, we will add just one table that computes some 
data for the whole states and is ready for analysis. The table 
named `gold_temperature_by_state` is defined by the following block:  

<!-- Kept in sync with doc/tutorial/climate/example1_model.yml — edit the model file first -->
```yaml
    gold_temperature_by_state:
      description: |
        Temperature variations by US State
      create:
        type: materialized view
        from: silver_temperature
        group by:
          - us_state
          - date
      columns:
        - us_state
        - date
        - t_span:
            type: float
            description: Temperature variation in Celsius
            source: MAX(tmmx) - MIN(tmmx)
        - t_mean_in_C:
            type: float
            description: Mean Temperature in Celsius
            source: AVG(temperature_in_C)
        - t_mean_in_F:
            type: float
            description: Mean Temperature in Fahrenheit
            source: AVG(temperature_in_F)
      primary_key:
        - us_state
        - date
```

The gold table contains mean temperatures on a date for every US state 
and also the variation in the temperature on the day. The variation 
is in maximum temperature, so it does not reflect a change during a 
day, but only the diversity of geography. Note that `t_span` is 
computed on the raw Kelvin values (`tmmx`); because a temperature 
*difference* is the same number of degrees in Kelvin and in Celsius, 
labeling the span in Celsius is correct.   

We now need to add a step to build a gold schema to the workflow 
itself. The step is literally the same as silver, the difference is 
just the target table name:  
                             
```yaml
  build_gold:
    run: https://raw.githubusercontent.com/ForomePlatform/dorieh/main/src/cwl/create.cwl
    in:
      depends_on: build_silver/log
      registry:
        default:
          class: File
          location: "https://raw.githubusercontent.com/ForomePlatform/dorieh/main/doc/tutorial/climate/example1_model.yml"
      domain:
        valueFrom: "tutorial"
      table:
        valueFrom: "gold_temperature_by_state"
      database: database
      connection_name: connection_name
    out:
      - log
      - errors
```

The final version of the workflow is:

:::{toggle} Expand Code Block
```{literalinclude} example1.cwl
:linenos:
:language: yaml
```
:::


While the final Medallion data model is:

:::{toggle} Expand Code Block
```{literalinclude} example1_model.yml
:linenos:
:language: yaml
```
:::

## Step 6. Testing the Pipeline

At this point example1.cwl orchestrates:

1. Data download.
2. Shape download.
3. Spatial aggregation.
4. DB initialization.
5. Bronze ingestion.
6. Silver view creation.
7. Gold materialized view creation.

The pipeline is now ready to be tested. You can run it with the 
same command as before:

```shell
toil-cwl-runner --retryCount 3 --cleanWorkDir never --outdir outputs example1.cwl --workDir . --band tmmx --date 2019-01-15 --geography zcta
```

If everything completes successfully, you should see the following 
tables in your PostgreSQL database:

* `bronze_temperature`
* `silver_temperature` (view)
* `gold_temperature_by_state` (materialized view)

You can also run the following SQL queries to verify the data:

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

-- Inspect Gold: which state was hottest on 2019‑01‑15?
SELECT us_state, t_mean_in_C, t_span
FROM gold_temperature_by_state
WHERE date = '2019-01-15'
ORDER BY t_mean_in_C DESC
LIMIT 10;
```

```{note}
**Scope and next steps.** This tutorial intentionally does not demonstrate
scatter/parallelization of workflow steps, nor validation journaling
(recording records that fail validation in an audit table instead of
silently dropping them). Both are demonstrated in the
[Medicare case study](../../Medicare.md).
```

## Next Steps

This completes Part 1. The remaining two parts of this tutorial cover:

* [Part 2. Documenting the workflow](documenting-a-workflow.md)
* [Part 3. Data dictionaries and lineage graphs](constructing-lineage.md)


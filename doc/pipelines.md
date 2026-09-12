# Data Processing Pipelines

This page explains how Dorieh pipelines are described in CWL, lists the
published, tested workflows, and shows how to run and troubleshoot them
with Toil.

```{contents}
---
local:
---
```

## Introduction

Most computational studies acquire and process data using a data
processing pipeline. Such pipelines are composed of multiple steps,
where each step may be a script, binary executable, or a specific data
transformation. These steps often depend on the completion and outcome
of previous steps, so the entire workflow can be naturally represented
as a **Directed Acyclic Graph (DAG)**: nodes represent workflow steps,
and
edges indicate their dependencies.

This DAG-based representation allows for complex pipeline topologies,
including parallelization and multiple dependencies. However, describing
such logic in procedural programming languages quickly becomes unwieldy
and hard to maintain. To address this challenge, **domain-specific
workflow description languages (DSLs)** have been developed.

## Workflow Description Languages

For reproducibility and repeatability, pipelines are commonly specified
using descriptive workflow DSLs. In bioinformatics and other scientific
domains, three such languages are widely used: CWL, WDL and Nextflow.
The most prevalent is the
[Common Workflow Language (CWL)](https://www.commonwl.org/),
due to its extensive community support,
number of published workflows, and broad platform compatibility. All
pipelines published in this documentation use CWL. CWL is the workflow
half of the two declarative languages described in
[The Dorieh approach](concepts.md#two-languages-one-pipeline): it
declares the pipeline topology, while the
[data-modeling DSL](Datamodels.md) declares what each step does to the
data.

Descriptive workflow languages separate the definition of pipeline
structure (topology, inputs, outputs, requirements) from the
implementation of processing steps. While these languages were pioneered
in bioinformatics—often operating on well-defined inputs and known
tools—they are also applicable to fields with more diverse and less
standardized data, such as population health research. In these domains,
many workflow steps may focus on complex data transformation and
harmonization.

> Some workflows require a database connection during execution;
> see [Managing database connections](DBConnections.md) for details.

## Running Workflows

### Tested Runners

CWL is a "write once, run anywhere" language. A pipeline developed and
tested in one environment (such as a laptop) will run on clusters and
cloud platforms using any compliant runner. For the latest list of
compatible runners, visit the
[CWL Implementations](https://www.commonwl.org/implementations/) page.

We have successfully used **cwltool**, **CWL-Airflow**, and **Toil**:

* **Toil**: Highly featured, supports AWS Batch and pipeline resumption
  after failures. Output can be quite verbose. We recommend it for
  production and development use.
* **CWL-Airflow**: Provides a graphical interface for managing and
  visualizing workflows.
* **cwltool**: Lightweight reference implementation, ideal for
  development for those who prefer to avoid Toil.

See the [Toil documentation](https://toil.readthedocs.io/en/latest/)
for additional details on using Toil for running CWL workflows.

### Providing Parameters to the Pipelines

Pipeline parameters are supplied on the command line
(as double-dash `--` options) or via YAML or JSON files.

When using YAML to specify files or directories as inputs,
use this structure:

```yaml
my_file:
  path: /path/to/data.nc
  class: File
my_directory:
  path: /path/to/data/downloads
  class: Directory

```

### Using Toil

For hands-on examples, refer to the
[Dorieh Examples Folder](https://github.com/ForomePlatform/dorieh/tree/main/examples)
on GitHub. There you will find:

* [Instructions for environment setup](https://github.com/ForomePlatform/dorieh/tree/main/examples#running-cwl-examples)
* [Running workflows that do not require a database backend](Example-climate-workflow.md)
* [Workflows with PostgreSQL backend](https://github.com/ForomePlatform/dorieh/tree/main/examples/with-postgres)

#### Quick Start with Toil

1. Install Toil with AWS and CWL support:

        pip install toil[aws,cwl]
2. Enable pipeline resumption:
   Use the `--jobStore` option when running the pipeline.
   To resume after a failure, use the same command plus `--restart`.

**Sample command**:

```shell
toil-cwl-runner --retryCount 1 --cleanWorkDir never \
  --outdir /scratch/work/exposures/outputs \
  --workDir /scratch/work/exposures \
  --jobStore /scratch/work/someDir123 \
  pm25_yearly_download.cwl test_exposure_job.yml
```

Most Dorieh workflows consist of multiple steps, each producing two log
files: a progress log (`*.log`) and an error log (`*.err`). On success,
error logs are usually empty; all logs are collected under the
`--outdir` directory.

A successful pipeline run typically emits a JSON object in standard
output or log file, for example:

```json
{
  "qc_ev_create_log": {
    "location": "file:///shared/dorieh-logs/data_loader-2025-03-05-09-48-27.log_2",
    "basename": "data_loader-2025-03-05-09-48-27.log",
    "nameroot": "data_loader-2025-03-05-09-48-27",
    "nameext": ".log",
    "class": "File",
    "checksum": "sha1$fa01481303c9030c8095387661a3bdc6851fc1ed",
    "size": 12060,
    "path": "/shared/dorieh-logs/data_loader-2025-03-05-09-48-27.log_2"
  },
  "registry": {
    "location": "file:///shared/dorieh-logs/data.yaml",
    "basename": "data.yaml",
    "nameroot": "data",
    "nameext": ".yaml",
    "class": "File",
    "checksum": "sha1$73700ade239b3a0c5f755ef694f05aebb4442c68",
    "size": 140457,
    "path": "/shared/dorieh-logs/ingestion/2015/outputs/cms.yaml"
  }
}
```

Alternatively, you can confirm successful completion by searching the
logs for either of: `Finished toil run successfully`  or
`CWL run complete!`:

```shell
grep 'Finished toil run successfully' 1_2015prod.log
grep 'CWL run complete!' 1_2015prod.log
```

A failed run usually ends with a `PermanentFail` message, although
abrupt
system failures may not log this. If a log file remains unmodified for
several hours, the workflow is likely not running.

> Some workflow steps, especially those involving database
> transformations, may run for extended periods but produce little log
> output. Check individual step logs for progress if you suspect issues.

### Troubleshooting Workflows Run by Toil

To check for errors across all runs:

```shell
find /shared/dorieh-logs/ -type f -name "*.err" -size +0c -exec ls -alF {} \;
```

> No output indicates no errors. Non-empty `.err` files should be
> examined.


For logs from a specific run (e.g., subdirectory per run):

```shell
find /shared/dorieh-logs/toilwf-c36b795b68935d99be01ed1556c85b1e/ -type f -name "*.err" -size +0c -exec ls -alF {} \;
```

To see all error logs regardless of whether they are empty or not omit
the `-size +0c` filter:

```shell
find /shared/dorieh-logs/toilwf-c36b795b68935d99be01ed1556c85b1e/ -type f -name "*.err" -exec ls -alF {} \;
```

## Testing Workflows

Pipelines can be tested with the included
[DBT pipeline testing framework](DBT.md); testing is described in
detail in [Testing bundled workflows](TestingWorkflows.md).

## Published and Tested Workflows

```{toctree}
---
maxdepth: 2

---
pipeline/gridmet
pipeline/wustl
pipeline/pm25_yearly_download
pipeline/aqs
pipeline/airnow
pipeline/medicare
pipeline/medicaid
pipeline/census_workflow
```

## Developing New Workflows

### Combining Included CWL Tools into a New Workflow

Dorieh provides multiple pre-packaged CWL tools, which you can mix and
match into custom workflows; the complete alphabetic index of every
tool and workflow shipped with the platform is in
[CWL Tools and Common Workflows](cwl_tools.md). Use
the [CWL output collection utility](members/cwl_collect_outputs) to help
generate CWL code snippets for new workflows.

### Ordering Database Steps with `depends_on`

CWL has no explicit "run after" clause: runners start every step whose
data inputs are available, possibly in parallel. Steps that share a
database must therefore be ordered explicitly through data dependencies.
Dorieh CWL tools that write to a database expose a `depends_on` input
for this purpose (declared as `Any?` or `File?`, depending on the tool):
wire it to a log output of the step that must finish first, for example
`depends_on: initdb/log`. In particular, every step that writes to the
database should depend, directly or transitively, on the database
initialization step (`initdb.cwl` or `initcoredb.cwl`); otherwise the
workflow may fail on its first run against a fresh database, or fail
intermittently when parallel branches race to create the same schema or
metadata tables. For a worked example of chaining steps this way, see
the [climate tutorial](tutorial/climate/building-climate-pipeline.md).

### Wrapping Python Modules as CWL Tools

Consider
using [cwl2argparse](https://github.com/hexylena/argparse2tool#cwl-specific-functionality)
or browse other [CWL development tools](https://www.commonwl.org/tools/)
for converting Python modules into CWL tools.





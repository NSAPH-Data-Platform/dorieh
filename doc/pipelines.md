# Data Processing Pipelines

```{contents}
---
local:
---
```

## Introduction

For the majority of computational studies, their data acquisition workflow can
be represented as a data processing pipeline. A data processing pipeline
consists of steps, each step being either a script, a binary executable, or a
specific data transformation within a data warehouse. Some steps are dependent
on the results of other steps. Therefore, every workflow can be represented as a
directed acyclic graph (DAG), where steps are the nodes of the graph and
dependencies are its edges. Pipeline topologies are complex as they provide for
massive parallelization and multiple dependencies. When pipeline logic is
expressed in a procedural programming language, the result is a very convoluted
program that is economically ineffective to maintain. Fortunately, alternatives
to procedural languages have been proposed and are widely used.

To the full extent both repeatability and reproducibility of data processing
pipelines is addressed by special descriptive domain specific languages (DSL).
Three such languages have been developed by different communities that work
primarily in bioinformatics. The most widely adopted is 
[Common Workflow Language (CWL)](https://www.commonwl.org/), 
the most popular in terms of studies that use it, the number of
published workflows and the number of runtime platforms supporting execution of
the workflows defined in CWL. The pipelines we publish here are all written
in CWL.

Descriptive workflow languages focus on explicit definition of the pipeline
topology and insulation of the topology, inputs, requirements and outputs from
the actual processing algorithms. Developed primarily by bioinformatics
communities and mostly used by bioinformatics projects they expect the inputs to
be in a few well-defined formats and orchestrate the work of a limited set of
known tools. In other areas, for example, in population health research, the
data comes from much more diverse sources, in diverse and often incompatible
formats. Therefore, many steps (nodes in the pipeline topology) will be
responsible for various data transformation operations. 
                                                           
> Some workflows require database connection to perform all steps.
> See [](DBConnections) section. for details

## Running Workflows
                   
### Tested runners

CWL is "write once run anywhere" language. If a piepline one has developed
runs on the developer's laptop it is more or less guaranteed it will run
in any on-prem cluster or cloud environment, provided a runner supporting
a given environment is used. One can find the list of currently 
supported runners in 
[CWL Implementations](https://www.commonwl.org/implementations/) page.

We have used cwltool, CWL-Airflow and Toil in our development
and production. Toil's output is a little too verbose, but it has
great features like ability to restart a pipeline from a failed
step (even after minor corrections) and native support for AWS Batch.
CWL-Airflow provides a nice graphical user interface.

See [Toil documentation](https://toil.readthedocs.io/en/latest/) 
for some details of running CWL workflows.
                                               
### Providing parameters to the pipelines

Parameters can be provided either as command line options
with two dashes `--` or in YaML or JSON file.

Note, that when using a YaML file, files and directories 
have to be specified in the following way:

```yaml
my_file:
  path: /path/to/data.nc
  class: File
my_directory:
  path: /path/to/data/downloads
  class: Directory

```

### Using Toil

A few hints if you are using Toil:

1. Install Toil with aws and cwl options:

        pip install toil[aws,cwl]
2. If you want to be able to restart a pipeline from a failed step you need to 
    provide `--jobStore` option. To restart - give exactly the same options
    adding `--restart` 

Here is an example of a command to execute a pipeline:

```shell
toil-cwl-runner --retryCount 1 --cleanWorkDir never \ 
  --outdir /scratch/work/exposures/outputs \ 
  --workDir /scratch/work/exposures \
  --jobStore /scratch/work/someDir123
  pm25_yearly_download.cwl test_exposure_job.yml 
```
                                                                                
## Testing workflows

Pipelines can be tested using included 
[DBT Pipeline Testing Framework](DBT)

More detailed document that describes testing is: [](TestingWorkflows).

## Installing Python dependencies
                                 
The following requirements.txt file can be used to fetch all 
Python packages included in the platform. 




## Published and tested workflows

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

## Developing your own workflows

### Combining included CWL tools into a new workflow

Dorieh includes many packaged CWL tools that can be combined in custom workflows. 
It also includes a [utility](members/cwl_collect_outputs) 
to generate CWL code that can be copied abd pasted into a parent
workflow.

### Wrapping python modules as CWL tools

You might want to look at [cwl2argparse](https://github.com/hexylena/argparse2tool#cwl-specific-functionality)
or other [CWL development tools](https://www.commonwl.org/tools/)

## Example of a workflow

Please see [](Example-climate-workflow)


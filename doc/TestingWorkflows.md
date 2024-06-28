# Testing bundled workflows

```{contents}
---
local:
---
```

```{seealso}
[Database Testing Framework](DBT)
```
  

## Introduction to testing and prerequisites

Bundled workflows can be tested in two ways:

1. With a local installation of dorieh package
2. Using Docker image

Regardless of the option you need to install a CWL implementation. We suggest that You create a 
Python virtual environment for trying this workflow, or use an existing one.
If you are creating a new virtual environment, run the following command:

    python3 -m venv $path
    source $path/bin/activate

where $path is a path to a directory, that will be created and where the new visualiser environment will
reside.

To run the workflow you need to install a [CWL implementation](https://www.commonwl.org/implementations/).
We suggest using [Toil](https://toil.ucsc-cgl.org/). To install Toil just run the following command
in your Python Virtual Environment:

    pip install "toil[cwl,aws]"

If you would like to test workflows with a local installation of Dorieh, execute 
this additional command:

    pip install dorieh

## Testing AQS workflow

### Before running the test
                          
Tests write significant amount of logs, therefore we recommend running them in a temporary scratch directory.

First, create a scratch directory:

    mkdir -p scratch/aqs
    cd scratch/aqs
                                                               
You will also need to create a database connection file, see 
[](DBConnections) for details and examples.

Further we assume the following environment variables:

```shell
export dbini=${/path/to/database.ini}
export connection=${section_name_in_database.ini}
```
                               
We also assume that you are using Toil as CWL implementation. If you use a different implementation,
you will need to replace `toil-cwl-runner` command with an appropriate alternative

###  Testing local installation

If you have installed dorieh locally, run the following command

    toil-cwl-runner --retryCount 0 --cleanWorkDir never --outdir outputs --workDir . \
        https://raw.githubusercontent.com/ForomePlatform/dorieh/main/src/cwl/test_aqs.cwl \
        --database ${dbini} --connection_name ${connection} \
        --test_script https://raw.githubusercontent.com/ForomePlatform/dorieh/main/src/cwl/test_cases/aqs_test.sql \
        --aggregation annual --parameter_code PM25 --table pm25_annual --years 2011 --years 2010    


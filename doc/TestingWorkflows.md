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

## Before running any test

Tests write significant amount of logs, therefore we recommend running them in a temporary scratch directory.

First, create a scratch directory:

    mkdir -p scratch/testxx
    cd scratch/testxx

You will also need to create a database connection file, see
[](DBConnections) for details and examples.

Further we assume the following environment variables:

```shell
export dbini=${/path/to/database.ini}
export connection=${section_name_in_database.ini}
```

We also assume that you are using Toil as CWL implementation. If you use a different implementation,
you will need to replace `toil-cwl-runner` command with an appropriate alternative


## Testing AQS workflow

### Before running the test

Create a scratch directory:

    mkdir -p scratch/aqs
    cd scratch/aqs
 
Export environment variables:

```shell
export dbini=${/path/to/database.ini}
export connection=${section_name_in_database.ini}
```

###  Testing local installation

If you have installed dorieh locally, run the following command

    toil-cwl-runner --retryCount 0 --cleanWorkDir never --outdir outputs --workDir . \
        https://raw.githubusercontent.com/ForomePlatform/dorieh/main/src/cwl/test_aqs.cwl \
        --database ${dbini} --connection_name ${connection} \
        --test_script https://raw.githubusercontent.com/ForomePlatform/dorieh/main/src/cwl/test_cases/aqs_test.sql \
        --aggregation annual --parameter_code PM25 --table pm25_annual --years 2011 --years 2010    


### Testing with DockerRequirement
                                                                                  
We will use workflows from src/workflows instead of src/cwl directory.

When testing with Docker, you should remember that commands are executed within 
a docker container, so `localhost` refers to a local docker container, not to your
local host. If your PostgreSQL is running locally, you need to update your database.ini file.

You might need to replace host with `host.docker.internal` or `172.17.0.1`.

In the virtual environment that has Toil run the following command:

    toil-cwl-runner --retryCount 0 --cleanWorkDir never --outdir outputs --workDir . \
        https://raw.githubusercontent.com/ForomePlatform/dorieh/main/src/workflows/test_aqs.cwl \
        --database ${dbini} --connection_name ${connection} \
        --test_script https://raw.githubusercontent.com/ForomePlatform/dorieh/main/src/cwl/test_cases/aqs_test.sql \
        --aggregation annual --parameter_code PM25 --table pm25_annual --years 2011 --years 2010    


## Testing Airnow workflow

### Before running the test

Create a scratch directory:

    mkdir -p scratch/airnow
    cd scratch/airnow

Export environment variables:

```shell
export dbini=${/path/to/database.ini}
export connection=${section_name_in_database.ini}
```

###  Testing local installation

If you have installed dorieh locally, run the following command

    toil-cwl-runner --retryCount 0 --cleanWorkDir never --outdir outputs --workDir . \
        https://raw.githubusercontent.com/ForomePlatform/dorieh/main/src/cwl/test_airnow.cwl \
        --database ${dbini} --connection_name ${connection} \
        --test_script https://raw.githubusercontent.com/ForomePlatform/dorieh/main/src/cwl/test_cases/airnow_test.sql \
        --parameter_code PM25 --table airnow_pm25_2022 --year 2022  \
        --api-key 9B053C38-3C42-416E-A330-203A698CCCDA --from 2022-01-01 --to 2022-08-31

## Testing Climate workflow
                                    
See also [](Example-climate-workflow)

### Before running the test

Create a scratch directory:

    mkdir -p scratch/climate
    cd scratch/climate

Export environment variables:

```shell
export dbini=${/path/to/database.ini}
export connection=${section_name_in_database.ini}
```

###  Testing local installation
                                  
There are frequent failure in downloading both datafiles and shapefiles, therefore, here we use option `--retryCount 3`
to automatically retry failed downloads.

If you have installed dorieh locally, run the following command

    toil-cwl-runner --retryCount 3 --cleanWorkDir never --outdir outputs --workDir . \
        https://raw.githubusercontent.com/ForomePlatform/dorieh/main/src/cwl/test_gridmet.cwl \
        --database ${dbini} --connection_name ${connection} \
        --test_script https://raw.githubusercontent.com/ForomePlatform/dorieh/main/src/cwl/test_cases/county_rmax.sql \
        --test_script https://raw.githubusercontent.com/ForomePlatform/dorieh/main/src/cwl/test_cases/county_rmin.sql \
        --dates dayOfMonth:13 --bands rmax --bands rmin --geography county
        


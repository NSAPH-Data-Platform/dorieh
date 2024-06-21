# Dorieh Data Platform for population and environmental health

Detailed documentation: [Dorieh Documentation](https://foromeplatform.github.io/dorieh/)

## Dorieh overview


Dorieh Data Platform is intended for development and deployment of
ETL/ELT pipelines that includes complex data processing and data
cleansing workflows. Complex workflows require a workflow language,
and we have chosen
[Common Workflow Language (CWL)](https://www.commonwl.org/).

We have tested deployment with the following CWL [implementations](https://www.commonwl.org/implementations/): 
                                                                 
* [Toil](https://toil.readthedocs.io/en/latest/running/cwl.html).
* [CWL reference implementation](https://github.com/common-workflow-language/cwltool), 
    primarily using [cwlref-runner ](https://pypi.org/project/cwlref-runner/) package
* [CWL-Airflow](https://cwl-airflow.readthedocs.io/en/latest/) that provides a very nice 
    Airflow graphical user interface (GUI) for running workflows.

The data produced by the data processing workflows is eventually stored in 
either CSV files, a PostgreSQL DBMS or Parquet files. Dorieh also supports storing
results in [FST](https://www.fstpackage.org/) and [HDF5](https://www.hdfgroup.org/) files. 

Some of the included data processing workflows use “Extract, Load, Transform,” (ELT) paradigm 
rather than more traditional “Extract, Transform, Load” ETL. It means that these workflows 
perform calculations, translations, filtering, cleansing, de-duplicating, validating, and 
data analysis or summarizations inside a DBMS using DBMS internal tools.

The data platform supports tools written in widely used languages such as
Python, C/C++ and Java, R and PL/pgSQL.
            

## Setting up

### Python Virtual Environment

Install Toil:

    pip install "toil[cwl,aws]"

Install Dorieh (stable version):

    pip install dorieh

If you prefer to install the latest version from GitHub: 

    pip install git+https://github.com/NSAPH-Data-Platform/dorieh

If FST support is desired, [R](https://www.r-project.org/) runtime has to be installed and R_HOME environment 
variable set up. One of the simples ways of installing R is to use 
[Conda package manager](https://docs.conda.io/projects/conda/en/stable/). Once R is set up, install
Dorieh with either of the  following command:

    pip install dorieh[FST]

    pip install "git+https://github.com/NSAPH-Data-Platform/dorieh[FST]"

### Docker Container

To build your own Dorieh Docker image see [docker directory](docker/README.md)

A prebuilt docker image with Dorieh is provided:

    docker pull forome/dorieh


## Built-in Workflows

For examples of data processing workflows, see [included data processing workflows](doc/pipelines.md)


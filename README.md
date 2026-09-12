# Dorieh Data Platform for population and environmental health

[![PyPI](https://img.shields.io/pypi/v/dorieh.svg)](https://pypi.org/project/dorieh/)
[![DOI](https://zenodo.org/badge/816452278.svg)](https://zenodo.org/badge/latestdoi/816452278)
                                                          
Read the [book about Dorieh](https://tidd.ly/4y1ClDH), published by Springer.

<a href="https://tidd.ly/4y1ClDH"><img src="https://raw.githubusercontent.com/ForomePlatform/dorieh/main/doc/img/awin_qrcode.png" alt="QR code linking to the book about Dorieh" width="120"></a>

Detailed documentation: [Dorieh Documentation](https://foromeplatform.github.io/dorieh/)

## Cite as

If you use Dorieh in academic work, please cite the book:

> Bouzinier, M., Etin, D., Khoshnevis, N., Shad, M., Yockel, S. (2026).
> *Research Data that Can be Trusted.* SpringerBriefs in Computer Science.
> Springer. <https://doi.org/10.1007/978-3-032-21032-6>

To reference the software itself, use the Zenodo concept DOI
[10.5281/zenodo.22728722](https://doi.org/10.5281/zenodo.22728722)
(always resolves to the latest release). See
[Citing Dorieh](https://foromeplatform.github.io/dorieh/citing.html)
for chapter DOIs, version DOIs, and BibTeX.

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

    pip install git+https://github.com/ForomePlatform/dorieh

If FST support is desired, [R](https://www.r-project.org/) runtime has to be installed and R_HOME environment 
variable set up. One of the simples ways of installing R is to use 
[Conda package manager](https://docs.conda.io/projects/conda/en/stable/). Once R is set up, install
Dorieh with either of the  following command:

    pip install dorieh[FST]

    pip install "git+https://github.com/ForomePlatform/dorieh[FST]"

### Docker Container

To build your own Dorieh Docker image see [docker directory](docker/README.md)

A prebuilt docker image with Dorieh is provided:

    docker pull forome/dorieh


## Built-in Workflows

For examples of data processing workflows, see [included data processing workflows](doc/pipelines.md)


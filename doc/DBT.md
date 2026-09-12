# Database Testing Framework

```{toctree}
---
maxdepth: 4
glob: true
hidden: 
---
members/create_test
members/dbt_runner
members/gen_dbt_cwl
TestingWorkflows.md
```

See also [Data Platform Internals](guts.md).

The testing framework allows to test a pipeline produces
exactly the same data in subsequent pipeline runs. The data is
tested in database table(s) procedure by the pipeline.


The framework consists of three utilities:

* [create_test.py](members/create_test): A tool to generate a set of SQL queries
    testing that the data has not changed
* [dbt_runner.py](members/dbt_runner): A tool to run the test cases generated
    by `create_test.py`
* [gen_dbt_cwl.py](members/gen_dbt_cwl): A tool to generate a CWL workflow
    that tests a given pipeline (also CWL workflow)
                                                             
For instructions to test bundled workflows 
see [](TestingWorkflows.md)

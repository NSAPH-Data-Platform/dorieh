Utility to generate test queries
================================

```{toctree}
---
maxdepth: 4
glob: true
hidden: 
---
dbt_runner.md
getn_dbt_cwl.rst
../DBT.md
```

```{contents}
---
local:
---
```


Usage
-----

      python -m dorieh.platform.dbt.create_test --script SCRIPT [SCRIPT ...]
            [--table TABLE]
            [--db DB]
            [--connection CONNECTION]
            [--autocommit]
            [-h]
            [--verbose]

Options:
                                                                                                          
| Option                        | Alias                          | Description                                                                                    |
|-------------------------------|--------------------------------|------------------------------------------------------------------------------------------------|
| `--help`                      | `-h`                           | Show this help message and exit                                                                |
| `--script SCRIPT [SCRIPT...]` | `-s SCRIPT [SCRIPT...]`        | Path to the file to write the test scripts                                                     |
| `--autocommit`                |                                | Use autocommit, default: False                                                                 |
| `--database DB`               | `--db DB`                      | Path to a database connection parameters file, default: database.ini (in the working directory |
| `--connection CONNECTION`     | `--connection_name CONNECTION` | Section in the database connection parameters file                                             |
| `--table TABLE`               | `-t TABLE`                     | Name of the table to being tested, default: None                                               |
| `--verbose`                   |                                | Verbose output, default: False                                                                 |



Details
-------
 
```{automodule}  dorieh.platform.dbt.create_test
:members:
:undoc-members:
```


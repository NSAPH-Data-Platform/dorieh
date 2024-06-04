Utility to generate test queries
================================

Usage
-----

    python -m dorieh.platform.dbt.dbt_runner [-h] --script SCRIPT [SCRIPT ...]
        [--autocommit] [--db DB] [--connection CONNECTION]
        [--verbose] [--table TABLE]

Options:


| Option                        | Alias                          | Description                                                                                     |
|-------------------------------|--------------------------------|-------------------------------------------------------------------------------------------------|
| `--help`                      | `-h`                           | Show this help message and exit                                                                 |
| `--script SCRIPT [SCRIPT...]` | `-s SCRIPT [SCRIPT...]`        | Path to the file(s) containing test scripts to execute                                          |
| `--autocommit`                |                                | Use autocommit, default: False                                                                  |
| `--database DB`               | `--db DB`                      | Path to a database connection parameters file, default: database.ini (in the working directory) |
| `--connection CONNECTION`     | `--connection_name CONNECTION` | Section in the database connection parameters file                                              |
| `--table TABLE`               | `-t TABLE`                     | Name of the table to test, default: None                                                        |
| `--verbose`                   |                                | Verbose output, default: False                                                                  |


 


Details
-------


```{automodule}  dorieh.platform.dbt.dbt_runner
:members:
:undoc-members:
```




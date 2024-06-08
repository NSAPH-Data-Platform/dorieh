# Monitoring database activity

```{contents}
---
local:
---
```


## Module monitor

Dorieh includes support for monitoring database activity, implemented
by the Python module [monitor](members/monitor).

The module can be used 3 ways:

1. As a command line utility to list all processes,currently running in the database
2. As a command line utility to display details about a specific process running in the database
3. As a Python API to execute a long-running process in the database with periodically displaying 
    the process status

## CLI Usage for monitor

    python -m  dorieh.platform.loader.monitor 
       [-h] [--pid PID [PID ...]] [--state STATE] [--autocommit] [--db DB]
       [--connection CONNECTION] [--verbose] [--dryrun]

Options:

      -h, --help            show this help message and exit
      --pid PID [PID ...], -p PID [PID ...]
                            Display monitoring information only for selected
                            process ids, default: None
      --state STATE         Show only processes in the given state, default: None
      --autocommit          Use autocommit, default: False
      --db DB, --database DB
                            Path to a database connection parameters file,
                            default: database.ini
      --connection CONNECTION, --connection_name CONNECTION
                            Section in the database connection parameters file,
                            default: nsaph2
      --verbose             Verbose output, default: False
      --dryrun              Dry run: do not perform any modifications of the
                            database, default: False

CLI uses a standard Dorieh way to retrieve database connection credentials
[see [](DBConnections)].

## Using as API

See [](monitor-example_src).

In this example we monitor execute a sample process inside PostgreSQL database using
a built-in progress logging function. Users can also specify provide their own callbacks.

A custom callback can query `DBActivityMonitor` instance (`monitor` in the example) using
the following code:

```python
    activity = monitor.get_activity(pid)
    for msg in activity:
        pass
        ## do whatever with the given message


```


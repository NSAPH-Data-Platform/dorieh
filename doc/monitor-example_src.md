# Example of using the database mounting tool

```{literalinclude} ../examples/longprocess.py
:linenos:
:language: python
```
                 
## Usage

    python longprocess.py --db DB --connection CONNECTION

Where:

      --db DB, --database DB
                            Path to a database connection parameters file,
                            default: database.ini
      --connection CONNECTION, --connection_name CONNECTION
                            Section in the database connection parameters file,
                            default: nsaph2

[see [](DBConnections)] for details on how to manage and specify connections to PostgreSQL database.



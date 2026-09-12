# Column silver_temperature.temperature_in_F

## Overview of column temperature_in_F in table silver_temperature 

|                               |                        |
| ----------------------------- | ---------------------- |
| Table                         | [silver_temperature](../silver_temperature.md)           |
| Qualified name                | silver_temperature.temperature_in_F  |
| Datatype                      | float        |
| Column type | computed |


Temperature in Fahrenheit




## Expressions

```sql
SELECT ((tmmx - 273.15)*9/5 + 32)
```



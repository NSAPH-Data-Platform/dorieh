# Column silver_temperature.us_state

## Overview of column us_state in table silver_temperature 

|                               |                        |
| ----------------------------- | ---------------------- |
| Table                         | [silver_temperature](../silver_temperature.md)           |
| Qualified name                | silver_temperature.us_state  |
| Datatype                      | VARCHAR(2)        |
| Column type | computed |


US State




## Expressions

```sql
SELECT public.zip_to_state(EXTRACT(YEAR FROM date)::INT, zcta)
```


```{toctree}
---
maxdepth: 1
hidden:
---
us_state_svg_envelop.md
```


```{figure} us_state.svg
:align: center
:alt: Column silver_temperature.us_state Lineage SVG
:target: us_state_svg_envelop.html

Data lineage for column silver_temperature.us_state

```



# Column gold_temperature_by_state.t_span

## Overview of column t_span in table gold_temperature_by_state 

|                               |                        |
| ----------------------------- | ---------------------- |
| Table                         | [gold_temperature_by_state](../gold_temperature_by_state.md)           |
| Qualified name                | gold_temperature_by_state.t_span  |
| Datatype                      | float        |
| Column type | computed |


Temperature variation in Celsius




## Expressions

```sql
SELECT MAX(tmmx) - MIN(tmmx)
```


```{toctree}
---
maxdepth: 1
hidden:
---
t_span_svg_envelop.md
```


```{figure} t_span.svg
:align: center
:alt: Column gold_temperature_by_state.t_span Lineage SVG
:target: t_span_svg_envelop.html

Data lineage for column gold_temperature_by_state.t_span

```



# Column silver_temperature.city

## Overview of column city in table silver_temperature 

|                               |                        |
| ----------------------------- | ---------------------- |
| Table                         | [silver_temperature](../silver_temperature.md)           |
| Qualified name                | silver_temperature.city  |
| Datatype                      | VARCHAR(128)        |
| Column type | computed |


Name of a representative city for the ZIP Code Tabulation Area (ZCTA);  for ZCTAs spanning multiple cities, this is the city covering the largest  portion of the area or population.





## Expressions

```sql
SELECT public.zip_to_city(EXTRACT(YEAR FROM date)::INT, zcta)
```


```{toctree}
---
maxdepth: 1
hidden:
---
city_svg_envelop.md
```


```{figure} city.svg
:align: center
:alt: Column silver_temperature.city Lineage SVG
:target: city_svg_envelop.html

Data lineage for column silver_temperature.city

```



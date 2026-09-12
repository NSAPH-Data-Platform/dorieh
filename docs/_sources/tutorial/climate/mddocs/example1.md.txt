---
orphan: true
---

# example1.cwl


 [Source code](example1cwl_src.md) 


![](example1.png)

```{contents}
---
local:
---
```

**Workflow**

## Inputs

| Name            | Type   | Default                                                                                                                                        | Description | 
|:----------------|:-------|:-----------------------------------------------------------------------------------------------------------------------------------------------|:------------|
| band            | string |                                                                                                                                                |             | 
| date            | string |                                                                                                                                                |             | 
| geography       | string |                                                                                                                                                |             | 
| database        | File   | `{'class': 'File', 'location': 'https://raw.githubusercontent.com/ForomePlatform/dorieh/refs/heads/main/examples/with-postgres/database.ini'}` |             | 
| connection_name | string | `localhost`                                                                                                                                    |             | 

## Outputs

| Name                   | Type   | Description | 
|:-----------------------|:-------|:------------|
| download_log           | File   |             | 
| download_data          | File   |             | 
| download_errors        | File   |             | 
| get_shapes_shape_files | File[] |             | 
| aggregate_log          | File   |             | 
| aggregate_data         | File   |             | 
| aggregate_errors       | File   |             | 
| initdb_log             | File   |             | 
| initdb_err             | File   |             | 
| ingest_log             | File   |             | 
| ingest_err             | File   |             | 
| build_silver_log       | File   |             | 
| build_silver_err       | File   |             | 
| build_gold_log         | File   |             | 
| build_gold_err         | File   |             | 

## Steps

| Name         | Runs                                                                                         | Description | 
|:-------------|:---------------------------------------------------------------------------------------------|:------------|
| extract_year | [parse_date.cwl](https://foromeplatform.github.io/dorieh/pipeline/parse_date.html)           |             | 
| download     | [download.cwl](https://foromeplatform.github.io/dorieh/pipeline/download.html)               |             | 
| get_shapes   | [get_shapes.cwl](https://foromeplatform.github.io/dorieh/pipeline/get_shapes.html)           |             | 
| aggregate    | [aggregate_daily.cwl](https://foromeplatform.github.io/dorieh/pipeline/aggregate_daily.html) |             | 
| initdb       | [initcoredb.cwl](https://foromeplatform.github.io/dorieh/pipeline/initcoredb.html)           |             | 
| ingest       | [ingest.cwl](https://foromeplatform.github.io/dorieh/pipeline/ingest.html)                   |             | 
| build_silver | [create.cwl](https://foromeplatform.github.io/dorieh/pipeline/create.html)                   |             | 
| build_gold   | [create.cwl](https://foromeplatform.github.io/dorieh/pipeline/create.html)                   |             | 
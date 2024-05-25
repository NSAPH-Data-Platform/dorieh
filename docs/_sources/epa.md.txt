# Dorieh EPA Package Description

[Documentation Home](home)

Toolkit for downloading and preprocessing of data provided by EPA

Handles the following types of data: 

* EPA AQS Data hosted at https://www.epa.gov/aqs and EPA AirNow data 
  from https://docs.airnowapi.org/webservices
    * [Pipeline](pipeline/aqs)
* AirNow contains real-time up-to-date pollution data but is less reliable
  than AQS
    * [Pipeline](pipeline/airnow)

## Package Contents

```{toctree}
epa_usage
epa_python_modules
epa_cwl_tools
```

## Querying Data

### AirNow

> Note: Negative values indicate missing data, therefore
> we need to specify a condition (value > 0)

#### Columns

COLUMN_NAME | TYPE_NAME | IS_NULLABLE | IS_AUTOINCREMENT | IS_GENERATEDCOLUMN | 
------------|-----------| ------------|----------------|------------------| 
fullaqscode | text | YES | NO | NO
latitude | numeric | YES | NO | NO
longitude | numeric | YES | NO | NO
utc | timestamp | YES | NO | NO
parameter | varchar | YES | NO | NO
unit | varchar | YES | NO | NO
value | numeric | YES | NO | NO
aqi | numeric | YES | NO | NO
category | int4 | YES | NO | NO
sitename | varchar | YES | NO | NO
agencyname | varchar | YES | NO | NO
intlaqscode | text | YES | NO | NO
zcta | int4 | YES | NO | NO
state | int4 | YES | NO | NO
fips5 | int4 | YES | NO | NO
statefp | int4 | YES | NO | NO
countyfp | int4 | YES | NO | NO
county | int4 | YES | NO | NO
stusps | varchar | YES | NO | NO
record | varchar | NO | NO | NO
monitor | varchar | YES | NO | NO

#### Sample AirNow query by date

```sql
SELECT 
    utc::date,
    AVG(value) AS mean_value,
    MIN(value) AS minimum,
    MAX(value) AS maximum,
    COUNT(*)
FROM 
    epa.airnow_pm25_2022
WHERE value > 0    
GROUP BY 1
ORDER BY 1
```

#### Sample AirNow query, aggregating monthly

```sql
SELECT 
    EXTRACT(MONTH FROM utc),
    AVG(value) AS mean_value,
    MIN(value) AS minimum,
    MAX(value) AS maximum,
    COUNT(*)
FROM 
    epa.airnow_pm25_2022
WHERE value > 0    
GROUP BY 1
ORDER BY 1
```

#### Sample AirNow query, aggregating by State

```sql
SELECT 
    stusps,
    AVG(value) AS mean_value,
    MIN(value) AS minimum,
    MAX(value) AS maximum,
    COUNT(*)
FROM 
    epa.airnow_pm25_2022
WHERE value > 0    
GROUP BY 1
ORDER BY 2 desc

```

### AQS
                     
See [AQS Data Dictionary](https://aqs.epa.gov/aqsweb/documents/AQS_Data_Dictionary.html)
for the description of the columns

#### Annual Columns

COLUMN_NAME | TYPE_NAME | IS_NULLABLE | IS_AUTOINCREMENT | IS_GENERATEDCOLUMN |
------------|-----------|-------------|------------------|------------------- |
state_code | varchar | YES | NO | NO
county_code | varchar | YES | NO | NO
site_num | varchar | YES | NO | NO
parameter_code | varchar | YES | NO | NO
poc | numeric | YES | NO | NO
latitude | numeric | YES | NO | NO
longitude | numeric | YES | NO | NO
datum | varchar | YES | NO | NO
parameter_name | varchar | YES | NO | NO
sample_duration | varchar | YES | NO | NO
pollutant_standard | varchar | YES | NO | NO
metric_used | varchar | YES | NO | NO
method_name | varchar | YES | NO | NO
year | numeric | YES | NO | NO
units_of_measure | varchar | YES | NO | NO
event_type | varchar | YES | NO | NO
observation_count | numeric | YES | NO | NO
observation_percent | numeric | YES | NO | NO
completeness_indicator | varchar | YES | NO | NO
valid_day_count | numeric | YES | NO | NO
required_day_count | numeric | YES | NO | NO
exceptional_data_count | numeric | YES | NO | NO
null_data_count | numeric | YES | NO | NO
primary_exceedance_count | varchar | YES | NO | NO
secondary_exceedance_count | varchar | YES | NO | NO
certification_indicator | varchar | YES | NO | NO
num_obs_below_mdl | numeric | YES | NO | NO
arithmetic_mean | numeric | YES | NO | NO
arithmetic_standard_dev | numeric | YES | NO | NO
c_1st_max_value | numeric | YES | NO | NO
c_1st_max_datetime | varchar | YES | NO | NO
c_2nd_max_value | varchar | YES | NO | NO
c_2nd_max_datetime | varchar | YES | NO | NO
c_3rd_max_value | varchar | YES | NO | NO
c_3rd_max_datetime | varchar | YES | NO | NO
c_4th_max_value | varchar | YES | NO | NO
c_4th_max_datetime | varchar | YES | NO | NO
c_1st_max_non_overlapping_value | varchar | YES | NO | NO
c_1st_no_max_datetime | varchar | YES | NO | NO
c_2nd_max_non_overlapping_value | varchar | YES | NO | NO
c_2nd_no_max_datetime | varchar | YES | NO | NO
c_99th_percentile | numeric | YES | NO | NO
c_98th_percentile | numeric | YES | NO | NO
c_95th_percentile | numeric | YES | NO | NO
c_90th_percentile | numeric | YES | NO | NO
c_75th_percentile | numeric | YES | NO | NO
c_50th_percentile | numeric | YES | NO | NO
c_10th_percentile | numeric | YES | NO | NO
local_site_name | varchar | YES | NO | NO
address | varchar | YES | NO | NO
state_name | varchar | YES | NO | NO
county_name | varchar | YES | NO | NO
city_name | varchar | YES | NO | NO
cbsa_name | varchar | YES | NO | NO
date_of_last_change | date | YES | NO | NO
monitor | varchar | YES | NO | NO
record | varchar | NO | NO | NO

#### Daily columns

COLUMN_NAME | TYPE_NAME | IS_NULLABLE | SCOPE_TABLE | IS_AUTOINCREMENT | IS_GENERATEDCOLUMN  |
------------|-----------|-------------|-------------|------------------|------------------- |
state_code | varchar | YES | (null) | NO | NO
county_code | varchar | YES | (null) | NO | NO
site_num | varchar | YES | (null) | NO | NO
parameter_code | varchar | YES | (null) | NO | NO
poc | numeric | YES | (null) | NO | NO
latitude | numeric | YES | (null) | NO | NO
longitude | numeric | YES | (null) | NO | NO
datum | varchar | YES | (null) | NO | NO
parameter_name | varchar | YES | (null) | NO | NO
sample_duration | varchar | YES | (null) | NO | NO
pollutant_standard | varchar | YES | (null) | NO | NO
date_local | date | YES | (null) | NO | NO
units_of_measure | varchar | YES | (null) | NO | NO
event_type | varchar | YES | (null) | NO | NO
observation_count | numeric | YES | (null) | NO | NO
observation_percent | numeric | YES | (null) | NO | NO
arithmetic_mean | numeric | YES | (null) | NO | NO
c_1st_max_value | numeric | YES | (null) | NO | NO
c_1st_max_hour | numeric | YES | (null) | NO | NO
aqi | numeric | YES | (null) | NO | NO
method_code | varchar | YES | (null) | NO | NO
method_name | varchar | YES | (null) | NO | NO
local_site_name | varchar | YES | (null) | NO | NO
address | varchar | YES | (null) | NO | NO
state_name | varchar | YES | (null) | NO | NO
county_name | varchar | YES | (null) | NO | NO
city_name | varchar | YES | (null) | NO | NO
cbsa_name | varchar | YES | (null) | NO | NO
date_of_last_change | date | YES | (null) | NO | NO
monitor | varchar | YES | (null) | NO | NO
record | varchar | NO | (null) | NO | NO
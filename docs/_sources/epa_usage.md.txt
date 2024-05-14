# EPA Toolkit Usage

```{contents}
---
local:
---
```

## AQS Usage   

```
    python -m dorieh.epa.aqs [-h] 
        [--years [YEARS ...]] 
        [--aggregation {annual,daily}] 
        --parameters PARAMETERS [PARAMETERS ...] 
        --destination DESTINATION 
        [--merge_years]
    
    optional arguments:
      -h, --help            show this help message and exit
      --years [YEARS ...], -y [YEARS ...]
                            Year or list of years to download. For example, the
                            following argument: `-y 1992:1995 1998 1999 2011
                            2015:2017` will produce the following list:
                            [1992,1993,1994,1995,1998,1999,2011,2015,2016,2017],
                            default: 1990:2020
      --aggregation {annual,daily}, -a {annual,daily}
                            Whether to use annual or daily aggregation, default:
                            annual
      --parameters PARAMETERS [PARAMETERS ...], -p PARAMETERS [PARAMETERS ...]
                            Parameter(s) to download, allowed mnemonic names:
                            NO2,OZONE,PM25,MAX_TEMP,MIN_TEMP or integer codes.
                            Example: `-p NO2 44201` will download Ozone and NO2.
                            Required for daily data, for annual data defaults to
                            all.
      --destination DESTINATION, --dest DESTINATION, -d DESTINATION
                            Destination directory for the downloaded files
      --merge_years         Concatenate consecutive years in one file, default:
                            False
```

## AirNow Usage

```
    python -m dorieh.epa.airnow  
       [-h] --parameters
       {no2,ozone,pm25,pm10,co,so2,NO2,OZONE,PM25,PM10,CO,SO2}
       [{no2,ozone,pm25,pm10,co,so2,NO2,OZONE,PM25,PM10,CO,SO2} ...]
       [--destination DESTINATION] --start_date START_DATE --end_date END_DATE
       [--reset] [--qc] [--cfg CFG] [--shapes SHAPES [SHAPES ...]]
       [--api_key API_KEY] [--years [YEARS [YEARS ...]]] [--compress]

    optional arguments:
      -h, --help            show this help message and exit
      --parameters {no2,ozone,pm25,pm10,co,so2,NO2,OZONE,PM25,PM10,CO,SO2} [{no2,ozone,pm25,pm10,co,so2,NO2,OZONE,PM25,PM10,CO,SO2} ...], -p {no2,ozone,pm25,pm10,co,so2,NO2,OZONE,PM25,PM10,CO,SO2} [{no2,ozone,pm25,pm10,co,so2,NO2,OZONE,PM25,PM10,CO,SO2} ...]
                            EPA AirNow Parameter Codes
      --destination DESTINATION, --dest DESTINATION, -d DESTINATION
                            Destination directory for the downloaded files,
                            default: None
      --start_date START_DATE, --start-date START_DATE, --from START_DATE
                            First date in the range to download (inclusive)
      --end_date END_DATE, --end-date END_DATE, --to END_DATE
                            Last date in the range to download (inclusive)
      --reset               Discard previously downloaded data if exists, default:
                            True
      --qc                  Perform basic data QC, default: True
      --cfg CFG             An optional path to config file, default: None
      --shapes SHAPES [SHAPES ...]
                            An optional path to shape files, default: None
      --api_key API_KEY     AirNow API Key, default: None
      --years [YEARS [YEARS ...]], -y [YEARS [YEARS ...]]
                            Year or list of years to download. For example, the
                            following argument: `-y 1992:1995 1998 1999 2011
                            2015:2017` will produce the following list:
                            [1992,1993,1994,1995,1998,1999,2011,2015,2016,2017] ,
                            default: 1990:2020
      --compress, -c        Use gzip compression for the result, default: True
```

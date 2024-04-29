--  Copyright (c) 2022. Harvard University
--
--  Developed by Research Software Engineering,
--  Faculty of Arts and Sciences, Research Computing (FAS RC)
--  Author: Michael A Bouzinier
--
--  Licensed under the Apache License, Version 2.0 (the "License");
--  you may not use this file except in compliance with the License.
--  You may obtain a copy of the License at
--
--         http://www.apache.org/licenses/LICENSE-2.0
--
--  Unless required by applicable law or agreed to in writing, software
--  distributed under the License is distributed on an "AS IS" BASIS,
--  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
--  See the License for the specific language governing permissions and
--  limitations under the License.
--

/*
 Purpose:
 Utilities and tools for gridMET data
 */

-- Creates materialized view organized in the same way
-- as Randall Martin's pollution data downloaded from WashU
-- Name: epa.pm25_monthly

DROP MATERIALIZED VIEW IF EXISTS epa.pm25_monthly CASCADE;
CREATE MATERIALIZED VIEW epa.pm25_monthly AS
SELECT
    EXTRACT (YEAR FROM date_local)::INT AS year,
    btrim(to_char(EXTRACT (MONTH FROM date_local)::INT, '00'))::VARCHAR AS month,
    state_code AS fips2,
    county_code AS fips3,
    public.fips2state(state_code) AS state,
    state_code||county_code AS fips5,
    MAX(state_name) AS state_name,
    MAX(county_name) AS county_name,
    AVG(arithmetic_mean) AS pm25,
    COUNT(*)
FROM
    epa.pm25_daily AS ep
GROUP BY 1,2,3,4
ORDER BY 1,2,3,4
;
CREATE INDEX pm25_monthly_ym ON epa.pm25_monthly (year, month);
CREATE INDEX pm25_monthly_m ON epa.pm25_monthly (month);
CREATE INDEX pm25_monthly_f2 ON epa.pm25_monthly (fips2);
CREATE INDEX pm25_monthly_s ON epa.pm25_monthly (state);
CREATE INDEX pm25_monthly_f3 ON epa.pm25_monthly (fips3);
CREATE INDEX pm25_monthly_f5 ON epa.pm25_monthly (fips5);

-- ================= END of   epa.pm25_monthly =================
-- Creates materialized view to compare PM25 data from
-- EPA and from WashU (Randall Martin's data)


DROP TABLE IF EXISTS exposures.pm25_monthly_county_epa CASCADE;
CREATE TABLE exposures.pm25_monthly_county_epa AS
SELECT
    EXTRACT (YEAR FROM date_local)::INT AS year,
    EXTRACT (MONTH FROM date_local)::INT AS month,
    state_code AS fips2,
    county_code AS fips3,
    public.fips2state(state_code) AS state,
    state_code||county_code AS fips5,
    MAX(state_name) AS state_name,
    MAX(county_name) AS county_name,
    AVG(arithmetic_mean) AS pm25,
    COUNT(*)
FROM
    epa.pm25_daily AS ep
GROUP BY 1,2,3,4
ORDER BY 1,2,3,4
;
CREATE INDEX epa_pm25_monthly_ym ON exposures.pm25_monthly_county_epa (year, month);
CREATE INDEX epa_pm25_monthly_m ON  exposures.pm25_monthly_county_epa (month);
CREATE INDEX epa_pm25_monthly_f2 ON exposures.pm25_monthly_county_epa (fips2);
CREATE INDEX epa_pm25_monthly_s ON  exposures.pm25_monthly_county_epa (state);
CREATE INDEX epa_pm25_monthly_f3 ON exposures.pm25_monthly_county_epa (fips3);
CREATE INDEX epa_pm25_monthly_f5 ON exposures.pm25_monthly_county_epa (fips5);

-- ===========================================

DROP TABLE IF EXISTS exposures.pm25_daily_county_epa CASCADE;
CREATE TABLE exposures.pm25_daily_county_epa AS
SELECT
    date_local,
    EXTRACT (YEAR FROM date_local)::INT AS year,
    EXTRACT (MONTH FROM date_local)::INT AS month,
    EXTRACT (DAY FROM date_local)::INT AS day,
    state_code AS fips2,
    county_code AS fips3,
    public.fips2state(state_code) AS state,
    state_code||county_code AS fips5,
    MAX(state_name) AS state_name,
    MAX(county_name) AS county_name,
    AVG(arithmetic_mean) AS pm25,
    COUNT(*)
FROM
    epa.pm25_daily AS ep
GROUP BY 1,5,6
ORDER BY 1,5,6
;
CREATE INDEX epa_pm25_daily_dt ON exposures.pm25_daily_county_epa (date_local);
CREATE INDEX epa_pm25_daily_ym ON exposures.pm25_daily_county_epa (year, month);
CREATE INDEX epa_pm25_daily_m ON  exposures.pm25_daily_county_epa (month);
CREATE INDEX epa_pm25_daily_f2 ON exposures.pm25_daily_county_epa (fips2);
CREATE INDEX epa_pm25_daily_s ON  exposures.pm25_daily_county_epa (state);
CREATE INDEX epa_pm25_daily_f3 ON exposures.pm25_daily_county_epa (fips3);
CREATE INDEX epa_pm25_daily_f5 ON exposures.pm25_daily_county_epa (fips5);

-- ===========================================


DROP MATERIALIZED VIEW IF EXISTS exposures.pm25_monthly_comparison;
CREATE MATERIALIZED VIEW exposures.pm25_monthly_comparison AS
SELECT
    ep.year,
    ep.month,
    ep.fips5,
    ep.fips2,
    ep.fips3,
    ep.state,
    state_name,
    county_name,
    state_iso,
    ep.pm25 AS epa_pm25,
    rm.pm25 AS rm_pm25
FROM
    exposures.pm25_monthly_county_epa AS ep
    full outer join exposures.pm25_monthly_county_mean as rm
    on
        ep.year = rm.year
        and ep.month = rm.month
        and ep.fips5 = rm.fips5
ORDER BY 1, 2, 3
;
CREATE INDEX cpm25_monthly_ym ON exposures.pm25_monthly_comparison (year, month);
CREATE INDEX cpm25_monthly_m ON exposures.pm25_monthly_comparison (month);
CREATE INDEX cpm25_monthly_f2 ON exposures.pm25_monthly_comparison (fips2);
CREATE INDEX cpm25_monthly_s ON exposures.pm25_monthly_comparison (state);
CREATE INDEX cpm25_monthly_f3 ON exposures.pm25_monthly_comparison (fips3);
CREATE INDEX cpm25_monthly_f5 ON exposures.pm25_monthly_comparison (fips5);

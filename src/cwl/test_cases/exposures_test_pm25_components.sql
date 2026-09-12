-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.bc' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(bc) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.6563475343706378 AND 0.6696070805195395 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.bc' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(bc) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.06415679008883848 AND 0.06545288685830997 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.county' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT county) FROM exposures.pm25_components_annual_county_mean) = '3221' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.county' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(county::varchar, '' order by county)) FROM exposures.pm25_components_annual_county_mean) = '0f85765ad1d6a9c2a6bfb7c774532077' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.fips2' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(fips2) FROM exposures.pm25_components_annual_county_mean) BETWEEN 30.983834212977335 AND 31.609770257683948 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.fips2' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(fips2) FROM exposures.pm25_components_annual_county_mean) BETWEEN 262.29520710833526 AND 267.59410018123094 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.fips3' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(fips3) FROM exposures.pm25_components_annual_county_mean) BETWEEN 102.05728966159579 AND 104.11905308910276 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.fips3' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(fips3) FROM exposures.pm25_components_annual_county_mean) BETWEEN 11324.344235285238 AND 11553.1188663011 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.fips5' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(fips5) FROM exposures.pm25_components_annual_county_mean) BETWEEN 31085.891502638933 AND 31713.88931077305 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.fips5' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(fips5) FROM exposures.pm25_components_annual_county_mean) BETWEEN 262777636.01464692 AND 268086275.12605396 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.nh4' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(nh4) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.7962715086961194 AND 0.8123578018010915 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.nh4' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(nh4) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.11160019764729098 AND 0.113854747094711 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.nit' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(nit) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.8646292036869823 AND 0.8820964603271233 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.nit' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(nit) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.3915997557084612 AND 0.39951086188438967 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.om' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(om) FROM exposures.pm25_components_annual_county_mean) BETWEEN 2.5170450704262404 AND 2.5678944657883864 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.om' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(om) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.695277182587269 AND 0.7093231862759006 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.pm25' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(pm25) FROM exposures.pm25_components_annual_county_mean) BETWEEN 7.583637749409997 AND 7.7368425524283815 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.pm25' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(pm25) FROM exposures.pm25_components_annual_county_mean) BETWEEN 5.1246658305747435 AND 5.228194433212618 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.so4' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(so4) FROM exposures.pm25_components_annual_county_mean) BETWEEN 1.9543144400620458 AND 1.993795539861279 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.so4' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(so4) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.5901095351177322 AND 0.6020309398675855 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.soil' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(soil) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.6173729365736865 AND 0.6298451171105287 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.soil' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(soil) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.08056324841078687 AND 0.08219078878272194 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.ss' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(ss) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.1775260543960497 AND 0.18111243933334367 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.ss' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(ss) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.0517597987203805 AND 0.052805451219782126 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.state' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT state) FROM exposures.pm25_components_annual_county_mean) = '52' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.state' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(state::varchar, '' order by state)) FROM exposures.pm25_components_annual_county_mean) = 'a32da4d8fedce872796c3456221fdcef' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.state_iso' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT state_iso) FROM exposures.pm25_components_annual_county_mean) = '52' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.state_iso' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(state_iso::varchar, '' order by state_iso)) FROM exposures.pm25_components_annual_county_mean) = '5b14c11d66d16d8fc87872887082e1d1' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.year' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT year) FROM exposures.pm25_components_annual_county_mean) = '2' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.year' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(year) FROM exposures.pm25_components_annual_county_mean) BETWEEN 1989.405 AND 2029.595 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.year' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(year) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.2475384257102934 AND 0.25253920198726904 
		THEN true ELSE false END AS passed

-- Test case end

-- Test case start
SELECT 
	'epa.airnow_pm25_2022.agencyname' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT agencyname) FROM epa.airnow_pm25_2022) = '127' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.agencyname' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(agencyname::varchar, '')) FROM epa.airnow_pm25_2022) = '8bfcd3fcc292502f4a683b6dc12d30ec' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.aqi' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(aqi) FROM epa.airnow_pm25_2022) BETWEEN 23.989301402987206 AND 24.473933754562704 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.aqi' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(aqi) FROM epa.airnow_pm25_2022) BETWEEN 1281.7717594607398 AND 1307.6661384397448 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.category' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT category) FROM epa.airnow_pm25_2022) = '7' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.category' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(category) FROM epa.airnow_pm25_2022) BETWEEN -9.547293187122587 AND -9.358237876486495 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.category' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(category) FROM epa.airnow_pm25_2022) BETWEEN 10341.02224880589 AND 10549.931789185808 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.county' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(county) FROM epa.airnow_pm25_2022) BETWEEN 29150.051480074962 AND 29738.94140896537 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.county' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(county) FROM epa.airnow_pm25_2022) BETWEEN 270375670.75455755 AND 275837805.51727587 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.countyfp' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(countyfp) FROM epa.airnow_pm25_2022) BETWEEN 70.48598392187809 AND 71.90994319302713 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.countyfp' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(countyfp) FROM epa.airnow_pm25_2022) BETWEEN 6438.64585222901 AND 6568.719505809395 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.fips5' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(fips5) FROM epa.airnow_pm25_2022) BETWEEN 29150.051480074962 AND 29738.94140896537 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.fips5' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(fips5) FROM epa.airnow_pm25_2022) BETWEEN 270375670.75455755 AND 275837805.51727587 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.fullaqscode' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT fullaqscode) FROM epa.airnow_pm25_2022) = '1176' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.fullaqscode' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(fullaqscode::varchar, '')) FROM epa.airnow_pm25_2022) = 'e21c77fff9376fbec77d66a7c8150853' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.intlaqscode' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT intlaqscode) FROM epa.airnow_pm25_2022) = '1176' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.intlaqscode' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(intlaqscode::varchar, '')) FROM epa.airnow_pm25_2022) = '2c9e9869567ce019f397650cd80e7d12' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.latitude' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(latitude) FROM epa.airnow_pm25_2022) BETWEEN 40.337899575047906 AND 41.15280663717008 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.latitude' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(latitude) FROM epa.airnow_pm25_2022) BETWEEN 41.568358848616576 AND 42.40812367384115 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.longitude' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(longitude) FROM epa.airnow_pm25_2022) BETWEEN -99.14829391785852 AND -97.18496136502964 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.longitude' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(longitude) FROM epa.airnow_pm25_2022) BETWEEN 344.4014824343221 AND 351.3590881400659 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.monitor' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT monitor) FROM epa.airnow_pm25_2022) = '1176' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.monitor' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(monitor::varchar, '')) FROM epa.airnow_pm25_2022) = '96a82bb18efd0c3ab58eca6f065f6f85' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.parameter' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT parameter) FROM epa.airnow_pm25_2022) = '1' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.parameter' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(parameter::varchar, '')) FROM epa.airnow_pm25_2022) = 'cd0240767d56b0e7c722798839185d2b' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.record' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT record) FROM epa.airnow_pm25_2022) = '269930' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.record' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(record::varchar, '')) FROM epa.airnow_pm25_2022) = 'dbfe09241f1e18b253feeae090e5a65d' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.sitename' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT sitename) FROM epa.airnow_pm25_2022) = '1161' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.sitename' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(sitename::varchar, '')) FROM epa.airnow_pm25_2022) = '12791833ea6db8895f7a7119eb19700e' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.state' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(state) FROM epa.airnow_pm25_2022) BETWEEN 29.079565496153087 AND 29.66703146577234 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.state' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(state) FROM epa.airnow_pm25_2022) BETWEEN 270.17279788533546 AND 275.63083420625134 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.statefp' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(statefp) FROM epa.airnow_pm25_2022) BETWEEN 29.079565496153087 AND 29.66703146577234 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.statefp' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(statefp) FROM epa.airnow_pm25_2022) BETWEEN 270.17279788533546 AND 275.63083420625134 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.stusps' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT stusps) FROM epa.airnow_pm25_2022) = '50' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.stusps' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(stusps::varchar, '')) FROM epa.airnow_pm25_2022) = '3f8ed7715aeb892f7443444f04ebf17a' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.unit' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT unit) FROM epa.airnow_pm25_2022) = '1' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.unit' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(unit::varchar, '')) FROM epa.airnow_pm25_2022) = '73c9646e24f4425a10c787a6f385eaae' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.utc' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT utc) FROM epa.airnow_pm25_2022) = '1965' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.utc' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(utc::varchar, '')) FROM epa.airnow_pm25_2022) = '266ce430183ae951c1b3b1ef1caedbb6' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.value' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(value) FROM epa.airnow_pm25_2022) BETWEEN 3.550946570352244 AND 3.6226828647027944 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.value' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(value) FROM epa.airnow_pm25_2022) BETWEEN 1027.074959677832 AND 1047.823948762233 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.zcta' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(zcta) FROM epa.airnow_pm25_2022) BETWEEN 60277.66145041563 AND 61495.39198476747 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.zcta' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(zcta) FROM epa.airnow_pm25_2022) BETWEEN 944410013.1104591 AND 963489003.2743068 
		THEN true ELSE false END AS passed

-- Test case end

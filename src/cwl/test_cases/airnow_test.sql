-- Test case start
SELECT 
	'epa.airnow_pm25_2022.agencyname' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT agencyname) FROM epa.airnow_pm25_2022) = '120' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.agencyname' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(agencyname::varchar, '' order by agencyname)) FROM epa.airnow_pm25_2022) = 'e42e43b35a2aa7cd0597c0fdfacebc20' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.aqi' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(aqi) FROM epa.airnow_pm25_2022) BETWEEN 33.44922107148058 AND 34.12496291130847 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.aqi' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(aqi) FROM epa.airnow_pm25_2022) BETWEEN 1342.3424065378422 AND 1369.460434952748 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.category' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT category) FROM epa.airnow_pm25_2022) = '6' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.category' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(category) FROM epa.airnow_pm25_2022) BETWEEN -8.203098767023242 AND -8.040661167676248 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.category' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(category) FROM epa.airnow_pm25_2022) BETWEEN 9189.881620272261 AND 9375.535794419176 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.county' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(county) FROM epa.airnow_pm25_2022) BETWEEN 28483.06713313461 AND 29058.482630773695 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.county' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(county) FROM epa.airnow_pm25_2022) BETWEEN 270775324.515041 AND 276245533.0911025 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.countyfp' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(countyfp) FROM epa.airnow_pm25_2022) BETWEEN 70.4405800733335 AND 71.863622095017 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.countyfp' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(countyfp) FROM epa.airnow_pm25_2022) BETWEEN 6448.332433135411 AND 6578.601775218955 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.fips5' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(fips5) FROM epa.airnow_pm25_2022) BETWEEN 28483.06713313461 AND 29058.482630773695 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.fips5' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(fips5) FROM epa.airnow_pm25_2022) BETWEEN 270775324.515041 AND 276245533.0911025 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.fullaqscode' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT fullaqscode) FROM epa.airnow_pm25_2022) = '1054' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.fullaqscode' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(fullaqscode::varchar, '' order by fullaqscode)) FROM epa.airnow_pm25_2022) = '2060c7bd74b6867dace575cda070171c' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.intlaqscode' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT intlaqscode) FROM epa.airnow_pm25_2022) = '1054' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.intlaqscode' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(intlaqscode::varchar, '' order by intlaqscode)) FROM epa.airnow_pm25_2022) = 'ad368507b3c3d87cbfbb6a3fe00cb8ac' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.latitude' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(latitude) FROM epa.airnow_pm25_2022) BETWEEN 40.41377958304486 AND 41.230219574621515 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.latitude' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(latitude) FROM epa.airnow_pm25_2022) BETWEEN 41.561173070883854 AND 42.40079272888151 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.longitude' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(longitude) FROM epa.airnow_pm25_2022) BETWEEN -99.29274201932638 AND -97.32654910805259 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.longitude' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(longitude) FROM epa.airnow_pm25_2022) BETWEEN 342.83656587227 AND 349.76255710201286 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.monitor' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT monitor) FROM epa.airnow_pm25_2022) = '1054' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.monitor' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(monitor::varchar, '' order by monitor)) FROM epa.airnow_pm25_2022) = '8eed7a9fa8459b553ee97b9c791fb7bf' 
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
		WHEN (SELECT MD5(string_agg(parameter::varchar, '' order by parameter)) FROM epa.airnow_pm25_2022) = '8bc2e46d684aec8b2a5dde5e2ff91011' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.record' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT record) FROM epa.airnow_pm25_2022) = '46554' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.record' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(record::varchar, '' order by record)) FROM epa.airnow_pm25_2022) = '19183599b0c7aa421d8a7f3e818d097e' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.sitename' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT sitename) FROM epa.airnow_pm25_2022) = '1039' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.sitename' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(sitename::varchar, '' order by sitename)) FROM epa.airnow_pm25_2022) = '01537deade5987091dda5f7cff18f90b' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.state' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(state) FROM epa.airnow_pm25_2022) BETWEEN 28.412626553061276 AND 28.986619008678677 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.state' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(state) FROM epa.airnow_pm25_2022) BETWEEN 270.6109844507679 AND 276.07787302553083 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.statefp' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(statefp) FROM epa.airnow_pm25_2022) BETWEEN 28.412626553061276 AND 28.986619008678677 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.statefp' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(statefp) FROM epa.airnow_pm25_2022) BETWEEN 270.6109844507679 AND 276.07787302553083 
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
		WHEN (SELECT MD5(string_agg(stusps::varchar, '' order by stusps)) FROM epa.airnow_pm25_2022) = '8236a07d0086d3e5ab2a633438050052' 
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
		WHEN (SELECT MD5(string_agg(unit::varchar, '' order by unit)) FROM epa.airnow_pm25_2022) = 'ce6c89cefcb767a0fc20d8e253896efc' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.utc' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT utc) FROM epa.airnow_pm25_2022) = '321' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.utc' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(utc::varchar, '' order by utc)) FROM epa.airnow_pm25_2022) = 'ec3dbcfa9fa76326d96a44b6ef21e630' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.value' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(value) FROM epa.airnow_pm25_2022) BETWEEN 4.615041643379898 AND 4.708274807892623 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.value' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(value) FROM epa.airnow_pm25_2022) BETWEEN 989.3046217746838 AND 1009.290573729728 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.zcta' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(zcta) FROM epa.airnow_pm25_2022) BETWEEN 60512.48924799704 AND 61734.963778259604 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.zcta' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(zcta) FROM epa.airnow_pm25_2022) BETWEEN 922955446.7469195 AND 941601011.3276654 
		THEN true ELSE false END AS passed

-- Test case end

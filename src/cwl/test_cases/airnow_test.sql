-- Test case start
SELECT 
	'epa.airnow_pm25_2022.agencyname' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT agencyname) FROM epa.airnow_pm25_2022) = '126' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.agencyname' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(agencyname::varchar, '' order by agencyname)) FROM epa.airnow_pm25_2022) = 'efb0c6ddb859d8a357540d0ca4e10ab8' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.aqi' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(aqi) FROM epa.airnow_pm25_2022) BETWEEN 30.52329272514281 AND 31.13992490140832 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.aqi' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(aqi) FROM epa.airnow_pm25_2022) BETWEEN 1279.0248739613687 AND 1304.8637603040227 
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
		WHEN (SELECT AVG(category) FROM epa.airnow_pm25_2022) BETWEEN -9.281832024146528 AND -9.098033370203034 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.category' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(category) FROM epa.airnow_pm25_2022) BETWEEN 10190.738404304393 AND 10396.611907421655 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.county' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(county) FROM epa.airnow_pm25_2022) BETWEEN 28834.996731841922 AND 29417.52191834378 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.county' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(county) FROM epa.airnow_pm25_2022) BETWEEN 266210178.3882168 AND 271588161.78999895 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.countyfp' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(countyfp) FROM epa.airnow_pm25_2022) BETWEEN 70.29652135963377 AND 71.71665310427284 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.countyfp' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(countyfp) FROM epa.airnow_pm25_2022) BETWEEN 6359.567011231304 AND 6488.0431124683 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.fips5' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(fips5) FROM epa.airnow_pm25_2022) BETWEEN 28834.996731841922 AND 29417.52191834378 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.fips5' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(fips5) FROM epa.airnow_pm25_2022) BETWEEN 266210178.3882168 AND 271588161.78999895 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.fullaqscode' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT fullaqscode) FROM epa.airnow_pm25_2022) = '1157' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.fullaqscode' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(fullaqscode::varchar, '' order by fullaqscode)) FROM epa.airnow_pm25_2022) = 'b3aa2851cfa54db7480f701eac37b0ff' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.intlaqscode' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT intlaqscode) FROM epa.airnow_pm25_2022) = '1157' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.intlaqscode' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(intlaqscode::varchar, '' order by intlaqscode)) FROM epa.airnow_pm25_2022) = 'd35ad20fd649999c51e4917a6c024dfe' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.latitude' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(latitude) FROM epa.airnow_pm25_2022) BETWEEN 40.37531130098637 AND 41.19097415555176 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.latitude' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(latitude) FROM epa.airnow_pm25_2022) BETWEEN 41.23567738980816 AND 42.068721377481054 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.longitude' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(longitude) FROM epa.airnow_pm25_2022) BETWEEN -99.1896801748497 AND -97.2255280921794 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.longitude' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(longitude) FROM epa.airnow_pm25_2022) BETWEEN 343.7438091719147 AND 350.68812854912505 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.monitor' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT monitor) FROM epa.airnow_pm25_2022) = '1157' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.monitor' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(monitor::varchar, '' order by monitor)) FROM epa.airnow_pm25_2022) = '647ad82facaedddf429904ce8115ce37' 
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
		WHEN (SELECT MD5(string_agg(parameter::varchar, '' order by parameter)) FROM epa.airnow_pm25_2022) = '5ac82262d1576ff0211e9c263915cad3' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.record' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT record) FROM epa.airnow_pm25_2022) = '266705' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.record' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(record::varchar, '' order by record)) FROM epa.airnow_pm25_2022) = '34067e2f727594be311c09cd8abb1f1e' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.sitename' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT sitename) FROM epa.airnow_pm25_2022) = '1142' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.sitename' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(sitename::varchar, '' order by sitename)) FROM epa.airnow_pm25_2022) = 'fed34eff122046a5508b9b9c82a61419' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.state' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(state) FROM epa.airnow_pm25_2022) BETWEEN 28.764700210482292 AND 29.34580526523951 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.state' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(state) FROM epa.airnow_pm25_2022) BETWEEN 266.022493856625 AND 271.3966856517083 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.statefp' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(statefp) FROM epa.airnow_pm25_2022) BETWEEN 28.764700210482292 AND 29.34580526523951 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.statefp' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(statefp) FROM epa.airnow_pm25_2022) BETWEEN 266.022493856625 AND 271.3966856517083 
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
		WHEN (SELECT MD5(string_agg(stusps::varchar, '' order by stusps)) FROM epa.airnow_pm25_2022) = '6bef9ce45d6c8c9db53d0a25eacc9226' 
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
		WHEN (SELECT MD5(string_agg(unit::varchar, '' order by unit)) FROM epa.airnow_pm25_2022) = 'b7926a3a98091e104c71425cde6bd9fb' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.utc' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT utc) FROM epa.airnow_pm25_2022) = '1919' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.utc' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(utc::varchar, '' order by utc)) FROM epa.airnow_pm25_2022) = '21342b947bb298addd3f6ce73ebd9642' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.value' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(value) FROM epa.airnow_pm25_2022) BETWEEN 3.6543681092309277 AND 3.7281937275992294 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.value' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(value) FROM epa.airnow_pm25_2022) BETWEEN 909.5639002320942 AND 927.9389285196113 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.zcta' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(zcta) FROM epa.airnow_pm25_2022) BETWEEN 60264.06892267724 AND 61481.524860509104 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.airnow_pm25_2022.zcta' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(zcta) FROM epa.airnow_pm25_2022) BETWEEN 936105341.634869 AND 955016560.6577955 
		THEN true ELSE false END AS passed

-- Test case end

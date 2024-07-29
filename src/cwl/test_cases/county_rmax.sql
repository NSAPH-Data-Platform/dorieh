-- Test case start
SELECT 
	'climate.county_rmax.county' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT county) FROM climate.county_rmax) = '3221' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.county' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(county::varchar, '' order by county)) FROM climate.county_rmax) = 'd8504aca08ea5048996363e051ff1572' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.day_of_the_year' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(day_of_the_year) FROM climate.county_rmax) BETWEEN 181.17 AND 184.83 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.day_of_the_year' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(day_of_the_year) FROM climate.county_rmax) BETWEEN 10990.984674369261 AND 11213.024768800962 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.fips2' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(fips2) FROM climate.county_rmax) BETWEEN 30.983834212977335 AND 31.609770257683948 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.fips2' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(fips2) FROM climate.county_rmax) BETWEEN 262.25460221834004 AND 267.55267499042776 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.fips3' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(fips3) FROM climate.county_rmax) BETWEEN 102.05728966159579 AND 104.11905308910276 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.fips3' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(fips3) FROM climate.county_rmax) BETWEEN 11322.591158067355 AND 11551.330373381848 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.fips5' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(fips5) FROM climate.county_rmax) BETWEEN 31085.891502638933 AND 31713.88931077305 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.fips5' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(fips5) FROM climate.county_rmax) BETWEEN 262736956.44172907 AND 268044773.7435822 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.month' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT month) FROM climate.county_rmax) = '12' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.month' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(month) FROM climate.county_rmax) BETWEEN 6.46076712328767 AND 6.591287671232877 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.month' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(month) FROM climate.county_rmax) BETWEEN 11.76880695675591 AND 12.006560632649968 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.observation_date' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT observation_date) FROM climate.county_rmax) = '730' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.rmax' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(rmax) FROM climate.county_rmax) BETWEEN 86.39938453812883 AND 88.14482665001023 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.rmax' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(rmax) FROM climate.county_rmax) BETWEEN 199.14711154448997 AND 203.1702855150857 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.state' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT state) FROM climate.county_rmax) = '52' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.state' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(state::varchar, '' order by state)) FROM climate.county_rmax) = '726da1cf93f1f96047cf6cc6922b41f0' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.state_iso' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT state_iso) FROM climate.county_rmax) = '52' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.state_iso' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(state_iso::varchar, '' order by state_iso)) FROM climate.county_rmax) = '2d5a3a771365d55cab6f5ce6b6b7040b' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.year' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT year) FROM climate.county_rmax) = '2' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.year' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(year) FROM climate.county_rmax) BETWEEN 1989.405 AND 2029.595 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.year' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(year) FROM climate.county_rmax) BETWEEN 0.24750010525962124 AND 0.25250010738607825 
		THEN true ELSE false END AS passed

-- Test case end

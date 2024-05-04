-- Test case start
SELECT 
	'climate.county_rmax.county' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(county) FROM climate.county_rmax) BETWEEN 31135.78794546223 AND 31764.79376254228 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.county' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(county) FROM climate.county_rmax) BETWEEN 264298493.8085356 AND 269637857.31981915 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.observation_date' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT observation_date) FROM climate.county_rmax) = '264' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.rmax' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(rmax) FROM climate.county_rmax) BETWEEN 86.11785126701962 AND 87.85760583807051 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmax.rmax' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(rmax) FROM climate.county_rmax) BETWEEN 316.62930137553093 AND 323.025852918471 
		THEN true ELSE false END AS passed

-- Test case end

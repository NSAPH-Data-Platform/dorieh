-- Test case start
SELECT 
	'climate.county_rmin.county' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(county) FROM climate.county_rmin) BETWEEN 31135.78794546223 AND 31764.79376254228 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmin.county' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(county) FROM climate.county_rmin) BETWEEN 264298493.8085356 AND 269637857.31981915 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmin.observation_date' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT observation_date) FROM climate.county_rmin) = '264' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmin.rmin' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(rmin) FROM climate.county_rmin) BETWEEN 46.28944401420604 AND 47.224584297321314 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'climate.county_rmin.rmin' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(rmin) FROM climate.county_rmin) BETWEEN 379.20946608357747 AND 386.8702633781952 
		THEN true ELSE false END AS passed

-- Test case end

-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.bc' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(bc) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.6576247141430052 AND 0.67091006190347 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.bc' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(bc) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.0793798008220431 AND 0.08098343316188236 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.nh4' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(nh4) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.8431400639042059 AND 0.8601731965083312 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.nh4' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(nh4) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.24612174047159655 AND 0.25109389684476013 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.nit' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(nit) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.9928360109009963 AND 1.0128933040505113 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.nit' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(nit) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.4693774094516653 AND 0.4788597813597797 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.om' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(om) FROM exposures.pm25_components_annual_county_mean) BETWEEN 2.8686305588145964 AND 2.9265826913159017 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.om' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(om) FROM exposures.pm25_components_annual_county_mean) BETWEEN 1.0163852601175227 AND 1.0369182956754526 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.pm25' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(pm25) FROM exposures.pm25_components_annual_county_mean) BETWEEN 8.365317699053495 AND 8.534314016206093 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.pm25' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(pm25) FROM exposures.pm25_components_annual_county_mean) BETWEEN 7.995489357364692 AND 8.157014394887211 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.so4' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(so4) FROM exposures.pm25_components_annual_county_mean) BETWEEN 2.160679747743267 AND 2.204329843657272 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.so4' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(so4) FROM exposures.pm25_components_annual_county_mean) BETWEEN 1.3694808843691324 AND 1.3971471648614382 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.soil' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(soil) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.5595299418209477 AND 0.5708335770092497 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.soil' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(soil) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.10816289179463176 AND 0.11034800071977585 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.ss' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(ss) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.28293915393006747 AND 0.2886550964337052 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.ss' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(ss) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.08522955088863568 AND 0.08695135999749701 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.year' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT year) FROM exposures.pm25_components_annual_county_mean) = '18' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.year' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(year) FROM exposures.pm25_components_annual_county_mean) BETWEEN 1988.4896434744587 AND 2028.6611514234378 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.year' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(year) FROM exposures.pm25_components_annual_county_mean) BETWEEN 26.69362790800671 AND 27.232893118269473 
		THEN true ELSE false END AS passed

-- Test case end
    
-- ????
-- UNION ALL
-- -- Test case start
-- SELECT
-- 	'exposures.pm25_components_annual_county_mean.zcta' As table_column,
-- 	'count distinct' As Testing,
-- 	CASE
-- 		WHEN (SELECT COUNT(DISTINCT zcta) FROM exposures.pm25_components_annual_county_mean) = '33804'
-- 		THEN true ELSE false END AS passed
--
-- -- Test case end
-- UNION ALL
-- -- Test case start
-- SELECT
-- 	'exposures.pm25_components_annual_county_mean.zcta' As table_column,
-- 	'MD5 value' As Testing,
-- 	CASE
-- 		WHEN (SELECT MD5(string_agg(zcta::varchar, '')) FROM exposures.pm25_components_annual_county_mean) = '12b3cbafbe4d32784a0c54915dfd3f4d'
-- 		THEN true ELSE false END AS passed
--
-- Test case end

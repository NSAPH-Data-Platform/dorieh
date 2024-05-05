-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.bc' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(bc) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.6124995071537814 AND 0.6248732345710296 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.bc' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(bc) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.06240171287378741 AND 0.06366235353790432 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.county' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT county) FROM exposures.pm25_components_annual_county_mean) = '3236' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.county' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(county::varchar, '')) FROM exposures.pm25_components_annual_county_mean) = 'c90f7b9304fcd6913abff7cc6e21a24d' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.fips2' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(fips2) FROM exposures.pm25_components_annual_county_mean) BETWEEN 31.02250176605386 AND 31.649218973448885 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.fips2' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(fips2) FROM exposures.pm25_components_annual_county_mean) BETWEEN 263.4524803245169 AND 268.77475265430513 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.fips3' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(fips3) FROM exposures.pm25_components_annual_county_mean) BETWEEN 101.96275056427574 AND 104.0226041110288 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.fips3' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(fips3) FROM exposures.pm25_components_annual_county_mean) BETWEEN 11302.961786570691 AND 11531.304448925655 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.fips5' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(fips5) FROM exposures.pm25_components_annual_county_mean) BETWEEN 31124.464516618136 AND 31753.241577559915 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.fips5' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(fips5) FROM exposures.pm25_components_annual_county_mean) BETWEEN 263929237.85514632 AND 269261141.6501998 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.nh4' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(nh4) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.7788980919273153 AND 0.794633406915746 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.nh4' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(nh4) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.20945610481140178 AND 0.21368754127223819 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.nit' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(nit) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.8379800141854943 AND 0.8549089033609589 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.nit' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(nit) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.32947864817171707 AND 0.33613478247821643 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.om' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(om) FROM exposures.pm25_components_annual_county_mean) BETWEEN 2.7179507413223747 AND 2.7728588371066647 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.om' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(om) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.8616532904547463 AND 0.8790604276356502 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.pm25' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(pm25) FROM exposures.pm25_components_annual_county_mean) BETWEEN 7.860270252277878 AND 8.019063590707734 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.pm25' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(pm25) FROM exposures.pm25_components_annual_county_mean) BETWEEN 6.97200380142324 AND 7.1128523630681535 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.so4' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(so4) FROM exposures.pm25_components_annual_county_mean) BETWEEN 2.1177554426385528 AND 2.160538380873675 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.so4' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(so4) FROM exposures.pm25_components_annual_county_mean) BETWEEN 1.3050561786513764 AND 1.3314209499372627 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.soil' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(soil) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.5715891921212602 AND 0.5831364485277503 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.soil' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(soil) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.07560580991074504 AND 0.07713320000995201 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.ss' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(ss) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.22365470511295898 AND 0.22817298198392788 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.ss' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(ss) FROM exposures.pm25_components_annual_county_mean) BETWEEN 0.04993301395902126 AND 0.05094176171576916 
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
		WHEN (SELECT MD5(string_agg(state::varchar, '')) FROM exposures.pm25_components_annual_county_mean) = '76404b04a7221490841601d5ad0dc21a' 
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
		WHEN (SELECT MD5(string_agg(state_iso::varchar, '')) FROM exposures.pm25_components_annual_county_mean) = '1eb3436976d4c44e7e74d5df216876c2' 
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
		WHEN (SELECT AVG(year) FROM exposures.pm25_components_annual_county_mean) BETWEEN 1988.4217291821017 AND 2028.5918651251743 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'exposures.pm25_components_annual_county_mean.year' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(year) FROM exposures.pm25_components_annual_county_mean) BETWEEN 26.66553978148215 AND 27.204237554845424 
		THEN true ELSE false END AS passed

-- Test case end

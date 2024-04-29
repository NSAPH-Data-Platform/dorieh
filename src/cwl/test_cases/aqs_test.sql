-- Test case start
SELECT 
	'epa.pm25_annual.address' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT address) FROM epa.pm25_annual) = '993' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.address' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(address::varchar, '')) FROM epa.pm25_annual) = 'ec9230a8a7127a522a2ecd7f8c052fd3' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.arithmetic_mean' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(arithmetic_mean) FROM epa.pm25_annual) BETWEEN 9.627916329030045 AND 9.822419689212472 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.arithmetic_mean' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(arithmetic_mean) FROM epa.pm25_annual) BETWEEN 7.763678420205004 AND 7.920520408491974 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.arithmetic_standard_dev' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(arithmetic_standard_dev) FROM epa.pm25_annual) BETWEEN 5.6094210487397165 AND 5.722742686087993 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.arithmetic_standard_dev' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(arithmetic_standard_dev) FROM epa.pm25_annual) BETWEEN 4.536551403561332 AND 4.628198906663582 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_10th_percentile' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(c_10th_percentile) FROM epa.pm25_annual) BETWEEN 4.233091033742697 AND 4.318608024323358 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_10th_percentile' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(c_10th_percentile) FROM epa.pm25_annual) BETWEEN 3.575286852546901 AND 3.6475148697700703 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_1st_max_datetime' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT c_1st_max_datetime) FROM epa.pm25_annual) = '758' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_1st_max_datetime' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(c_1st_max_datetime::varchar, '')) FROM epa.pm25_annual) = 'e3de45d8b4510254a55484458e3445a1' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_1st_max_non_overlapping_value' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT c_1st_max_non_overlapping_value) FROM epa.pm25_annual) = '0' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_1st_max_non_overlapping_value' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(c_1st_max_non_overlapping_value::varchar, '')) FROM epa.pm25_annual) IS NULL 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_1st_max_value' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(c_1st_max_value) FROM epa.pm25_annual) BETWEEN 36.345742398950755 AND 37.07999982115178 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_1st_max_value' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(c_1st_max_value) FROM epa.pm25_annual) BETWEEN 1474.2724295961407 AND 1504.0557110021232 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_1st_no_max_datetime' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT c_1st_no_max_datetime) FROM epa.pm25_annual) = '0' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_1st_no_max_datetime' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(c_1st_no_max_datetime::varchar, '')) FROM epa.pm25_annual) IS NULL 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_2nd_max_datetime' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT c_2nd_max_datetime) FROM epa.pm25_annual) = '801' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_2nd_max_datetime' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(c_2nd_max_datetime::varchar, '')) FROM epa.pm25_annual) = '9a60accc3b4ef3079888d279d1ffc115' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_2nd_max_non_overlapping_value' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT c_2nd_max_non_overlapping_value) FROM epa.pm25_annual) = '0' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_2nd_max_non_overlapping_value' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(c_2nd_max_non_overlapping_value::varchar, '')) FROM epa.pm25_annual) IS NULL 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_2nd_max_value' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT c_2nd_max_value) FROM epa.pm25_annual) = '720' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_2nd_max_value' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(c_2nd_max_value::varchar, '')) FROM epa.pm25_annual) = '516b00296c832606b489471fa56134ca' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_2nd_no_max_datetime' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT c_2nd_no_max_datetime) FROM epa.pm25_annual) = '0' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_2nd_no_max_datetime' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(c_2nd_no_max_datetime::varchar, '')) FROM epa.pm25_annual) IS NULL 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_3rd_max_datetime' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT c_3rd_max_datetime) FROM epa.pm25_annual) = '838' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_3rd_max_datetime' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(c_3rd_max_datetime::varchar, '')) FROM epa.pm25_annual) = '2a242e0cc05b7f581d01e9c152063c78' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_3rd_max_value' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT c_3rd_max_value) FROM epa.pm25_annual) = '657' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_3rd_max_value' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(c_3rd_max_value::varchar, '')) FROM epa.pm25_annual) = '582f6f97e6902531b62490306285f604' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_4th_max_datetime' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT c_4th_max_datetime) FROM epa.pm25_annual) = '859' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_4th_max_datetime' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(c_4th_max_datetime::varchar, '')) FROM epa.pm25_annual) = 'c01d956db14baf101955059c7ec93f09' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_4th_max_value' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT c_4th_max_value) FROM epa.pm25_annual) = '630' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_4th_max_value' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(c_4th_max_value::varchar, '')) FROM epa.pm25_annual) = 'aa6f85bdd4e8462125f51e8969b31410' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_50th_percentile' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(c_50th_percentile) FROM epa.pm25_annual) BETWEEN 8.573521581018243 AND 8.746724037200428 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_50th_percentile' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(c_50th_percentile) FROM epa.pm25_annual) BETWEEN 7.891667345468497 AND 8.051094968609275 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_75th_percentile' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(c_75th_percentile) FROM epa.pm25_annual) BETWEEN 12.307794026469535 AND 12.556436330034577 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_75th_percentile' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(c_75th_percentile) FROM epa.pm25_annual) BETWEEN 14.614393194893033 AND 14.90963346145653 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_90th_percentile' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(c_90th_percentile) FROM epa.pm25_annual) BETWEEN 17.015534994634553 AND 17.359283176344345 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_90th_percentile' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(c_90th_percentile) FROM epa.pm25_annual) BETWEEN 29.146664829837643 AND 29.73548634155154 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_95th_percentile' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(c_95th_percentile) FROM epa.pm25_annual) BETWEEN 20.584811374746632 AND 21.000666149994036 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_95th_percentile' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(c_95th_percentile) FROM epa.pm25_annual) BETWEEN 46.714846957935016 AND 47.65858123991351 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_98th_percentile' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(c_98th_percentile) FROM epa.pm25_annual) BETWEEN 24.589790449505184 AND 25.086553892929533 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_98th_percentile' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(c_98th_percentile) FROM epa.pm25_annual) BETWEEN 77.23104259674369 AND 78.79126567950618 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_99th_percentile' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(c_99th_percentile) FROM epa.pm25_annual) BETWEEN 27.656648026708 AND 28.215368188863717 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_99th_percentile' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(c_99th_percentile) FROM epa.pm25_annual) BETWEEN 114.48248629296299 AND 116.79526379383094 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.cbsa_name' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT cbsa_name) FROM epa.pm25_annual) = '378' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.cbsa_name' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(cbsa_name::varchar, '')) FROM epa.pm25_annual) = 'cb0fe1122176e5ed11c685a439f82e68' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.certification_indicator' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT certification_indicator) FROM epa.pm25_annual) = '6' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.certification_indicator' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(certification_indicator::varchar, '')) FROM epa.pm25_annual) = '36a6f62f618f0399a36cb042531b5e24' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.city_name' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT city_name) FROM epa.pm25_annual) = '674' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.city_name' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(city_name::varchar, '')) FROM epa.pm25_annual) = 'bd69e3758a2a31ed3fdb3260ea7deab1' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.completeness_indicator' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT completeness_indicator) FROM epa.pm25_annual) = '2' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.completeness_indicator' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(completeness_indicator::varchar, '')) FROM epa.pm25_annual) = '6726d0fb6738e3f3d336e4c10d20165d' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.county_code' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT county_code) FROM epa.pm25_annual) = '126' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.county_code' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(county_code::varchar, '')) FROM epa.pm25_annual) = '13aad789762bd9749d10cd4393f5f1c2' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.county_name' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT county_name) FROM epa.pm25_annual) = '517' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.county_name' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(county_name::varchar, '')) FROM epa.pm25_annual) = 'eaa955a371d6dd92e9699283e36d65ea' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.date_of_last_change' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT date_of_last_change) FROM epa.pm25_annual) = '51' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.datum' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT datum) FROM epa.pm25_annual) = '2' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.datum' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(datum::varchar, '')) FROM epa.pm25_annual) = 'bcc35414a683bbcea4389eab8017b234' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.event_type' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT event_type) FROM epa.pm25_annual) = '4' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.event_type' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(event_type::varchar, '')) FROM epa.pm25_annual) = '006d31ad0996c7d8d62bbb9969e2c7aa' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.exceptional_data_count' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(exceptional_data_count) FROM epa.pm25_annual) BETWEEN 66.39557112197448 AND 67.73689579110527 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.exceptional_data_count' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(exceptional_data_count) FROM epa.pm25_annual) BETWEEN 432627.6217933872 AND 441367.57374880917 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.latitude' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(latitude) FROM epa.pm25_annual) BETWEEN 38.03261812908132 AND 38.800953848860736 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.latitude' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(latitude) FROM epa.pm25_annual) BETWEEN 40.29847174575818 AND 41.11258228607653 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.local_site_name' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT local_site_name) FROM epa.pm25_annual) = '950' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.local_site_name' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(local_site_name::varchar, '')) FROM epa.pm25_annual) = '88b5c334d44684b5b1436fdb8b202a31' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.longitude' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(longitude) FROM epa.pm25_annual) BETWEEN -96.98953747685465 AND -95.06895257632289 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.longitude' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(longitude) FROM epa.pm25_annual) BETWEEN 379.44622059104296 AND 387.1118008050034 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.method_name' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT method_name) FROM epa.pm25_annual) = '19' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.method_name' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(method_name::varchar, '')) FROM epa.pm25_annual) = '123e081ccb3fddda43f417ab31c029f8' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.metric_used' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT metric_used) FROM epa.pm25_annual) = '3' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.metric_used' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(metric_used::varchar, '')) FROM epa.pm25_annual) = 'e536482f26ebbb95686e014975825dab' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.monitor' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT monitor) FROM epa.pm25_annual) = '994' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.monitor' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(monitor::varchar, '')) FROM epa.pm25_annual) = '37d7c3ea9eeb7f987976e5226493bbc8' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.null_data_count' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(null_data_count) FROM epa.pm25_annual) BETWEEN 28.84415225944915 AND 29.426862406104686 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.null_data_count' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(null_data_count) FROM epa.pm25_annual) BETWEEN 38092.828733197064 AND 38862.3808288172 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.num_obs_below_mdl' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(num_obs_below_mdl) FROM epa.pm25_annual) BETWEEN 0.0 AND 0.0 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.num_obs_below_mdl' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(num_obs_below_mdl) FROM epa.pm25_annual) BETWEEN 0.0 AND 0.0 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.observation_count' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(observation_count) FROM epa.pm25_annual) BETWEEN 398.9148754024085 AND 406.97376177417436 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.observation_count' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(observation_count) FROM epa.pm25_annual) BETWEEN 1753472.9706274145 AND 1788896.6670037261 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.observation_percent' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(observation_percent) FROM epa.pm25_annual) BETWEEN 85.04037438893526 AND 86.7583617503279 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.observation_percent' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(observation_percent) FROM epa.pm25_annual) BETWEEN 418.05954283482515 AND 426.50519016482167 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.parameter_code' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT parameter_code) FROM epa.pm25_annual) = '1' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.parameter_code' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(parameter_code::varchar, '')) FROM epa.pm25_annual) = '16918fd1636766a91923b35a1332dc0c' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.parameter_name' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT parameter_name) FROM epa.pm25_annual) = '1' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.parameter_name' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(parameter_name::varchar, '')) FROM epa.pm25_annual) = 'fce443b4cda113128d5f1c45c4ab75fa' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.poc' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(poc) FROM epa.pm25_annual) BETWEEN 1.591235841182783 AND 1.6233820197925362 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.poc' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(poc) FROM epa.pm25_annual) BETWEEN 0.9848852611858934 AND 1.0047819331290428 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.pollutant_standard' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT pollutant_standard) FROM epa.pm25_annual) = '6' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.pollutant_standard' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(pollutant_standard::varchar, '')) FROM epa.pm25_annual) = '42f8d63f5424b75931d1a14d6b78ad8f' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.primary_exceedance_count' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT primary_exceedance_count) FROM epa.pm25_annual) = '138' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.primary_exceedance_count' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(primary_exceedance_count::varchar, '')) FROM epa.pm25_annual) = '97780607d4d5eef906bc24dde95d1de5' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.record' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT record) FROM epa.pm25_annual) = '16774' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.record' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(record::varchar, '')) FROM epa.pm25_annual) = 'f63d1437b2db3faee82345f5d918d7c0' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.required_day_count' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(required_day_count) FROM epa.pm25_annual) BETWEEN 188.30102181948254 AND 192.10508286634078 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.required_day_count' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(required_day_count) FROM epa.pm25_annual) BETWEEN 16110.2618195721 AND 16435.72165431093 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.sample_duration' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT sample_duration) FROM epa.pm25_annual) = '3' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.sample_duration' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(sample_duration::varchar, '')) FROM epa.pm25_annual) = '336664c4f9b959251960fd58af3e7669' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.secondary_exceedance_count' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT secondary_exceedance_count) FROM epa.pm25_annual) = '138' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.secondary_exceedance_count' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(secondary_exceedance_count::varchar, '')) FROM epa.pm25_annual) = '97780607d4d5eef906bc24dde95d1de5' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.site_num' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT site_num) FROM epa.pm25_annual) = '218' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.site_num' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(site_num::varchar, '')) FROM epa.pm25_annual) = 'e6ccc8c43e80d65a715afbc98428c2b7' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.state_code' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT state_code) FROM epa.pm25_annual) = '52' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.state_code' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(state_code::varchar, '')) FROM epa.pm25_annual) = 'd62420b790c30e771f0c00b16a9f2fc9' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.state_name' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT state_name) FROM epa.pm25_annual) = '52' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.state_name' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(state_name::varchar, '')) FROM epa.pm25_annual) = '940e8be7508584f3222bd87fd7ffc015' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.units_of_measure' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT units_of_measure) FROM epa.pm25_annual) = '1' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.units_of_measure' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(units_of_measure::varchar, '')) FROM epa.pm25_annual) = '3efe11b94b1ccc9abf4d1260c43ca00a' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.valid_day_count' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(valid_day_count) FROM epa.pm25_annual) BETWEEN 158.58337486586385 AND 161.78707940860858 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.valid_day_count' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(valid_day_count) FROM epa.pm25_annual) BETWEEN 13013.235906772297 AND 13276.129561454567 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.year' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(year) FROM epa.pm25_annual) BETWEEN 1990.3807762012639 AND 2030.5904888517944 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.year' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(year) FROM epa.pm25_annual) BETWEEN 0.2473103836227622 AND 0.2523065529888786 
		THEN true ELSE false END AS passed

-- Test case end

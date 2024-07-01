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
		WHEN (SELECT MD5(string_agg(address::varchar, '' order by address)) FROM epa.pm25_annual) = 'a9d9efbd73758559b709f5743b0a0298' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.arithmetic_mean' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(arithmetic_mean) FROM epa.pm25_annual) BETWEEN 9.629209926363096 AND 9.823739419824978 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.arithmetic_mean' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(arithmetic_mean) FROM epa.pm25_annual) BETWEEN 7.838455816201485 AND 7.99680845895303 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.arithmetic_standard_dev' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(arithmetic_standard_dev) FROM epa.pm25_annual) BETWEEN 5.609451331035894 AND 5.722773580147731 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.arithmetic_standard_dev' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(arithmetic_standard_dev) FROM epa.pm25_annual) BETWEEN 4.5492152627144975 AND 4.641118601355194 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_10th_percentile' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(c_10th_percentile) FROM epa.pm25_annual) BETWEEN 4.2345429799426935 AND 4.320089302769819 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_10th_percentile' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(c_10th_percentile) FROM epa.pm25_annual) BETWEEN 3.5833437485749045 AND 3.6557345313743976 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_1st_max_datetime' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT c_1st_max_datetime) FROM epa.pm25_annual) = '760' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_1st_max_datetime' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(c_1st_max_datetime::varchar, '' order by c_1st_max_datetime)) FROM epa.pm25_annual) = '809d0fe4f270d463378b7208c29be0f2' 
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
		WHEN (SELECT MD5(string_agg(c_1st_max_non_overlapping_value::varchar, '' order by c_1st_max_non_overlapping_value)) FROM epa.pm25_annual) IS NULL 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_1st_max_value' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(c_1st_max_value) FROM epa.pm25_annual) BETWEEN 36.31439234648472 AND 37.04801643429249 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_1st_max_value' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(c_1st_max_value) FROM epa.pm25_annual) BETWEEN 1470.596999364861 AND 1500.3060296550602 
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
		WHEN (SELECT MD5(string_agg(c_1st_no_max_datetime::varchar, '' order by c_1st_no_max_datetime)) FROM epa.pm25_annual) IS NULL 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_2nd_max_datetime' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT c_2nd_max_datetime) FROM epa.pm25_annual) = '804' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_2nd_max_datetime' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(c_2nd_max_datetime::varchar, '' order by c_2nd_max_datetime)) FROM epa.pm25_annual) = '9e0797d9d1acd7f40d263c4ff24844dd' 
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
		WHEN (SELECT MD5(string_agg(c_2nd_max_non_overlapping_value::varchar, '' order by c_2nd_max_non_overlapping_value)) FROM epa.pm25_annual) IS NULL 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_2nd_max_value' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(c_2nd_max_value) FROM epa.pm25_annual) BETWEEN 29.637130914920142 AND 30.23586083239328 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_2nd_max_value' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(c_2nd_max_value) FROM epa.pm25_annual) BETWEEN 553.1244621794679 AND 564.298693738649 
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
		WHEN (SELECT MD5(string_agg(c_2nd_no_max_datetime::varchar, '' order by c_2nd_no_max_datetime)) FROM epa.pm25_annual) IS NULL 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_3rd_max_datetime' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT c_3rd_max_datetime) FROM epa.pm25_annual) = '840' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_3rd_max_datetime' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(c_3rd_max_datetime::varchar, '' order by c_3rd_max_datetime)) FROM epa.pm25_annual) = '8ebbfb3b6687810ad38d0841841f7f85' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_3rd_max_value' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(c_3rd_max_value) FROM epa.pm25_annual) BETWEEN 26.736599607866435 AND 27.27673293327788 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_3rd_max_value' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(c_3rd_max_value) FROM epa.pm25_annual) BETWEEN 378.83833600261426 AND 386.49163571983877 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_4th_max_datetime' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT c_4th_max_datetime) FROM epa.pm25_annual) = '863' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_4th_max_datetime' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(c_4th_max_datetime::varchar, '' order by c_4th_max_datetime)) FROM epa.pm25_annual) = 'cd3726e9d0a84b5136ede5c60a55b09f' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_4th_max_value' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(c_4th_max_value) FROM epa.pm25_annual) BETWEEN 24.918563113145847 AND 25.421968428562938 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_4th_max_value' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(c_4th_max_value) FROM epa.pm25_annual) BETWEEN 301.5608637122657 AND 307.65300237311953 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_50th_percentile' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(c_50th_percentile) FROM epa.pm25_annual) BETWEEN 8.5570488500624 AND 8.729918523801034 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_50th_percentile' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(c_50th_percentile) FROM epa.pm25_annual) BETWEEN 7.9989136370147 AND 8.160507851903885 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_75th_percentile' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(c_75th_percentile) FROM epa.pm25_annual) BETWEEN 12.293092257490358 AND 12.541437555621478 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_75th_percentile' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(c_75th_percentile) FROM epa.pm25_annual) BETWEEN 14.729089827522861 AND 15.02664719777585 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_90th_percentile' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(c_90th_percentile) FROM epa.pm25_annual) BETWEEN 17.001598042124 AND 17.345064669237615 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_90th_percentile' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(c_90th_percentile) FROM epa.pm25_annual) BETWEEN 29.300960948139004 AND 29.89289955315191 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_95th_percentile' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(c_95th_percentile) FROM epa.pm25_annual) BETWEEN 20.569603856422425 AND 20.985151409077424 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_95th_percentile' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(c_95th_percentile) FROM epa.pm25_annual) BETWEEN 46.88119119796214 AND 47.828285969638145 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_98th_percentile' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(c_98th_percentile) FROM epa.pm25_annual) BETWEEN 24.572070186888165 AND 25.068475645209137 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_98th_percentile' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(c_98th_percentile) FROM epa.pm25_annual) BETWEEN 77.3295639205613 AND 78.8917773330979 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_99th_percentile' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(c_99th_percentile) FROM epa.pm25_annual) BETWEEN 27.64407161079798 AND 28.202537703945417 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.c_99th_percentile' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(c_99th_percentile) FROM epa.pm25_annual) BETWEEN 114.68744730457331 AND 117.00436543193842 
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
		WHEN (SELECT MD5(string_agg(cbsa_name::varchar, '' order by cbsa_name)) FROM epa.pm25_annual) = '522e6cba62648a647a254f048b224682' 
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
		WHEN (SELECT MD5(string_agg(certification_indicator::varchar, '' order by certification_indicator)) FROM epa.pm25_annual) = 'ee2b5a527cca5d670dd4aa66b959a36f' 
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
		WHEN (SELECT MD5(string_agg(city_name::varchar, '' order by city_name)) FROM epa.pm25_annual) = '6c23ef42c9425d740f9abb265c94ac01' 
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
		WHEN (SELECT MD5(string_agg(completeness_indicator::varchar, '' order by completeness_indicator)) FROM epa.pm25_annual) = '41e1f9f5ae8c339a95700e01f0f7659a' 
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
		WHEN (SELECT MD5(string_agg(county_code::varchar, '' order by county_code)) FROM epa.pm25_annual) = '4c4d462f07e93f98f283b87200f2cd3b' 
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
		WHEN (SELECT MD5(string_agg(county_name::varchar, '' order by county_name)) FROM epa.pm25_annual) = 'be2922f342a260f39ed8f2cf393cc556' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.date_of_last_change' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT date_of_last_change) FROM epa.pm25_annual) = '82' 
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
		WHEN (SELECT MD5(string_agg(datum::varchar, '' order by datum)) FROM epa.pm25_annual) = '1495bac431dcdc8ab09406883498edd0' 
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
		WHEN (SELECT MD5(string_agg(event_type::varchar, '' order by event_type)) FROM epa.pm25_annual) = 'cfcab13f876ad5e021130fa16dc04ac0' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.exceptional_data_count' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(exceptional_data_count) FROM epa.pm25_annual) BETWEEN 62.73439988134085 AND 64.00176149510531 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.exceptional_data_count' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(exceptional_data_count) FROM epa.pm25_annual) BETWEEN 406905.96114650153 AND 415126.28359390557 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.latitude' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(latitude) FROM epa.pm25_annual) BETWEEN 38.03180284507386 AND 38.800122094469295 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.latitude' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(latitude) FROM epa.pm25_annual) BETWEEN 40.444784078521906 AND 41.261850423542555 
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
		WHEN (SELECT MD5(string_agg(local_site_name::varchar, '' order by local_site_name)) FROM epa.pm25_annual) = '8c09d9aa32cc81416cf34690e3e899d3' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.longitude' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(longitude) FROM epa.pm25_annual) BETWEEN -97.02507246366359 AND -95.1037839000267 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.longitude' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(longitude) FROM epa.pm25_annual) BETWEEN 381.3759916953831 AND 389.08055718417876 
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
		WHEN (SELECT MD5(string_agg(method_name::varchar, '' order by method_name)) FROM epa.pm25_annual) = 'dbd4fab73c64227bb707205dc11a6ac7' 
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
		WHEN (SELECT MD5(string_agg(metric_used::varchar, '' order by metric_used)) FROM epa.pm25_annual) = '324c7584c24e4b25c01f6ba8f77121b8' 
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
		WHEN (SELECT MD5(string_agg(monitor::varchar, '' order by monitor)) FROM epa.pm25_annual) = '14a415660aef3ad3bc94f64bc5788daf' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.null_data_count' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(null_data_count) FROM epa.pm25_annual) BETWEEN 28.526801542568972 AND 29.10310056363097 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.null_data_count' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(null_data_count) FROM epa.pm25_annual) BETWEEN 37478.93926391428 AND 38236.08955207417 
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
		WHEN (SELECT AVG(observation_count) FROM epa.pm25_annual) BETWEEN 397.89894393355087 AND 405.93730643725894 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.observation_count' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(observation_count) FROM epa.pm25_annual) BETWEEN 1738860.0437725543 AND 1773988.5295053332 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.observation_percent' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(observation_percent) FROM epa.pm25_annual) BETWEEN 85.03386354197568 AND 86.7517193711065 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.observation_percent' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(observation_percent) FROM epa.pm25_annual) BETWEEN 419.53451414621753 AND 428.00995887644416 
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
		WHEN (SELECT MD5(string_agg(parameter_code::varchar, '' order by parameter_code)) FROM epa.pm25_annual) = '72ef4cca04aefddbd0fc7402cebe7a85' 
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
		WHEN (SELECT MD5(string_agg(parameter_name::varchar, '' order by parameter_name)) FROM epa.pm25_annual) = 'f465fe43bdd4d0b6ec9474ff6f4d72b6' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.poc' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(poc) FROM epa.pm25_annual) BETWEEN 1.5935152773657668 AND 1.6257075051913379 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.poc' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(poc) FROM epa.pm25_annual) BETWEEN 0.985961227309051 AND 1.0058796359415572 
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
		WHEN (SELECT MD5(string_agg(pollutant_standard::varchar, '' order by pollutant_standard)) FROM epa.pm25_annual) = 'b7dee0347764d9583d5c244f0eaa8bb9' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.primary_exceedance_count' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(primary_exceedance_count) FROM epa.pm25_annual) BETWEEN 3.787693726937269 AND 3.8642127921279212 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.primary_exceedance_count' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(primary_exceedance_count) FROM epa.pm25_annual) BETWEEN 268.9483425542645 AND 274.3816424038456 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.record' As table_column,
	'count distinct' As Testing,
	CASE 
		WHEN (SELECT COUNT(DISTINCT record) FROM epa.pm25_annual) = '16855' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.record' As table_column,
	'MD5 value' As Testing,
	CASE 
		WHEN (SELECT MD5(string_agg(record::varchar, '' order by record)) FROM epa.pm25_annual) = '3951fd3d1486000188c29c2aaa652d24' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.required_day_count' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(required_day_count) FROM epa.pm25_annual) BETWEEN 189.13264253930583 AND 192.95350400474638 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.required_day_count' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(required_day_count) FROM epa.pm25_annual) BETWEEN 16177.51097908606 AND 16504.32938270396 
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
		WHEN (SELECT MD5(string_agg(sample_duration::varchar, '' order by sample_duration)) FROM epa.pm25_annual) = 'cddb8eb9fd5de3c259434f05decfc630' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.secondary_exceedance_count' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(secondary_exceedance_count) FROM epa.pm25_annual) BETWEEN 3.787693726937269 AND 3.8642127921279212 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.secondary_exceedance_count' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(secondary_exceedance_count) FROM epa.pm25_annual) BETWEEN 268.9483425542645 AND 274.3816424038456 
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
		WHEN (SELECT MD5(string_agg(site_num::varchar, '' order by site_num)) FROM epa.pm25_annual) = '14848a342a904e1b783ca8eda84b23a5' 
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
		WHEN (SELECT MD5(string_agg(state_code::varchar, '' order by state_code)) FROM epa.pm25_annual) = 'f78d5325a168b8313201edc6fffddcad' 
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
		WHEN (SELECT MD5(string_agg(state_name::varchar, '' order by state_name)) FROM epa.pm25_annual) = 'a938a15cde90aafce1d9ff68da7f8be8' 
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
		WHEN (SELECT MD5(string_agg(units_of_measure::varchar, '' order by units_of_measure)) FROM epa.pm25_annual) = '43be6a1d9866031f20d2e90b3a70579d' 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.valid_day_count' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(valid_day_count) FROM epa.pm25_annual) BETWEEN 159.28879738949868 AND 162.50675289231683 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.valid_day_count' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(valid_day_count) FROM epa.pm25_annual) BETWEEN 13101.708452468381 AND 13366.389431306128 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.year' As table_column,
	'Mean value' As Testing,
	CASE 
		WHEN (SELECT AVG(year) FROM epa.pm25_annual) BETWEEN 1990.380286561851 AND 2030.5899893206763 
		THEN true ELSE false END AS passed

-- Test case end
UNION ALL
-- Test case start
SELECT 
	'epa.pm25_annual.year' As table_column,
	'Variance' As Testing,
	CASE 
		WHEN (SELECT VARIANCE(year) FROM epa.pm25_annual) BETWEEN 0.2472959999847927 AND 0.2522918787723643 
		THEN true ELSE false END AS passed

-- Test case end

-- --------------------- DRINKS ---------------------
SELECT DISTINCT taxonomy_code, t1.dow, COUNT(DISTINCT t1.dow) 
FROM (
SELECT DISTINCT DAYOFWEEK(load_timestamp) AS dow, data_provider
FROM "TEST_DATA"."PUBLIC"."TEST_TABLE") AS t1
JOIN "TEST_DATA"."PUBLIC"."TEST_TABLE" AS t2 ON t2.data_provider = t1.data_provider
GROUP BY 1,2
;


SELECT COUNT(DISTINCT user_id) , COUNT(*) AS drinks
FROM "TEST_DATA"."PUBLIC"."TEST_TABLE"
WHERE taxonomy_code = 'HOT_DRINKS_COMPANY'
;


-- lookup number of times each user appears in just hot_drinks
SELECT user_id, COUNT(*)
FROM "TEST_DATA"."PUBLIC"."TEST_TABLE"
WHERE taxonomy_code = 'HOT_DRINKS_COMPANY'
GROUP BY 1
LIMIT 10
;


SELECT *
FROM "TEST_DATA"."PUBLIC"."TEST_TABLE"
WHERE user_id = 14465135331660370218
;

-- number of rows distirbution
SELECT count_rows, COUNT(*) AS count_of_users 
FROM (
SELECT user_id, COUNT(*) AS count_rows
FROM "TEST_DATA"."PUBLIC"."TEST_TABLE"
WHERE taxonomy_code = 'HOT_DRINKS_COMPANY'
GROUP BY 1) AS t1
GROUP BY 1
;

-- person with 7 entries
SELECT user_id
FROM (
SELECT user_id, COUNT(*) AS count_rows
FROM "TEST_DATA"."PUBLIC"."TEST_TABLE"
WHERE taxonomy_code = 'HOT_DRINKS_COMPANY'
GROUP BY 1) AS t1
WHERE count_rows = 7
;

-- look into one of the users
SELECT *
FROM "TEST_DATA"."PUBLIC"."TEST_TABLE"
WHERE user_id IN (SELECT user_id
                  FROM (
                        SELECT user_id, COUNT(*) AS count_rows
                        FROM "TEST_DATA"."PUBLIC"."TEST_TABLE"
                        WHERE taxonomy_code = 'HOT_DRINKS_COMPANY'
                        GROUP BY 1) AS t1
                        WHERE count_rows = 6)
AND taxonomy_code = 'HOT_DRINKS_COMPANY'
;

/*user_id
number_of_transactions_drinks -- count num of rows
number_of_days_drinks -- count num of distinct dates from timestamp
number_of_geo_drinks -- count distinct geo_hash */

SELECT *, TO_DATE(load_timestamp)
FROM "TEST_DATA"."PUBLIC"."TEST_TABLE";


-- create user table to show each transaction and what day
CREATE TABLE hot_drinks AS (
SELECT user_id, 
       COUNT(*) as number_of_transactions_drinks, 
       COUNT(DISTINCT TO_DATE(load_timestamp)) AS number_of_days_drinks, 
       COUNT(DISTINCT GEO_DEVICE_HASH) AS number_of_geo_drink
FROM "TEST_DATA"."PUBLIC"."TEST_TABLE"
WHERE taxonomy_code = 'HOT_DRINKS_COMPANY'
GROUP BY 1)
;




-- --------------------- SPORTS ---------------------






-- --------------------- CAREER ---------------------







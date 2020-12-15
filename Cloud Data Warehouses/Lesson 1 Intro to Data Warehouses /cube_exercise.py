!PGPASSWORD=student createdb -h 127.0.0.1 -U student pagila_star
!PGPASSWORD=student psql -q -h 127.0.0.1 -U student -d pagila_star -f Data/pagila-star.sql

import sql
%load_ext sql

DB_ENDPOINT = "127.0.0.1"
DB = 'pagila_star'
DB_USER = 'student'
DB_PASSWORD = 'student'
DB_PORT = '5432'

# postgresql://username:password@host:port/database
conn_string = "postgresql://{}:{}@{}:{}/{}" \
                        .format(DB_USER, DB_PASSWORD, DB_ENDPOINT, DB_PORT, DB)

print(conn_string)
%sql $conn_string


############# CUBE #############
# --  Group by CUBE (dim1, dim2, ..) , produces all combinations of different lenghts in one go.
# -- This view could be materialized in a view and queried which would save lots repetitive aggregations

# TODO: Write a query that calculates the various levels of aggregation done in the grouping sets exercise 
# (total, by month, by country, by month & country) using the CUBE function.
%%time
%%sql
SELECT date.month, store.country, SUM(sales_amount) AS revenue
FROM factSales
JOIN dimStore store ON (store.store_key = factSales.store_key)
JOIN dimDate date ON (date.date_key = factSales.date_key)
GROUP BY CUBE (date.month, store.country);


############# Revenue Total, by Month, by Country, by Month & Country All in one shot, NAIVE way #############
# The naive way to create the same table as above is to write several queries and UNION them together. 
# Grouping sets and cubes produce queries that are shorter to write, easier to read, and more performant. 
# Run the naive query below and compare the time it takes to run to the time it takes the cube query to run.
%%time
%%sql
SELECT  NULL as month, NULL as country, sum(sales_amount) as revenue
FROM factSales
    UNION all 
SELECT NULL, dimStore.country,sum(sales_amount) as revenue
FROM factSales
JOIN dimStore on (dimStore.store_key = factSales.store_key)
GROUP by  dimStore.country
    UNION all 
SELECT cast(dimDate.month as text) , NULL, sum(sales_amount) as revenue
FROM factSales
JOIN dimDate on (dimDate.date_key = factSales.date_key)
GROUP by dimDate.month
    UNION all
SELECT cast(dimDate.month as text),dimStore.country,sum(sales_amount) as revenue
FROM factSales
JOIN dimDate     on (dimDate.date_key         = factSales.date_key)
JOIN dimStore on (dimStore.store_key = factSales.store_key)
GROUP by (dimDate.month, dimStore.country)
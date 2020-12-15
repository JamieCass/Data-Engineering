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


############# Simple Cube #############
# TODO: Write a query that calculates the revenue (sales_amount) by day, rating and city.
%%time
%%sql

SELECT dimDate.day, dimMovie.rating, dimCustomer.city, SUM(sales_amount) AS revenue
FROM factSales
JOIN dimMovie ON (dimMovie.movie_key = factSales.movie_key)
JOIN dimCustomer ON (dimcustomer.customer_key = factSales.customer_key)
JOIN dimDate ON (dimDate.date_key = factSales.date_key)
GROUP BY 1,2,3
ORDER BY 4 DESC
LIMIT 20;


############# Slicing #############
# TODO: Write a query that reduces the dimensionality of the above by limiting the results 
# to only include movies with a rating of 'PG-13'
%%time
%%sql
SELECT dimDate.day, dimMovie.rating, dimCustomer.city, SUM(sales_amount) AS revenue
FROM factSales
JOIN dimMovie ON (dimMovie.movie_key = factSales.movie_key)
JOIN dimCustomer ON (dimcustomer.customer_key = factSales.customer_key)
JOIN dimDate ON (dimDate.date_key = factSales.date_key)
WHERE rating = 'PG-13'
GROUP BY 1,2,3
ORDER BY 4 DESC
LIMIT 20;


############# Dicing #############
# TODO: Write a query to create a subcube of the initial cube that includes movies with:
# ratings of 'PG' or 'PG-13'
# in the city of 'Bellevue' or 'Lancaster'
# day equal to 1, 15 or 30
%%time
%%sql
SELECT dimDate.day, dimMovie.rating, dimCustomer.city, SUM(sales_amount) AS revenue
FROM factSales
JOIN dimMovie ON (dimMovie.movie_key = factSales.movie_key)
JOIN dimCustomer ON (dimcustomer.customer_key = factSales.customer_key)
JOIN dimDate ON (dimDate.date_key = factSales.date_key)
WHERE rating LIKE 'PG%' AND city IN ('Bellevue', 'Lancaster') AND day IN (1,15,30)
GROUP BY 1,2,3
ORDER BY 4 DESC
LIMIT 20;



 
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


############# Roll-up ############# 
# TODO: Write a query that calculates revenue (sales_amount) by day, rating and country
%%time
%%sql
SELECT date.day, movie.rating, customer.country, SUM(sales_amount) AS revenue
FROM factSales fact
JOIN dimDate date ON (date.date_key = fact.date_key)
JOIN dimCustomer customer ON (customer.customer_key = fact.customer_key)
JOIN dimMovie movie ON (movie.movie_key = fact.movie_key)
GROUP BY 1,2,3
ORDER BY 4 DESC
LIMIT 20;


############# Drill-down #############
# TODO: Write a query that calculates revenue (sales_amount) by day, rating and district
%%time
%%sql
SELECT date.day, movie.rating, customer.district, SUM(sales_amount) AS revenue
FROM factSales fact
JOIN dimDate date ON (date.date_key = fact.date_key)
JOIN dimCustomer customer ON (customer.customer_key = fact.customer_key)
JOIN dimMovie movie ON (movie.movie_key = fact.movie_key)
GROUP BY 1,2,3
ORDER BY 4 DESC
LIMIT 20;

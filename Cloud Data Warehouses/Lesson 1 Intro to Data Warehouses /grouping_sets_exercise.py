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


############# Total Revenue #############
# TODO: Write a query that calculates total revenue (sales_amount)
%%sql
SELECT SUM(sales_amount) AS revenue
FROM factSales;


############# Revenue by Country #############
# TODO: Write a query that calculates total revenue (sales_amount) by country
%%sql
SELECT store.country, SUM(sales_amount) AS revenue
FROM factSales
JOIN dimStore store ON (store.store_key = factSales.store_key)
GROUP BY 1
ORDER BY 1,2 DESC;


############# Revenue by Month #############
# TODO: Write a query that calculates total revenue (sales_amount) by month
%%sql
SELECT date.month, SUM(sales_amount) AS revenue
FROM factSales
JOIN dimDate date ON (date.date_key = factSales.date_key)
GROUP BY 1;


############# Revenue by Month & Country #############
# TODO: Write a query that calculates total revenue (sales_amount) by month and country. 
# Sort the data by month, country, and revenue in descending order
%%sql
SELECT date.month, store.country, SUM(sales_amount) AS revenue
FROM factSales
JOIN dimStore store ON (store.store_key = factSales.store_key)
JOIN dimDate date ON (date.date_key = factSales.date_key)
GROUP BY 1,2
ORDER BY 1,2,3 DESC;

############# Revenue Total, by Month, by Country, by Month & Country All in one shot #############
# TODO: Write a query that calculates total revenue at the various grouping levels done above 
# (total, by month, by country, by month & country) all at once using the grouping sets function. 
%%sql
SELECT date.month, store.country, SUM(sales_amount) AS revenue
FROM factSales
JOIN dimStore store ON (store.store_key = factSales.store_key)
JOIN dimDate date ON (date.date_key = factSales.date_key)
GROUP BY grouping sets ((), date.month, store.country, (date.month, store.country)) # This is the grouping sets
ORDER BY 1,2;






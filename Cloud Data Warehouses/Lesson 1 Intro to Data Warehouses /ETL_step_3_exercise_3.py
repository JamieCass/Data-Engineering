########################## Step 3 ##########################
# Perform some simple analysis

!PGPASSWORD=student createdb -h 127.0.0.1 -U student pagila
!PGPASSWORD=student psql -q -h 127.0.0.1 -U student -d pagila -f Data/pagila-schema.sql
!PGPASSWORD=student psql -q -h 127.0.0.1 -U student -d pagila -f Data/pagila-data.sql

%load_ext sql

DB_ENDPOINT = "127.0.0.1"
DB = 'pagila'
DB_USER = 'student'
DB_PASSWORD = 'student'
DB_PORT = '5432'

# postgresql://username:password@host:port/database
conn_string = "postgresql://{}:{}@{}:{}/{}" \
                        .format(DB_USER, DB_PASSWORD, DB_ENDPOINT, DB_PORT, DB)

print(conn_string)
%sql $conn_string


############# 3.1 Insight 1: Top Grossing movies #############
#3.1.1 Films 
%%sql
select film_id, title, release_year, rental_rate, rating  from film limit 5;


# 3.1.2 Payments 
%%sql
select * from payment limit 5;


#3.1.3 Inventory
%%sql
select * from inventory limit 5;


#3.1.4 Get the movie of every payment
%%sql
SELECT f.title, p.amount, p.payment_date, p.customer_id                                            
FROM payment p
JOIN rental r    ON ( p.rental_id = r.rental_id )
JOIN inventory i ON ( r.inventory_id = i.inventory_id )
JOIN film f ON ( i.film_id = f.film_id)
limit 5;


#3.1.5 Sum movie rental revenue
# TODO: Write a query that displays the amount of revenue from each title. 
# Limit the results to the top 10 grossing titles.
%%sql
SELECT f.title, sum(p.amount) AS revenue                    
FROM payment p
JOIN rental r 	 ON (r.rental_id = p.rental_id)
JOIN inventory i ON (i.inventory_id = r.inventory_id)
JOIN film f		 ON (f.film_id = i.film_id)
GROUP BY 1
ORDER BY revenue DESC
LIMIT 10;


############# 3.2 Insight 2: Top grossing cities #############
# 3.2.1 Get the city of each payment
%%sql
SELECT p.customer_id, p.rental_id, p.amount, ci.city                            
FROM payment p
JOIN customer c  ON ( p.customer_id = c.customer_id )
JOIN address a 	 ON ( c.address_id = a.address_id )
JOIN city ci 	 ON ( a.city_id = ci.city_id )
order by p.payment_date
limit 10;


# 3.2.2 Top grossing cities
# TODO: Write a query that returns the total amount of revenue by city as measured by the amount variable in the payment table. 
# Limit the results to the top 10 cities. 
%%sql
SELECT c.city, sum(p.amount) AS revenue
FROM payment p
JOIN customer cu ON (cu.customer_id = p.customer_id)
JOIN address a 	 ON (a.address_id = cu.address_id)
JOIN city c 	 ON (c.city_id = a.city_id)
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;


############# 3.3 Insight 3: Revenue of a movie by customer city and by month #############
# 3.3.1 Total revenue by month
%%sql
SELECT sum(p.amount) as revenue, EXTRACT(month FROM p.payment_date) as month
from payment p
group by month
order by revenue desc
limit 10;


# 3.2.2 Each movie by customer city and by month (data cube)
%%sql
SELECT f.title, p.amount, p.customer_id, ci.city, p.payment_date,EXTRACT(month FROM p.payment_date) as month
FROM payment p
JOIN rental r    ON ( p.rental_id = r.rental_id )
JOIN inventory i ON ( r.inventory_id = i.inventory_id )
JOIN film f ON ( i.film_id = f.film_id)
JOIN customer c  ON ( p.customer_id = c.customer_id )
JOIN address a ON ( c.address_id = a.address_id )
JOIN city ci ON ( a.city_id = ci.city_id )
order by p.payment_date
limit 10;


# 3.3.3 Sum of revenue of each movie by customer city and by month 
# TODO: Write a query that returns the total amount of revenue for each movie by customer city and by month. 
# Limit the results to the top 10 movies.
%%sql
SELECT f.title, c.city, 
       EXTRACT(month from p.payment_date) AS month, 
       sum(p.amount) AS revenue
FROM film f
JOIN inventory i ON (f.film_id = i.film_id)
JOIN rental r 	 ON (i.inventory_id = r.inventory_id)
JOIN payment p 	 ON (r.rental_id = p.rental_id)
JOIN customer cu ON (p.customer_id = cu.customer_id)
JOIN address a 	 ON (cu.address_id = a.address_id)
JOIN city c 	 ON (a.city_id = c.city_id)
GROUP BY 1,2,3
ORDER BY 3,4 DESC
LIMIT 10;






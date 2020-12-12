########################## Step 5 ##########################
# ETL the data from 3NF tables to Facts & Dimension tables

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


############# Populate the dimDate table #############
%%sql
INSERT INTO dimDate (date_key, date, year, quarter, month, day, week, is_weekend)
SELECT DISTINCT(TO_CHAR(payment_date :: DATE, 'yyyyMMDD')::integer) AS date_key,
       date(payment_date)                                           AS date,
       EXTRACT(year FROM payment_date)                              AS year,
       EXTRACT(quarter FROM payment_date)                           AS quarter,
       EXTRACT(month FROM payment_date)                             AS month,
       EXTRACT(day FROM payment_date)                               AS day,
       EXTRACT(week FROM payment_date)                              AS week,
       CASE WHEN EXTRACT(ISODOW FROM payment_date) IN (6, 7) THEN true ELSE false END AS is_weekend
FROM payment;


############# Populate the dimCustomer table #############
%%sql
INSERT INTO dimCustomer (customer_key, customer_id, first_name, last_name, email, address, 
                         address2, district, city, country, postal_code, phone, active, 
                         create_date, start_date, end_date)
SELECT c.customer_id      AS customer_key,
       c.customer_id      AS customer_id,
       c.first_name       AS first_name,
       c.last_name        AS last_name,
       c.email            AS email,
       a.address          AS address,
       a.address2         AS address2,
       a.district         AS district,
       ci.city            AS city,
       co.country         AS country,
       a.postal_code      AS postal_code,
       a.phone            AS phone,
       c.active           AS active,
       c.create_date      AS create_date,
       now()         AS start_date,
       now()         AS end_date
FROM customer c
JOIN address a  ON (c.address_id = a.address_id)
JOIN city ci    ON (a.city_id = ci.city_id)
JOIN country co ON (ci.country_id = co.country_id);


############# Populate the dimMovie table #############
%%sql
INSERT INTO dimMovie (movie_key, film_id, title, description, release_year,
                      language, original_language, rental_duration,
                      length, rating, special_features)
SELECT f.film_id          AS movie_key,
       f.film_id          AS film_id,
       f.title            AS title,
       f.description      AS description,
       f.release_year     AS release_year,
       l.name             AS language,
       orig_lang.name     AS original_language,
       f.rental_duration  AS rental_duration,
       f.length           AS length,
       f.rating           AS rating,
       f.special_features AS special_features
FROM film f
JOIN language l              ON (f.language_id=l.language_id)
LEFT JOIN language orig_lang ON (f.original_language_id = orig_lang.language_id);


############# Populate the dimStore table #############
%%sql
INSERT INTO dimStore (store_key, store_id, address, address2, district,
                      city, country, postal_code, manager_first_name,
                      manager_last_name, start_date, end_date)
SELECT s.store_id          AS store_key,
       s.store_id          AS store_id,
       a.address           AS address,
       a.address2          AS address2,
       a.district          AS district,
       c.city              AS city,
       co.country          AS country,
       a.postal_code       AS postal_code,
       st.first_name       AS manager_first_name,
       st.last_name        AS manager_last_name,
       now()               AS start_date,
       now()               AS end_date
FROM store s
JOIN staff st ON (s.manager_staff_id = st.staff_id)
JOIN address a ON (a.address_id = st.address_id)
JOIN city c ON (c.city_id = a.city_id)
JOIN country co ON (co.country_id = c.country_id)


############# Populate the factSales table #############
%%sql 
INSERT INTO factSales (date_key, customer_key, movie_key, store_key, sales_amount)
SELECT TO_CHAR(p.payment_date :: DATE, 'yyyyMMDD')::integer AS date_key ,
       p.customer_id                                        AS customer_key,
       i.film_id                                            AS movie_key,
       i.store_id                                           AS store_key,
       p.amount                                             AS sales_amount
FROM payment p
JOIN rental r    ON ( p.rental_id = r.rental_id )
JOIN inventory i ON ( r.inventory_id = i.inventory_id );






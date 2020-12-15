%load_ext sql

!sudo -u postgres psql -c 'CREATE DATABASE reviews;'

!wget http://examples.citusdata.com/customer_reviews_1998.csv.gz
!wget http://examples.citusdata.com/customer_reviews_1999.csv.gz

!gzip -d customer_reviews_1998.csv.gz 
!gzip -d customer_reviews_1999.csv.gz 

!mv customer_reviews_1998.csv /tmp/customer_reviews_1998.csv
!mv customer_reviews_1999.csv /tmp/customer_reviews_1999.csv

DB_ENDPOINT = "127.0.0.1"
DB = 'reviews'
DB_USER = 'student'
DB_PASSWORD = 'student'
DB_PORT = '5432'

# postgresql://username:password@host:port/database
conn_string = "postgresql://{}:{}@{}:{}/{}" \
                        .format(DB_USER, DB_PASSWORD, DB_ENDPOINT, DB_PORT, DB)

print(conn_string)

%sql $conn_string


############# STEP 1 #############
# Create a table with a normal (row) storage & load the data
# TODO: Create a table called customer_reviews_row with the column names contained 
# in the customer_reviews_1998.csv and customer_reviews_1999.csv files.
%%sql
DROP TABLE IF EXISTS customer_reviews_row;
CREATE TABLE customer_reviews_row 
(
    customer_id TEXT,
    review_date DATE,
    review_rating INT,
    review_votes INT,
    Review_helpful_notes INT,
    product_id CHAR(10),
    product_title TEXT,
    product_sales_rank BIGINT,
    product_group TEXT,
    product_category TEXT,
    product_subcategoory TEXT,
    similar_product_ids CHAR(10)[]
)
%%sql 
COPY customer_reviews_row FROM '/tmp/customer_reviews_1998.csv' WITH CSV;
COPY customer_reviews_row FROM '/tmp/customer_reviews_1999.csv' WITH CSV;


############# STEP 2 #############
# Create a table with columar storage & load the data
# First load the extension to use columnar storage in Postgres
%%sql

-- load extension first time after install
CREATE EXTENSION cstore_fdw;

-- create server object
CREATE SERVER cstore_server FOREIGN DATA WRAPPER cstore_fdw;

# TODO: Create a FOREIGN TABLE called customer_reviews_col with the column names contained 
# in the customer_reviews_1998.csv and customer_reviews_1999.csv files.
%%sql
-- create foreign table
DROP FOREIGN TABLE IF EXISTS customer_reviews_col;

-------------
CREATE FOREIGN TABLE customer_reviews_col
(
    customer_id TEXT,
    review_date DATE,
    review_rating INT,
    review_votes INT,
    Review_helpful_notes INT,
    product_id CHAR(10),
    product_title TEXT,
    product_sales_rank BIGINT,
    product_group TEXT,
    product_category TEXT,
    product_subcategoory TEXT,
    similar_product_ids CHAR(10)[]
)


-------------
-- leave code below as is
SERVER cstore_server
OPTIONS(compression 'pglz');


%%sql 
COPY customer_reviews_col FROM '/tmp/customer_reviews_1998.csv' WITH CSV;
COPY customer_reviews_col FROM '/tmp/customer_reviews_1999.csv' WITH CSV;


############# STEP 3 #############
# Compare performance
# Run the same query on the two tables and compare the run time. Which form of storage is quicker and more performant


########################## 1.2 s ##########################
%%time
%%sql
SELECT product_title, avg(review_rating)
FROM customer_reviews_row
WHERE review_date BETWEEN '1998-01-01' AND '1999-01-01'
GROUP BY 1
LIMIT 20;


########################## 351 ms ##########################
%%time
%%sql
SELECT product_title, avg(review_rating)
FROM customer_reviews_col
WHERE review_date BETWEEN '1998-01-01' AND '1999-01-01'
GROUP BY 1
LIMIT 20;




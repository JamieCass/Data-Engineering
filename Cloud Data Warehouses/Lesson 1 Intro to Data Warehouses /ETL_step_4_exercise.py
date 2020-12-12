########################## Step 4 ##########################
# Creating Facts and Dimensions

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


############# Create first dimension table #############
# TODO: Create the dimDate dimension table with the fields and data types shown in the ERD above.
%%sql
CREATE TABLE dimDate
(
  date_key integer NOT NULL PRIMARY KEY,
  date date NOT NULL,
  year smallint NOT NULL, 
  quarter smallint NOT NULL,
  month smallint NOT NULL,
  day smallint NOT NULL, 
  week smallint NOT NULL,
  is_weekend boolean NOT NULL
  
);


# Check to see if the table is correct 
%%sql
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name   = 'dimdate'


# create the rest of the dimension tables 
%%sql
CREATE TABLE dimCustomer
(
  customer_key SERIAL PRIMARY KEY,
  customer_id  smallint NOT NULL,
  first_name   varchar(45) NOT NULL,
  last_name    varchar(45) NOT NULL,
  email        varchar(50),
  address      varchar(50) NOT NULL,
  address2     varchar(50),
  district     varchar(20) NOT NULL,
  city         varchar(50) NOT NULL,
  country      varchar(50) NOT NULL,
  postal_code  varchar(10),
  phone        varchar(20) NOT NULL,
  active       smallint NOT NULL,
  create_date  timestamp NOT NULL,
  start_date   date NOT NULL,
  end_date     date NOT NULL
);

CREATE TABLE dimMovie
(
  movie_key          SERIAL PRIMARY KEY,
  film_id            smallint NOT NULL,
  title              varchar(255) NOT NULL,
  description        text,
  release_year       year,
  language           varchar(20) NOT NULL,
  original_language  varchar(20),
  rental_duration    smallint NOT NULL,
  length             smallint NOT NULL,
  rating             varchar(5) NOT NULL,
  special_features   varchar(60) NOT NULL
);
CREATE TABLE dimStore
(
  store_key           SERIAL PRIMARY KEY,
  store_id            smallint NOT NULL,
  address             varchar(50) NOT NULL,
  address2            varchar(50),
  district            varchar(20) NOT NULL,
  city                varchar(50) NOT NULL,
  country             varchar(50) NOT NULL,
  postal_code         varchar(10),
  manager_first_name  varchar(45) NOT NULL,
  manager_last_name   varchar(45) NOT NULL,
  start_date          date NOT NULL,
  end_date            date NOT NULL
);


############# Create the fact table #############
# TODO: Create the factSales table with the fields and data types shown in the ERD picture.
%%sql
CREATE TABLE factSales
(
  sales_key        SERIAL PRIMARY KEY,
  date_key         INT NOT NULL REFERENCES dimDate(date_key),
  customer_key     INT NOT NULL REFERENCES dimCustomer(customer_key),
  movie_key        INT NOT NULL REFERENCES dimMovie(movie_key),
  store_key        INT NOT NULL REFERENCES dimStore(store_key),
  sales_amount     decimal(5,2) NOT NULL
);


# Check to see if the table is correct 
%%sql
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name   = 'factsales'






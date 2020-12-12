########################## Step 1: ##########################
#Connect to the local database where Pagila is loaded 

############# 1.1 Create the Pagila db and fill it with data #############
## Adding '!' at beginning of a jupyter cell runs a comman in a shell. 
## i.e. We arent running python code but we are running the createdb and psql postgresql command-line utilities
!PGPASSWORD=student createdb -h 127.0.0.1 -U student pagila
!PGPASSWORD=student psql -q -h 127.0.0.1 -U student -d pagila -f Data/pagila-schema.sql
!PGPASSWORD=student psql -q -h 127.0.0.1 -U student -d pagila -f Data/pagila-data.sql

############# 1.2 Connect to the newly created db #############
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


########################## Step 2: ##########################
# Explore the 3NF Schema

############# 2.1 How much? What data sizes are we looking at? #############
nStores = %sql select count(*) from store;
nFilms = %sql select count(*) from film;
nCustomers = %sql select count(*) from customer;
nRentals = %sql select count(*) from rental;
nPayment = %sql select count(*) from payment;
nStaff = %sql select count(*) from staff;
nCity = %sql select count(*) from city;
nCountry = %sql select count(*) from country;

print("nFilms\t\t=", nFilms[0][0])
print("nCustomers\t=", nCustomers[0][0])
print("nRentals\t=", nRentals[0][0])
print("nPayment\t=", nPayment[0][0])
print("nStaff\t\t=", nStaff[0][0])
print("nStores\t\t=", nStores[0][0])
print("nCities\t\t=", nCity[0][0])
print("nCountry\t\t=", nCountry[0][0])


############# 2.2 When? What time period are we talking about? #############
%%sql 
select min(payment_date) as start, max(payment_date) as end from payment;


############# 2.3 When? Where do events in this database occur? #############
# TODO: Write a query that displays the number of addresses by district in the address table. 
# Limit the table to the top 10 districts.
%%sql
SELECT district, count(address) as n
FROM address
GROUP BY 1
ORDER BY n DESC
limit 10;





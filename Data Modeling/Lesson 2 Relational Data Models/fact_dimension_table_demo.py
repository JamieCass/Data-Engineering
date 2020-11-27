import psycopg2

try: 
    conn = psycopg2.connect("host=127.0.0.1 dbname=studentdb user=student password=student")
except psycopg2.Error as e: 
    print("Error: Could not make connection to the Postgres database")
    print(e)
try: 
    cur = conn.cursor()
except psycopg2.Error as e: 
    print("Error: Could not get curser to the Database")
    print(e)
conn.set_session(autocommit=True)


# Imagine you work at an online music store. Lets focus on 4 (out of many) tables around purchases.
# customer_transactions, customer, stors, items_purchased

############### CREATE FACT TABLE ###############
try: 
    cur.execute("CREATE TABLE IF NOT EXISTS customer_transactions (customer_id int, store_id int, spent numeric);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)
    
#Insert into all tables 
try: 
    cur.execute("INSERT INTO customer_transactions (customer_id, store_id, spent) \
                 VALUES (%s, %s, %s)", \
                 (1, 1, 20.50))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
try: 
    cur.execute("INSERT INTO customer_transactions (customer_id, store_id, spent) \
                 VALUES (%s, %s, %s)", \
                 (2, 1, 35.21))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)



############### CREATE DIMENSION TABLES ###############
try: 
    cur.execute("CREATE TABLE IF NOT EXISTS items_purchased (customer_id int, item_number int, item_name varchar);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)
    
try: 
    cur.execute("INSERT INTO items_purchased (customer_id, item_number, item_name) \
                 VALUES (%s, %s, %s)", \
                 (1, 1, "Rubber Soul"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO items_purchased (customer_id, item_number, item_name) \
                 VALUES (%s, %s, %s)", \
                 (2, 3, "Let It Be"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("CREATE TABLE IF NOT EXISTS store (store_id int, state varchar);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)
    
try: 
    cur.execute("INSERT INTO store (store_id, state) \
                 VALUES (%s, %s)", \
                 (1, "CA"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
try: 
    cur.execute("INSERT INTO store (store_id, state) \
                 VALUES (%s, %s)", \
                 (2, "WA"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("CREATE TABLE IF NOT EXISTS customer (customer_id int, name varchar, rewards boolean);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)
    
try: 
    cur.execute("INSERT INTO customer (customer_id, name, rewards) \
                 VALUES (%s, %s, %s)", \
                 (1, "Amanda", True))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO customer (customer_id, name, rewards) \
                 VALUES (%s, %s, %s)", \
                 (2, "Toby", False))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)


###### QUERY 1 ######
# Find all the customers that spent more than $30, who are they and what did they buy and if they are a rewards member
try: 
    cur.execute("SELECT name, item_name, rewards FROM ((customer_transactions \
                                                JOIN customer ON customer.customer_id=customer_transactions.customer_id)\
                                                JOIN items_purchased ON \
                                                customer_transactions.customer_id=items_purchased.customer_id)\
                                                WHERE spent > 30 ;")
    
    
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()


###### QUERY 2 ######
# How much did store 1 sell?
try: 
    cur.execute("SELECT store_id, SUM(spent) FROM customer_transactions GROUP BY store_id;")
    
    
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()

cur.close()
conn.close()










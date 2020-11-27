import psycopg2

try: 
    conn = psycopg2.connect("host=127.0.0.1 dbname=studentdb user=student password=student")
except psycopg2.Error as e: 
    print("Error: Could not make connection to the Postgres database")
    print(e)
try: 
    cur = conn.cursor()
except psycopg2.Error as e: 
    print("Error: Could not get cursor to the Database")
    print(e)
conn.set_session(autocommit=True)

# Create the Fact table and insert data into it
try: 
    cur.execute('CREATE TABLE IF NOT EXISTS customer_transactions (customer_id int,\
                                                                   store_id int, spent numeric)')
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)
    
#Insert into all tables 
try: 
    cur.execute('INSERT INTO customer_transactions (customer_id, store_id, spent) \
                 VALUES(%s, %s, %s)',\
                 (1, 1, 20.50))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
try: 
    cur.execute('INSERT INTO customer_transactions (customer_id, store_id, spent) \
                 VALUES(%s, %s, %s)',\
                 (2, 1, 35.21))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

# Create Dimension tables and insert data into them 
try: 
    cur.execute('CREATE TABLE IF NOT EXISTS items_purchased (customer_id int, \
                                                             item_number int, item_name varchar)')
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)
    
try: 
    cur.execute('INSERT INTO items_purchased (customer_id, item_number, item_name)\
                 VALUES(%s, %s, %s)',\
                 (1, 1, 'Rubber Soul'))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute('INSERT INTO items_purchased (customer_id, item_number, item_name)\
                 VALUES(%s, %s, %s)',\
                 (2, 3, 'Let It Be'))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute('CREATE TABLE IF NOT EXISTS customer (customer_id int, \
                                                      name varchar, rewards boolean)')
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)
    
try: 
    cur.execute('INSERT INTO customer (customer_id, name, rewards)\
                 VALUES(%s, %s, %s)',\
                 (1, 'Amanda', True))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
try: 
   cur.execute('INSERT INTO customer (customer_id, name, rewards)\
                VALUES(%s, %s, %s)',\
                (2, 'Toby', False))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute('CREATE TABLE IF NOT EXISTS store (store_id int, state varchar);')
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)
    
try: 
    cur.execute('INSERT INTO store(store_id, state)\
                 VALUES(%s, %s)',\
                 (1, 'CA'))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute('INSERT INTO store(store_id, state)\
                 VALUES(%s, %s)',\
                 (2, 'WA'))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)


###### QUERY 1 ######
# Find all customers that spent more than $30, who they are, which store they bought from, location of store, what they bought and if they are a rewards member 
try: 
    cur.execute("SELECT c.name, s.store_id, s.state, p.item_name, c.rewards \
                 FROM customer c \
                 JOIN items_purchased p ON p.customer_id = c.customer_id JOIN customer_transactions ct ON p.customer_id = ct.customer_id JOIN store s ON s.store_id = ct.store_id WHERE ct.spent > 30")
    
    
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()



###### QUERY 2 ######
# How much did customer 2 spend
try: 
    cur.execute("SELECT c.customer_id, SUM(ct.spent)\
                 FROM customer_transactions ct\
                 JOIN customer c ON c.customer_id = ct.customer_id\
                 WHERE c.customer_id = 2 GROUP BY 1")
    
    
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()

# Drop all the tables 
try: 
    cur.execute("DROP table customer_transactions")
except psycopg2.Error as e: 
    print("Error: Dropping table")
    print (e)
try: 
    cur.execute("DROP table items_purchased")
except psycopg2.Error as e: 
    print("Error: Dropping table")
    print (e)
try: 
    cur.execute("DROP table customer")
except psycopg2.Error as e: 
    print("Error: Dropping table")
    print (e)
try: 
    cur.execute("DROP table store")
except psycopg2.Error as e: 
    print("Error: Dropping table")
    print (e)

cur.close()
conn.close()

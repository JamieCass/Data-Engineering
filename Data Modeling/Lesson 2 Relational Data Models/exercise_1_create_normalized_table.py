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

# TO-DO: Add the CREATE Table Statement and INSERT statements to add the data in the table

try: 
    cur.execute("CREATE TABLE IF NOT EXISTS music_store (transaction_id int,\
                                                         customer_name varchar,\
                                                         casheir_name varchar,\
                                                         year int, albums_purcahsed text[])")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)
    
try: 
    cur.execute("INSERT INTO music_store (transaction_id, customer_name, casheir_name, year, albums_purcahsed) \
                 VALUES (%s, %s, %s, %s, %s)", \
                 (1, 'Amanda', 'Sam', 2000, ['Rubber Soul', 'Let It Be']))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO music_store (transaction_id, customer_name, casheir_name, year, albums_purcahsed) \
                 VALUES (%s, %s, %s, %s, %s)", \
                 (2, 'Toby', 'Sam', 2000, ['My Generation']))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO music_store (transaction_id, customer_name, casheir_name, year, albums_purcahsed) \
                 VALUES (%s, %s, %s, %s, %s)", \
                 (3, 'Max', 'Bob', 2018, ['Meet The Beatles', 'Help!']))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
    
try: 
    cur.execute("SELECT * FROM music_store;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()



############## 1NF ############## 
## TO-DO: Complete the CREATE table statements and INSERT statements

try: 
    cur.execute("CREATE TABLE IF NOT EXISTS music_store2 (transaction_id int,\
                                                         customer_name varchar,\
                                                         casheir_name varchar,\
                                                         year int, album_purcahsed varchar);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)
    
try: 
    cur.execute("INSERT INTO music_store2 (transaction_id, customer_name, casheir_name, year, album_purcahsed) \
                 VALUES (%s, %s, %s, %s, %s)", \
                 (1, 'Amanda', 'Sam', 2000, 'Rubber Soul'))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO music_store2 (transaction_id, customer_name, casheir_name, year, album_purcahsed) \
                 VALUES (%s, %s, %s, %s, %s)", \
                 (1, 'Amanda', 'Sam', 2000, 'Let it Be'))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO music_store2 (transaction_id, customer_name, casheir_name, year, album_purcahsed) \
                 VALUES (%s, %s, %s, %s, %s)", \
                 (2, 'Toby', 'Sam', 2000, 'My Generation'))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO music_store2 (transaction_id, customer_name, casheir_name, year, album_purcahsed) \
                 VALUES (%s, %s, %s, %s, %s)", \
                 (3, 'Max', 'Bob', 2018, 'Meet The Beatles'))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO music_store2 (transaction_id, customer_name, casheir_name, year, album_purcahsed) \
                 VALUES (%s, %s, %s, %s, %s)", \
                 (3, 'Max', 'Bob', 2018, 'Help!'))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("SELECT * FROM music_store2;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()




############## 2NF ############## 
# Two tables (transactions, albums_sold)
try: 
    cur.execute("CREATE TABLE IF NOT EXISTS transactions (transaction_id int, customer_name varchar, casheir_name varchar, year int);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)

try: 
    cur.execute("CREATE TABLE IF NOT EXISTS albums_sold (transaction_id int, casheir_name varchar, album_purcahsed varchar);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)
    
try: 
    cur.execute("INSERT INTO transactions (transaction_id, customer_name, casheir_name, year) \
                 VALUES (%s, %s, %s, %s)", \
                 (1, 'Amanda', 'Sam', 2000))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO transactions (transaction_id, customer_name, casheir_name, year) \
                 VALUES (%s, %s, %s, %s)", \
                 (2, 'Toby', 'Sam', 2000))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO transactions (transaction_id, customer_name, casheir_name, year) \
                 VALUES (%s, %s, %s, %s)", \
                 (3, 'Max', 'Bob', 2018))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO albums_sold (transaction_id, casheir_name, album_purcahsed) \
                 VALUES (%s, %s, %s)", \
                 (1, 'Sam', 'Rubber Soul'))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO albums_sold (transaction_id, casheir_name, album_purcahsed) \
                 VALUES (%s, %s, %s)", \
                 (1, 'Sam', 'Let it Be'))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO albums_sold (transaction_id, casheir_name, album_purcahsed) \
                 VALUES (%s, %s, %s)", \
                 (2, 'Sam','My Generation'))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO albums_sold (transaction_id, casheir_name, album_purcahsed) \
                 VALUES (%s, %s, %s)", \
                 (3, 'Bob', 'Meet The Beatles'))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO albums_sold (transaction_id, casheir_name, album_purcahsed) \
                 VALUES (%s, %s, %s)", \
                 (3, 'Bob', 'Help!'))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

print("Table: transactions\n")
try: 
    cur.execute("SELECT * FROM transactions;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()

print("\nTable: albums_sold\n")
try: 
    cur.execute("SELECT * FROM albums_sold;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)
row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()

############## JOIN both tables ##############
## TO-DO: Complete the join on the transactions and album_sold tables
try: 
    cur.execute("SELECT * FROM transactions JOIN albums_sold ON transactions.transaction_id = albums_sold.transaction_id ;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()




############## 3NF ##############
# another 2 tables (transactions2, employees)
# Cashier name can be move into seperate table, we just need something to use as a foreign key
try: 
    cur.execute("CREATE TABLE IF NOT EXISTS transactions2 (transaction_id int, casheir_id int, customer_name varchar, year int);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)

try: 
    cur.execute("CREATE TABLE IF NOT EXISTS employees (casheir_id int, casheir_name varchar);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)

try: 
    cur.execute("INSERT INTO transactions2 (transaction_id, casheir_id, customer_name, year) \
                 VALUES (%s, %s, %s, %s)", \
                 (1, 1, 'Amanda', 2000))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO transactions2 (transaction_id, casheir_id, customer_name, year) \
                 VALUES (%s, %s, %s, %s)", \
                 (2, 1, 'Toby', 2000))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO transactions2 (transaction_id, casheir_id, customer_name, year) \
                 VALUES (%s, %s, %s, %s)", \
                 (3, 2, 'Max', 2018))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO employees (casheir_id, casheir_name) \
                 VALUES (%s, %s)", \
                 (1, 'Sam'))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO employees (casheir_id, casheir_name) \
                 VALUES (%s, %s)", \
                 (2, 'Bob'))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)    

print("Table: transactions2\n")
try: 
    cur.execute("SELECT * FROM transactions2;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()

print("\nTable: albums_sold\n")
try: 
    cur.execute("SELECT * FROM albums_sold;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()

print("\nTable: employees\n")
try: 
    cur.execute("SELECT * FROM employees;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()



############## JOIN all 3 tables so we can get the same info in the original table ##############
try: 
    cur.execute("SELECT * FROM (transactions2 JOIN albums_sold ON \
                               transactions2.transaction_id = albums_sold.transaction_id) JOIN \
                               employees ON employees.casheir_id = transactions2.casheir_id;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()

cur.close()
conn.close()








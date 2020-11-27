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

# Create normal 3NF database set of tables. 
# 4 tables (transactions2, albums_sold, employees, sales)

# TO-DO: Add all Create statements for all tables
try: 
    cur.execute("CREATE TABLE IF NOT EXISTS transactions2 (transaction_id int, \
                                                           customer_name varchar, \
                                                           employee_id int, year int)")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)

try: 
    cur.execute("CREATE TABLE IF NOT EXISTS albums_sold (album_id int, \
                                                         transaction_id int, \
                                                         album_name varchar)")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)

try: 
    cur.execute("CREATE TABLE IF NOT EXISTS employees (employee_id int, employee_name varchar)")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)

try: 
    cur.execute("CREATE TABLE IF NOT EXISTS sales (transaction_id int, amount_spent int)")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)

      
# TO-DO: Insert data into the tables    
    
try: 
    cur.execute("INSERT INTO transactions2 (transaction_id, customer_name, employee_id, year) \
                 VALUES (%s, %s, %s, %s)", \
                 (1, "Amanda", 1, 2000))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO transactions2 (transaction_id, customer_name, employee_id, year) \
                 VALUES (%s, %s, %s, %s)", \
                 (2, "Toby", 1, 2000))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO transactions2 (transaction_id, customer_name, employee_id, year) \
                 VALUES (%s, %s, %s, %s)", \
                 (3, "Max", 2, 2018))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO albums_sold (album_id, transaction_id, album_name) \
                 VALUES (%s, %s, %s)", \
                 (1, 1, "Rubber Soul"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO albums_sold (album_id, transaction_id, album_name) \
                 VALUES (%s, %s, %s)", \
                 (2, 1, "Let It Be"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO albums_sold (album_id, transaction_id, album_name) \
                 VALUES (%s, %s, %s)", \
                 (3, 2, "My Generation"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO albums_sold (album_id, transaction_id, album_name) \
                 VALUES (%s, %s, %s)", \
                 (4, 3, "Meet the Beatles"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO albums_sold (album_id, transaction_id, album_name) \
                 VALUES (%s, %s, %s)", \
                 (5, 3, "Help!"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO employees (employee_id, employee_name) \
                 VALUES (%s, %s)", \
                 (1, "Sam"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO employees (employee_id, employee_name) \
                 VALUES (%s, %s)", \
                 (2, "Bob"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)    
    
try: 
    cur.execute("INSERT INTO sales (transaction_id, amount_spent) \
                 VALUES (%s, %s)", \
                 (1, 40))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)    
    
try: 
    cur.execute("INSERT INTO sales (transaction_id, amount_spent) \
                 VALUES (%s, %s)", \
                 (2, 19))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e) 

try: 
    cur.execute("INSERT INTO sales (transaction_id, amount_spent) \
                 VALUES (%s, %s)", \
                 (3, 45))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e) 

# print out the tables 
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
    
print("\nTable: sales\n")
try: 
    cur.execute("SELECT * FROM sales;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()

# JOIN the 4 tables with the query that gives us:
# transaction_id, customer_name, cashier_name, year, albums_sold, amount_sold
try: 
    cur.execute("SELECT t.transaction_id, t.customer_name, t.year, a.album_name, s.amount_sold FROM (transactions2 t JOIN albums_sold a ON t.transaction_id = a.transaction_id \
                                JOIN employees e ON t.employee_id = e.employee_id \
                                JOIN sales s ON t.transaction_id = s.transaction_id)")
    
    
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()


################ QUERY 1 ################
# SELECT transaction_id, customer_name, amount_spent FROM <min number of tables>
# basically the transactions table but we just need to add amount_spent

# Create the table..
try: 
    cur.execute("CREATE TABLE IF NOT EXISTS transactions (transaction_id int, \
                               customer_name varchar, employee_id int, \
                               year int, amount_spent int)")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)



#Insert data into all tables 
    
try: 
    cur.execute("INSERT INTO transactions (transaction_id, customer_name, employee_id, year, amount_spent) \
                 VALUES (%s, %s, %s, %s, %s)", \
                 (1, 'Amanda', 1, 2000, 40))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO transactions (transaction_id, customer_name, employee_id, year, amount_spent) \
                 VALUES (%s, %s, %s, %s, %s)", \
                 (2, 'Toby', 1, 2000, 19))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO transactions (transaction_id, customer_name, employee_id, year, amount_spent) \
                 VALUES (%s, %s, %s, %s, %s)", \
                 (3, 'Max', 2, 2018, 45))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

# Print out the query we wanted in QUERY 1 
try: 
    cur.execute("SELECT transaction_id, customer_name, amount_spent FROM transactions")
        
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()



################ QUERY 2 ################
# SELECT cashier_name, SUM(amount_spent) FROM <min number of tables>
# Have a table with just (transaction_id, cashier_name, employee_id, amount_spent)
# Create the table
try: 
    cur.execute("CREATE TABLE IF NOT EXISTS cashier_sales (transaction_id int,\
                                                           cashier_name varchar, \
                                                           employee_id int, amount_spent int)")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)


#Insert into all tables 
    
try: 
    cur.execute("INSERT INTO cashier_sales (transaction_id, cashier_name, employee_id, amount_spent) \
                 VALUES (%s, %s, %s, %s)", \
                 (1, 'Sam', 1, 40))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO cashier_sales (transaction_id, cashier_name, employee_id, amount_spent) \
                 VALUES (%s, %s, %s, %s)", \
                 (2, 'Sam', 1, 19))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO cashier_sales (transaction_id, cashier_name, employee_id, amount_spent) \
                 VALUES (%s, %s, %s, %s)", \
                 (3, 'Bob', 2, 45))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

# Run the query in QUERY 2 
try: 
    cur.execute("SELECT cashier_name, SUM(amount_spent) FROM cashier_sales GROUP BY 1")
        
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()

# Drop all the tables we created!
try: 
    cur.execute("DROP table transactions2")
except psycopg2.Error as e: 
    print("Error: Dropping table")
    print (e)
try: 
    cur.execute("DROP table albums_sold")
except psycopg2.Error as e: 
    print("Error: Dropping table")
    print (e)
try: 
    cur.execute("DROP table employees")
except psycopg2.Error as e: 
    print("Error: Dropping table")
    print (e)
try: 
    cur.execute("DROP table sales")
except psycopg2.Error as e: 
    print("Error: Dropping table")
    print (e)
try: 
    cur.execute("DROP table transactions")
except psycopg2.Error as e: 
    print("Error: Dropping table")
    print (e)
try: 
    cur.execute("DROP table cashier_sales")
except psycopg2.Error as e: 
    print("Error: Dropping table")
    print (e)

cur.close()
conn.close()



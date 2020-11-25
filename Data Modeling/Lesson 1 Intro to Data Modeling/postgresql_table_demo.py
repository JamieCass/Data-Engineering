# start with importing the correct modules
import psycopg2

# Create a connection to local instance of PastgreSQL (127.0.0.1)
# Use the database/schema form the instance
# The connection reaches out to the database (studentdb) and used the correct privilages to connect (user and password = student)
conn = psycopg2.connect('host=127.0.0.1 dbname=studentdb user=student password=student')

# adding a try excepot will make sure errors are caught and understood
# ----- This will be a standard bit of code
try:
	conn = psycopg2.connect('host=127.0.0.1 dbname=studentdb user=student password=student')
except psycopg2.Error as e:
	print('Error: Could not make connection to the Postgres database')
	print(e)

# Use the connection to get a cursor that can be used to execute queries
try:
	cur = conn.cursor()
except psycopg2.Error as e:
	print('Error: Could not get cursor to the database')
	print(e)

# Set up an auto commit so that each action is commited without have to call conn.commit() after every command
# The rollback and commit transactions is a feature of Realtional Databases
conn.set_session(autocommit=True)

# Test connection and Errorhandling code 
# -- this should fail because we havent created a table yet
try: 
    cur.execute("select * from udacity.music_library")
except psycopg2.Error as e:
    print(e)

# Create a database 'udacity' to work in
try: 
    cur.execute("create database udacity")
except psycopg2.Error as e:
    print(e)

# Close connection to the default database and reconnect to the udacity database and get a new cursor
try:
	conn.close()
except psycopg2.Error as e:
	print(e)

try:
	conn = psycopg2.connect('dbname=udacity')
except psycopg2.Error as e:
	print('Error: Could not make connection to the Postgres database')
	print(e)

try:
	cur = conn.cursor()
except psycopg2.Error as e:
	print('Error: Could not get cursor to the database')
	print(e)

conn.set_session(autocommit=True)

# We will create a Music Library of albums
# - Table name : music_library
# - column 1: Album Name
# - columns 2: Artist Name
# - column 3: Year

# The 'IF NOT EXISTS' will check to see if the table already exists (varchar: sting, int: integer)
try:
	cur.execute('CREATE TABLE IF NOT EXISTS music_library (album_name varcher, artist_name varcher, year int);')
except psycopg2.Error as e:
	print('Error: Issue creating table')
	print(e)

# See if we have successfully created the table. 
try: 
    cur.execute("select count(*) from music_library")
except psycopg2.Error as e:
    print(e)

print(curr.fetchall())

# Lets insert two rows
try:
	cur.execute('INSERT INTO music_library (album_name, artist_name, year) \
				 VALUES (%s, %s, %s)', \
				 ('Let It Be', 'The Beatles', 1970))
except psycopg2.Error as e:
	print('Error: Inserting rows')
	print(e)	

try:
	cur.execute('INSERT INTO music_library (album_name, artist_name, year) \
				 VALUES (%s, %s, %s)', \
				 ('Rubber Soul', 'The Beatles', 1965))
except psycopg2.Error as e:
	print('Error: Inserting rows')	
	print(e)

# Validate the data was inserted into the table
try:
	cur.execute('SELECT * FROM music_library')
except psycopg2.Error as e:
	print('Error: select *')
	print(e)

row = cur.fetchone()
while row:
	print(row)
	row = cur.fetchone()

# Finally close cursor and connection
cur.close()
conn.close()
















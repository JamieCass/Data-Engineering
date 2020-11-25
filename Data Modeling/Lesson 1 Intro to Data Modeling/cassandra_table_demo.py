# Import the module again
import cassandra 

# Create a connection to the database (pretty standard for all notebooks)
from cassandra.cluster import Cluster 
try:
	cluster = Cluster(['127.0.0.1'])
	session = cluster.connect()
except Exception as e:
	print(e)

# Test the connection (again it will fail becasue we havent selected a keyspace/database)
try:
	session.execute("""select * from music_library""")
except Exception as e:
	print(e)

# Create keyspace to do our work 
try:
	session.execute('''
	CREATE KEYSPACE IF NOT EXISTS udacity
	WITH REPLICATION = 
	{'class' : 'SimpleStrategy, 'replication_factor : 1} '''
)
except Exception as e:
	print(e)

# Connect to keyspace 
try:
	session.set_keyspace('udacity')
except Exception as e:
	print(e)

# Create a table
query = 'CREATE TABLE IF NOT EXISTS music_library'
query = query + '(year int, artist_name text, album_name text, PRIMARY KEY (year, artist_name))'
try:
	session.execute(query)
except Exception as e:
	print(e)

# Test the table creation
query = 'select count(*) from music_library'
try:
	count = session.execute(query)
except Exception as e:
	print(e)

print(count.one())

# Insert 2 rows
query = 'INSERT INTO music_library (year, artist_name, album_name)'
query = query + 'VALUES (%s, %s, %s)'

try:
	session.execute(query, (1970, 'The Beatles', 'Let It Be'))
except Exception as e:
	print(e)

try:
	session.execute(query, (1965, 'The Beatles', 'Rubber Soul'))
except Exception as e:
	print(e)

# Validate data was inserted into table
query = 'select * from music_library WHERE YEAR = 1970'
try:
	row = session.execute(query)
except Exception as e:
	print(e)

for row in rows:
	print(row.year, row.artist_name, row.album_name)

# Finally close the session and cluster connection
session.shutdown()
cluster.shutdown()









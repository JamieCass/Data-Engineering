import cassandra

from cassandra.cluster import Cluster
try: 
    cluster = Cluster(['127.0.0.1']) #If you have a locally installed Apache Cassandra instance
    session = cluster.connect()
except Exception as e:
    print(e)
 
## TO-DO: Create the keyspace
try:
    session.execute("""
    CREATE KEYSPACE IF NOT EXISTS jamie_db 
    WITH REPLICATION = 
    { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }"""
)

except Exception as e:
    print(e)

## To-Do: Add in the keyspace you created
try:
    session.set_keyspace('jamie_db')
except Exception as e:
    print(e

## TO-DO: Complete the query below
query = "CREATE TABLE IF NOT EXISTS music_library "
query = query + "(song_title text, artist_name text, year int, album_name text, single Boolean, PRIMARY KEY (year, artist_name))"
try:
    session.execute(query)
except Exception as e:
    print(e)

## Add in query and then run the insert statement
query = "INSERT INTO music_library (song_title, artist_name, year, album_name, single)" 
query = query + " VALUES (%s, %s, %s, %s, %s)"

try:
    session.execute(query, ('Across The Univers', 'The Beatles', 1970, 'Let It Be', False))
except Exception as e:
    print(e)
    
try:
    session.execute(query, ('Think For Yourself', 'The Beatles', 1965, 'Rubber Soul', False))
except Exception as e:
    print(e)

## TO-DO: Complete and then run the select statement to validate the data was inserted into the table
query = 'SELECT * FROM music_library'
try:
    rows = session.execute(query)
except Exception as e:
    print(e)
    
for row in rows:
    print (row.year, row.album_name, row.artist_name)

##TO-DO: Complete the select statement to run the query 
query = "select * from music_library WHERE YEAR=1970 AND artist_name='The Beatles'"
try:
    rows = session.execute(query)
except Exception as e:
    print(e)
    
for row in rows:
    print (row.year, row.album_name, row.artist_name)

session.shutdown()
cluster.shutdown()






















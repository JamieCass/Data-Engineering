import cassandra

# Create connection to database
from cassandra.cluster import Cluster
try: 
    cluster = Cluster(['127.0.0.1']) #If you have a locally installed Apache Cassandra instance
    session = cluster.connect()
except Exception as e:
    print(e)

# Create a keyspace to do the work in
try:
    session.execute("""
    CREATE KEYSPACE IF NOT EXISTS udacity 
    WITH REPLICATION = 
    { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }"""
)

except Exception as e:
    print(e)

# Connect to keyspace 
try:
    session.set_keyspace('udacity')
except Exception as e:
    print(e)


# 2 questions to be asked of our data
# 1. Give every album in the music library that was released in a given year
'SELECT * FROM music_library WHERE YEAR=1970'
# 2. Give every album in music library that was created by a given artist
'SELECT * FROM music_library WHERE artist_name="The Beatles"'
# So we need to create 2 different tables
''' 
----- First table -----
Table name: music library
column 1: Year
column 2: Artist name
column 3: Album name
PRIMARY KEY(year, artist name)

----- Second Table -----
Table name: album_library
column 1: Artist name
column 2: Year
column 3: Album name
PRIMARY KEY(artist name, year)
'''

# Create both the tables
query = "CREATE TABLE IF NOT EXISTS music_library "
query = query + "(year int, artist_name text, album_name text, PRIMARY KEY (year, artist_name))"
try:
    session.execute(query)
except Exception as e:
    print(e)
    
query = "CREATE TABLE IF NOT EXISTS album_library "
query = query + "(year int, artist_name text, album_name text, PRIMARY KEY (artist_name,  year))"
try:
    session.execute(query)
except Exception as e:
    print(e)


# Insert some data into both tables
query = "INSERT INTO music_library (year, artist_name, album_name)"
query = query + " VALUES (%s, %s, %s)"

query1 = "INSERT INTO album_library (artist_name, year, album_name)"
query1 = query1 + " VALUES (%s, %s, %s)"

try:
    session.execute(query, (1970, "The Beatles", "Let it Be"))
except Exception as e:
    print(e)
    
try:
    session.execute(query, (1965, "The Beatles", "Rubber Soul"))
except Exception as e:
    print(e)
    
try:
    session.execute(query, (1965, "The Who", "My Generation"))
except Exception as e:
    print(e)

try:
    session.execute(query, (1966, "The Monkees", "The Monkees"))
except Exception as e:
    print(e)

try:
    session.execute(query, (1970, "The Carpenters", "Close To You"))
except Exception as e:
    print(e)
    
try:
    session.execute(query1, ("The Beatles", 1970, "Let it Be"))
except Exception as e:
    print(e)
    
try:
    session.execute(query1, ("The Beatles", 1965, "Rubber Soul"))
except Exception as e:
    print(e)
    
try:
    session.execute(query1, ("The Who", 1965, "My Generation"))
except Exception as e:
    print(e)

try:
    session.execute(query1, ("The Monkees", 1966, "The Monkees"))
except Exception as e:
    print(e)

try:
    session.execute(query1, ("The Carpenters", 1970, "Close To You"))
except Exception as e:
    print(e)


# Validate out data model
# music_library
query = "select * from music_library WHERE YEAR=1970"
try:
    rows = session.execute(query)
except Exception as e:
    print(e)
    
for row in rows:
    print (row.year, row.artist_name, row.album_name)

# album_library
query = "select * from album_library WHERE ARTIST_NAME='The Beatles'"
try:
    rows = session.execute(query)
except Exception as e:
    print(e)
    
for row in rows:
    print (row.artist_name, row.year, row.album_name)


# Drop both tables 
query = "drop table music_library"
try:
    rows = session.execute(query)
except Exception as e:
    print(e)

query = "drop table album_library"
try:
    rows = session.execute(query)
except Exception as e:
    print(e)


# Close session and cluster
session.shutdown()
cluster.shutdown()




import psycopg2

# Create a connection
try: 
    conn = psycopg2.connect("host=127.0.0.1 dbname=studentdb user=student password=student")
except psycopg2.Error as e: 
    print("Error: Could not make connection to the Postgres database")
    print(e)
    
# get a cursor    
try: 
    cur = conn.cursor()
except psycopg2.Error as e: 
    print("Error: Could not get curser to the Database")
    print(e)
    
# set the autocommit to true    
conn.set_session(autocommit=True)


# Create a Table statement
try: 
    cur.execute("CREATE TABLE IF NOT EXISTS music_library (album_id int, \
                                                           album_name varchar, artist_name varchar, \
                                                           year int, songs text[]);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)
    
# Include the Insert statement    
try: 
    cur.execute("INSERT INTO music_library (album_id, album_name, artist_name, year, songs) \
                 VALUES (%s, %s, %s, %s, %s)", \
                 (1, "Rubber Soul", "The Beatles", 1965, ["Michelle", "Think For Yourself", "In My Life"]))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO music_library (album_id, album_name, artist_name, year, songs) \
                 VALUES (%s, %s, %s, %s, %s)", \
                 (2, "Let It Be", "The Beatles", 1970, ["Let It Be", "Across The Universe"]))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
# Confirm the data got inserted in the table we created    
try: 
    cur.execute("SELECT * FROM music_library;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()




############## 1NF ############## 
# same as table above, but each song is in a seperate row (along with duplicate artist_name etc..)
try: 
    cur.execute("CREATE TABLE IF NOT EXISTS music_library2 (album_id int, \
                                                           album_name varchar, artist_name varchar, \
                                                           year int, song_name varchar);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)
    
try: 
    cur.execute("INSERT INTO music_library2 (album_id, album_name, artist_name, year, song_name) \
                 VALUES (%s, %s, %s, %s, %s)", \
                 (1, "Rubber Soul", "The Beatles", 1965, "Michelle"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO music_library2 (album_id, album_name, artist_name, year, song_name) \
                 VALUES (%s, %s, %s, %s, %s)", \
                 (1, "Rubber Soul", "The Beatles", 1965, "Think For Yourself"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO music_library2 (album_id, album_name, artist_name, year, song_name) \
                 VALUES (%s, %s, %s, %s, %s)", \
                 (1, "Rubber Soul", "The Beatles", 1965, "In My Life"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO music_library2 (album_id, album_name, artist_name, year, song_name) \
                 VALUES (%s, %s, %s, %s, %s)", \
                 (2, "Let It Be", "The Beatles", 1970, "Let It Be"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO music_library2 (album_id, album_name, artist_name, year, song_name) \
                 VALUES (%s, %s, %s, %s, %s)", \
                 (2, "Let It Be", "The Beatles", 1970, "Across The Universe"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("SELECT * FROM music_library2;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()

############## 2NF ############## 
# seperate 1NF table into album_library and song_library
try: 
    cur.execute("CREATE TABLE IF NOT EXISTS album_library (album_id int, \
                                                           album_name varchar, artist_name varchar, \
                                                           year int);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)

try: 
    cur.execute("CREATE TABLE IF NOT EXISTS song_library (song_id int, album_id int, \
                                                          song_name varchar);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)
    
try: 
    cur.execute("INSERT INTO album_library (album_id, album_name, artist_name, year) \
                 VALUES (%s, %s, %s, %s)", \
                 (1, "Rubber Soul", "The Beatles", 1965))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO album_library (album_id, album_name, artist_name, year) \
                 VALUES (%s, %s, %s, %s)", \
                 (2, "Let It Be", "The Beatles", 1970))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO song_library (song_id, album_id, song_name) \
                 VALUES (%s, %s, %s)", \
                 (1, 1, "Michelle"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO song_library (song_id, album_id, song_name) \
                 VALUES (%s, %s, %s)", \
                 (2, 1, "Think For Yourself"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO song_library (song_id, album_id, song_name) \
                 VALUES (%s, %s, %s)", \
                 (3, 1, "In My Life"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO song_library (song_id, album_id, song_name) \
                 VALUES (%s, %s, %s)", \
                 (4, 2, "Let It Be"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO song_library (song_id, album_id, song_name) \
                 VALUES (%s, %s, %s)", \
                 (5, 2, "Across the Universe"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

print("Table: album_library\n")
try: 
    cur.execute("SELECT * FROM album_library;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()

print("\nTable: song_library\n")
try: 
    cur.execute("SELECT * FROM song_library;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)
row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()

############## JOIN both tables to get the original 1NF table ##############
try: 
    cur.execute("SELECT * FROM album_library JOIN\
                 song_library ON album_library.album_id = song_library.album_id ;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()


############## 3NF ##############
# split album table again into album_library2, artist_library 
try: 
    cur.execute("CREATE TABLE IF NOT EXISTS album_library2 (album_id int, \
                                                           album_name varchar, artist_id int, \
                                                           year int);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)

try: 
    cur.execute("CREATE TABLE IF NOT EXISTS artist_library (artist_id int, \
                                                           artist_name varchar);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)

    
try: 
    cur.execute("INSERT INTO album_library2 (album_id, album_name, artist_id, year) \
                 VALUES (%s, %s, %s, %s)", \
                 (1, "Rubber Soul", 1, 1965))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO album_library2 (album_id, album_name, artist_id, year) \
                 VALUES (%s, %s, %s, %s)", \
                 (2, "Let It Be", 1, 1970))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO artist_library (artist_id, artist_name) \
                 VALUES (%s, %s)", \
                 (1, "The Beatles"))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    

print("Table: album_library2\n")
try: 
    cur.execute("SELECT * FROM album_library2;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()

print("\nTable: song_library\n")
try: 
    cur.execute("SELECT * FROM song_library;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()

##Doublechecking that data is in the table
print("\nTable: artist_library\n")
try: 
    cur.execute("SELECT * FROM artist_library;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()

############## JOIN all 3 tables to get the same info as table 1NF ##############
try: 
    cur.execute("SELECT * FROM (artist_library JOIN album_library2 ON \
                               artist_library.artist_id = album_library2.artist_id) JOIN \
                               song_library ON album_library2.album_id=song_library.album_id;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()


curr.close()
conn.close()





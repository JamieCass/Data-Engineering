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



################ Create all 3NF Tables ################
# All the same as in the normalization demo, but with an extra table (song_length)
try: 
    cur.execute("CREATE TABLE IF NOT EXISTS album_library (album_id int, \
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
    cur.execute("CREATE TABLE IF NOT EXISTS song_library (song_id int, album_id int, \
                                                          song_name varchar);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)

try: 
    cur.execute("CREATE TABLE IF NOT EXISTS song_length (song_id int, song_length int);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)
    
#Insert into all tables 

try: 
    cur.execute("INSERT INTO song_length (song_id, song_length) \
                 VALUES (%s, %s)", \
                 (1, 163))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO song_length (song_id, song_length) \
                 VALUES (%s, %s)", \
                 (2, 137))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO song_length (song_id, song_length) \
                 VALUES (%s, %s)", \
                 (3, 145))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO song_length (song_id, song_length) \
                 VALUES (%s, %s)", \
                 (4, 240))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO song_length (song_id, song_length) \
                 VALUES (%s, %s)", \
                 (5, 227))
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

    
try: 
    cur.execute("INSERT INTO album_library (album_id, album_name, artist_id, year) \
                 VALUES (%s, %s, %s, %s)", \
                 (1, "Rubber Soul", 1, 1965))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO album_library (album_id, album_name, artist_id, year) \
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



################ Print results ################
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

print("\nTable: song_length\n")
try: 
    cur.execute("SELECT * FROM song_length;")
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()



# If we wanted to do a query to return (artist_id, artist_name, album_id, album_name, year, song_id, song_name, song_length)
# We would need to JOIN 3 tables...
try: 
    cur.execute("SELECT artist_library.artist_id, artist_name, album_library.album_id, \
                        album_name, year, song_library.song_id, song_name, song_length\
                  FROM ((artist_library JOIN album_library ON \
                         artist_library.artist_id = album_library.artist_id) JOIN \
                         song_library ON album_library.album_id=song_library.album_id) JOIN\
                         song_length ON song_library.song_id=song_length.song_id;")
    
    
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()

# This is good flexibility but the JOINs are slow. 



################ QUERY 1 ################
# Want a list of all the songs...
# SELECT artist_name, album_name, year, song_name, song_length FROM <min number of tables>
# To reduce the number of tables needed
# We should just add song_length to song_library table & artist_name to album_library
#Create all Tables
try: 
    cur.execute("CREATE TABLE IF NOT EXISTS album_library1 (album_id int, \
                                                           album_name varchar, artist_name varchar, \
                                                           year int);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)


try: 
    cur.execute("CREATE TABLE IF NOT EXISTS song_library1 (song_id int, album_id int, \
                                                          song_name varchar, song_length int);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)


#Insert into all tables 
    
try: 
    cur.execute("INSERT INTO song_library1 (song_id, album_id, song_name, song_length) \
                 VALUES (%s, %s, %s, %s)", \
                 (2, 1, "Think For Yourself", 137 ))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)
    
try: 
    cur.execute("INSERT INTO song_library1 (song_id, album_id, song_name, song_length) \
                 VALUES (%s, %s, %s, %s)", \
                 (3, 1, "In My Life", 145))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO song_library1 (song_id, album_id, song_name, song_length) \
                 VALUES (%s, %s, %s, %s)", \
                 (4, 2, "Let It Be", 240))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO song_library1 (song_id, album_id, song_name, song_length) \
                 VALUES (%s, %s, %s, %s)", \
                 (5, 2, "Across the Universe", 227))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

    
try: 
    cur.execute("INSERT INTO album_library1 (album_id, album_name, artist_name, year) \
                 VALUES (%s, %s, %s, %s)", \
                 (1, "Rubber Soul", "The Beatles", 1965))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO album_library1 (album_id, album_name, artist_name, year) \
                 VALUES (%s, %s, %s, %s)", \
                 (2, "Let It Be", "The Beatles", 1970))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

# Now we only need to do 1 JOIN to get the information 
try: 
    cur.execute("SELECT artist_name, album_name, year, song_name, song_length\
                  FROM song_library1 JOIN album_library1 ON \
                        song_library1.album_id = album_library1.album_id;")
        
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()


################ QUERY 2 ################
# WE want to knwo the length of each album in seconds
# SELECT album_name SUM(song_length) FROM <min number of tables> GROUP BY album_name
# WE can just create a new to be able to do this.. 
# table name: album_length columns(song_id, album_id, song_length)
try: 
    cur.execute("CREATE TABLE IF NOT EXISTS album_length (song_id int, album_name varchar, \
                                                          song_length int);")
except psycopg2.Error as e: 
    print("Error: Issue creating table")
    print (e)


#Insert into all tables 
    
try: 
    cur.execute("INSERT INTO album_length (song_id, album_name, song_length) \
                 VALUES (%s, %s, %s)", \
                 (1, "Rubber Soul", 163 ))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)

try: 
    cur.execute("INSERT INTO album_length (song_id, album_name, song_length) \
                 VALUES (%s, %s, %s)", \
                 (2, "Rubber Soul", 137 ))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)   

try: 
    cur.execute("INSERT INTO album_length (song_id, album_name, song_length) \
                 VALUES (%s, %s, %s)", \
                 (3, "Rubber Soul", 145 ))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e)   

try: 
    cur.execute("INSERT INTO album_length (song_id, album_name, song_length) \
                 VALUES (%s, %s, %s)", \
                 (4, "Let It Be", 240 ))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e) 
    
try: 
    cur.execute("INSERT INTO album_length (song_id, album_name, song_length) \
                 VALUES (%s, %s, %s)", \
                 (5, "Let It Be", 227 ))
except psycopg2.Error as e: 
    print("Error: Inserting Rows")
    print (e) 

# Run the query
try: 
    cur.execute("SELECT album_name, SUM(song_length) FROM album_length GROUP BY album_name;")
        
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()

cur.close()
conn.close()
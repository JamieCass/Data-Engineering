import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS stage_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS stage_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES
staging_events_table_create = ("""CREATE TABLE IF NOT EXISTS stage_events (
                                  artist  varchar,
                                  auth  varchar, 
                                  first_name varchar, 
                                  gender  varchar, 
                                  item_in_session int,
                                  last_name varchar, 
                                  length decimal, 
                                  level  varchar, 
                                  location varchar, 
                                  method varchar, 
                                  page  varchar,
                                  registration numeric,  
                                  session_id int, 
                                  song varchar,
                                  status numeric,   
                                  ts timestamp, 
                                  user_agent varchar, 
                                  user_id int)
""")


staging_songs_table_create = (""" CREATE TABLE IF NOT EXISTS stage_songs (
                                  num_songs int, 
                                  artist_id varchar,
                                  artist_latitude numeric, 
                                  artist_longitude numeric, 
                                  artist_location varchar,
                                  artist_name varchar, 
                                  song_id varchar, 
                                  title varchar,
                                  duration decimal, 
                                  year int)
""")


songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays (song_id varchar PRIMARY KEY,start_time timestamp NOT NULL,
             													  user_id varchar NOT NULL, level varchar, 
             													  artist_id varchar, 
             				 									  session_id int, location varchar,
             				 									  user_agent varchar);
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users (user_id varchar PRIMARY KEY, first_name varchar, 
         				 									  last_name varchar, gender varchar, 
        				 									  level varchar);
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs (song_id varchar PRIMARY KEY, title varchar,
      													     artist_id varchar, year int, duration numeric);
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (artist_id varchar PRIMARY KEY, name varchar,
          													  location varchar, latitude varchar,
           													  longitude varchar);
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time (start_time timestamp PRIMARY KEY, hour int,
        												    day int, week int, month int, 
        												    year int, weekday int);
""")

# STAGING TABLES

staging_events_copy    = ("""COPY stage_events 
                             FROM {}
                             CREDENTIALS 'aws_iam_role={}'
                             compupdate off
                             FORMAT as json {}
                             TIMEFORMAT 'epochmillisecs'
                             emptyasnull;
                         """).format(config.get('S3', 'LOG_DATA'), config.get('IAM_ROLE', 'ARN'), config.get('S3','LOG_JSONPATH'))

staging_songs_copy     = ("""COPY stage_songs 
                             FROM {} 
                             CREDENTIALS 'aws_iam_role={}'
                             compupdate
                             FORMAT as json 'auto'
                             emptyasnull;
                         """).format(config.get('S3', 'SONG_DATA'), config.get('IAM_ROLE', 'ARN'))

# FINAL TABLES

songplay_table_insert = ("""INSERT INTO songplays (song_id, start_time,user_id, level, artist_id,
                                                  session_id,location, user_agent) 
SELECT songs.song_id,
       ts AS start_time,
       user_id,
       level,
       songs.artist_id,
       session_id,
       location,
       user_agent
FROM stage_events events
JOIN stage_songs songs ON (songs.artist_name = events.artist AND songs.duration = events.length)
WHERE page = 'NextSong'
""")
user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level)
SELECT DISTINCT user_id,
                first_name,
                last_name,
                gender,
                level
FROM stage_events
WHERE page='NextSong';
""")

song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration)
SELECT DISTINCT song_id,
                title,
                artist_id,
                year,
                duration
FROM stage_songs
""")

artist_table_insert = ("""INSERT INTO artists (artist_id, name, location, latitude, longitude)
SELECT DISTINCT artist_id,
                artist_name AS name,
                artist_location AS location,
                artist_latitude AS latitude,
                artist_longitude AS longitude
FROM stage_songs
""")

time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month, year, weekday)
SELECT ts AS start_time,
       EXTRACT(HOUR FROM ts) AS hour,
       EXTRACT(DAY FROM ts) AS day,
       EXTRACT(WEEK FROM ts) AS week,
       EXTRACT(MONTH FROM ts) AS month,
       EXTRACT(YEAR FROM ts) AS year,
       EXTRACT(DOW FROM ts) AS weekday
FROM stage_events
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]


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

staging_events_table_create = ("""CREATE TABLE IF NOT EXISTS stage_events (artist text, auth text, 
                                              first_name text, gender text, item_in_session int,
                                              last_name text, length numeric, level text, 
                                              location text, method text, page text,
                                              registration numeric, session_id int, song text,
                                              status int, ts bigint, user_agent text, user_id int)
""")

staging_songs_table_create = (""" CREATE TABLE IF NOT EXISTS stage_songs (num_songs int, artist_id text,
                                              artist_latitude numeric, artist_longitude numeric, artist_location text,
                                              artist_name text, song_id text, title text,
                                              duration numeric, year int)
""")


songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays (songplay_id varchar PRIMARY KEY, start_time bigint NOT NULL,
             													  user_id varchar NOT NULL, level varchar, 
             													  song_id varchar, artist_id varchar, 
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
          													  location varchar, latitude numeric,
           													  longitude numeric);
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time (start_time timestamp PRIMARY KEY, hour int,
        												    day int, week int, month int, 
        												    year int, weekday int);
""")

# STAGING TABLES

staging_events_copy = (""" COPY stage_events FROM 's3://udacity-dend/log_data'
                           CREDENTIALS 'aws_iam_role={}'
                           gzip region 'us-west-2';
""").format(config.get('IAM_ROLE', 'ARN'))

staging_songs_copy = ("""COPY stage_events FROM 's3://udacity-dend/song_data/A/A/A'
                           CREDENTIALS 'aws_iam_role={}'
                           gzip region 'us-west-2';
""").format(config.get('IAM_ROLE', 'ARN'))

# FINAL TABLES

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")

time_table_insert = ("""
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]

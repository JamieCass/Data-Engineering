import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    '''
    Function to process the song and artist data and insert it into the songs table and artists table

    Tables the information is inserted into:
    songs 
    artists

    Parameters:
    cur: cursor to execute SQL queries
    filepath: location of the file that contains the song information

    Returns: None

    '''
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    try:
        cur.execute(song_table_insert, song_data)
    except pyscopg2.Error as e:
        print('Error inserting song info')
        print(e)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0].tolist()
    try:
        cur.execute(artist_table_insert, artist_data)
    except pyscopg2.Error as e:
        print('Error inserting artist info')
        print(e)


def process_log_file(cur, filepath):
    '''
    Function that process the log data containing all user information and inserts the data into the tables.

    Tables the information is inserted into:
    time
    users
    songplays

    Parameters:
    cur: cursor to execute SQL queries
    filepath: location of the file that contains the song information

    Returns: None

    '''
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = (t, t.dt.hour, t.dt.day, t.dt.weekofyear, t.dt.month, t.dt.year, t.dt.dayofweek)
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    t_data = [values for values in zip(*time_data)]
    time_df = pd.DataFrame(t_data, columns=column_labels)

    for i, row in time_df.iterrows():
        try:
            cur.execute(time_table_insert, list(row))
        except pyscopg2.Error as e:
            print('Error inserting time data records')
            print(e)


    # load user table
    user_df = df.filter(['userId', 'firstName', 'lastName', 'gender', 'level'], axis=1)

    # insert user records
    for i, row in user_df.iterrows():
        try:
            cur.execute(user_table_insert, row)
        except pyscopg2.Error as e:
            print('Error inserting user records')
            print(e)
                

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (index, row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        try:
            cur.execute(songplay_table_insert, songplay_data)
        except pyscopg2.Error as e:
            print('Error inserting songplay records')
            print(e)



def process_data(cur, conn, filepath, func):
    '''
    Function that will walk through all the files and gather all the information ready to be inserted into the tables.

    Parameters:
    cur: cursor to execute SQL queries
    conn: connection to the pyscopg2 database 
    filepath: location of the files that will be used for the data collection
    func: function name - what function will be used either the song or log functions above.

    Returns: None
    '''
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    '''
    Function that will run and start processing the data into the tables.
    '''
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    print('Loading data into staging tables')
    try:
        for query in copy_table_queries:
            cur.execute(query)
            conn.commit()
            
    except psycopg2.Error as e:
        print('Error loading data into staging tables')
        print(e)


def insert_tables(cur, conn):
    print('Loading data into fact & dimension tables')
    try:
        for query in insert_table_queries:
            cur.execute(query)
            conn.commit()
            
    except psycopg2.Error as e:
            print('Error inserting into tables')
            print(e)


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
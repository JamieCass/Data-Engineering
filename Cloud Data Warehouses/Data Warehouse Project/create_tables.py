import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    '''
    Function that will check to see if tables named in the 'drop_table_queries' have been created and if so, will drop them.
    This allows us to re run the code and make changes easily.

    Parameters:
    cur: cursor to execute SQL queries
    conn: connection to our redshift cluster, that we use to commit the changes
    '''
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    '''
    Function that will check to see if tables named in the 'create_table_queries' have been created and if not, will create the specified tables.

    Parameters:
    cur: cursor to execute SQL queries
    conn: connection to our redshift cluster, that we use to commit the changes
    '''
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    '''
    Function that will run from the terminal and execute the code above.
    '''
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    '''
    Function that will start loading data from a S3 bucket into our staging table using the COPY command.
    This bulk load all the data into the two staging tables

    Parameters:
    cur: cursor to execute SQL queries
    conn: connection to our redshift cluster, that we use to commit the changes
    '''
    print('Loading data into staging tables')
    try:
        for query in copy_table_queries:
            cur.execute(query)
            conn.commit()
            
    except psycopg2.Error as e:
        print('Error loading data into staging tables')
        print(e)

# function to get the name for each query being ran.. Got stuck on this during the project
def get_object_name(obj, test_globals = globals()):
    for name in test_globals:
        if test_globals[name] == obj:
            return name

def insert_tables(cur, conn):
    '''
    Function that will start inserting data from the staging tables into fact and dimension analytic tables.

    Parameters:
    cur: cursor to execute SQL queries
    conn: connection to our redshift cluster, that we use to commit the changes
    '''
    print('Loading data into fact & dimension tables')
    try:
        for query in insert_table_queries:
            cur.execute(query)
            conn.commit()
            table_name = get_object_name(query)
            print('Loading {}'.format(table_name))

    except psycopg2.Error as e:
            print('Error loading into fact/dimension tables')
            print(e)


def main():
    '''
    Function that will run from the terminal and execute the code above.
    '''
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()

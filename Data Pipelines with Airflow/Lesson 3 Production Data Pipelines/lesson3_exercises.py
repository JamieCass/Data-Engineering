####################################################################
# LESSON 3
####################################################################
#Instructions
#In this exercise, we’ll consolidate repeated code into Operator Plugins
#1 - Move the data quality check logic into a custom operator
#2 - Replace the data quality check PythonOperators with our new custom operator
#3 - Consolidate both the S3 to RedShift functions into a custom operator
#4 - Replace the S3 to RedShift PythonOperators with our new custom operator
#5 - Execute the DAG

import datetime
import logging

from airflow import DAG
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook

from airflow.operators import (
    HasRowsOperator,
    PostgresOperator,
    PythonOperator,
    S3ToRedshiftOperator
)

import sql_statements


#
# TODO: Replace the data quality checks with the HasRowsOperator
#
# def check_greater_than_zero(*args, **kwargs):
#     table = kwargs["params"]["table"]
#     redshift_hook = PostgresHook("redshift")
#     records = redshift_hook.get_records(f"SELECT COUNT(*) FROM {table}")
#     if len(records) < 1 or len(records[0]) < 1:
#         raise ValueError(f"Data quality check failed. {table} returned no results")
#     num_records = records[0][0]
#     if num_records < 1:
#         raise ValueError(f"Data quality check failed. {table} contained 0 rows")
#     logging.info(f"Data quality on table {table} check passed with {records[0][0]} records")


dag = DAG(
    "lesson3.exercise1",
    start_date=datetime.datetime(2018, 1, 1, 0, 0, 0, 0),
    end_date=datetime.datetime(2018, 12, 1, 0, 0, 0, 0),
    schedule_interval="@monthly",
    max_active_runs=1
)

create_trips_table = PostgresOperator(
    task_id="create_trips_table",
    dag=dag,
    postgres_conn_id="redshift",
    sql=sql_statements.CREATE_TRIPS_TABLE_SQL
)

copy_trips_task = S3ToRedshiftOperator(
    task_id="load_trips_from_s3_to_redshift",
    dag=dag,
    table="trips",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="udac-data-pipelines",
    s3_key="divvy/partitioned/{execution_date.year}/{execution_date.month}/divvy_trips.csv"
)

#
# TODO: Replace this data quality check with the HasRowsOperator
#
check_trips = HasRowsOperator(
    task_id='check_trips_data',
    dag=dag,
    provide_context=True,
    table='trips',
)

create_stations_table = PostgresOperator(
    task_id="create_stations_table",
    dag=dag,
    postgres_conn_id="redshift",
    sql=sql_statements.CREATE_STATIONS_TABLE_SQL,
)

copy_stations_task = S3ToRedshiftOperator(
    task_id="load_stations_from_s3_to_redshift",
    dag=dag,
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="udac-data-pipelines",
    s3_key="divvy/unpartitioned/divvy_stations_2017.csv",
    table="stations"
)

#
# TODO: Replace this data quality check with the HasRowsOperator
#
check_stations = HasRowsOperator(
    task_id='check_stations_data',
    dag=dag,
    provide_context=True,
    table='stations'
)

create_trips_table >> copy_trips_task
create_stations_table >> copy_stations_task
copy_stations_task >> check_stations
copy_trips_task >> check_trips





##################### Exercise 2 #####################
#Instructions
#In this exercise, we’ll refactor a DAG with a single overloaded task into a DAG with several tasks with well-defined boundaries
#1 - Read through the DAG and identify points in the DAG that could be split apart
#2 - Split the DAG into multiple PythonOperators
#3 - Run the DAG

import datetime
import logging

from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook

from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator


#
# TODO: Finish refactoring this function into the appropriate set of tasks,
#       instead of keeping this one large task.
#
# def load_and_analyze(*args, **kwargs):
#     redshift_hook = PostgresHook("redshift")

    # Find all trips where the rider was under 18
    # redshift_hook.run("""
    #     BEGIN;
    #     DROP TABLE IF EXISTS younger_riders;
    #     CREATE TABLE younger_riders AS (
    #         SELECT * FROM trips WHERE birthyear > 2000
    #     );
    #     COMMIT;
    # """)
    # records = redshift_hook.get_records("""
    #     SELECT birthyear FROM younger_riders ORDER BY birthyear DESC LIMIT 1
    # """)
    # if len(records) > 0 and len(records[0]) > 0:
    #     logging.info(f"Youngest rider was born in {records[0][0]}")


    # # Find out how often each bike is ridden
    # redshift_hook.run("""
    #     BEGIN;
    #     DROP TABLE IF EXISTS lifetime_rides;
    #     CREATE TABLE lifetime_rides AS (
    #         SELECT bikeid, COUNT(bikeid)
    #         FROM trips
    #         GROUP BY bikeid
    #     );
    #     COMMIT;
    # """)

    # Count the number of stations by city
    # redshift_hook.run("""
    #     BEGIN;
    #     DROP TABLE IF EXISTS city_station_counts;
    #     CREATE TABLE city_station_counts AS(
    #         SELECT city, COUNT(city)
    #         FROM stations
    #         GROUP BY city
    #     );
    #     COMMIT;
    # """)


def log_oldest():
    redshift_hook = PostgresHook("redshift")
    records = redshift_hook.get_records("""
        SELECT birthyear FROM older_riders ORDER BY birthyear ASC LIMIT 1
    """)
    if len(records) > 0 and len(records[0]) > 0:
        logging.info(f"Oldest rider was born in {records[0][0]}")


def log_u18():
    redshift_hook = PostgresHook('redshift')
    records = redshift_hook.get_records("""
        SELECT birthyear FROM younger_riders ORDER BY birthyear DESC LIMIT 1
    """)
    if len(records) > 0 and len(records[0]) > 0:
        logging.info(f"Youngest rider was born in {records[0][0]}")


dag = DAG(
    "lesson3.exercise2",
    start_date=datetime.datetime.utcnow()
)

load_and_analyze = PythonOperator(
    task_id='load_and_analyze',
    dag=dag,
    python_callable=load_and_analyze,
    provide_context=True,
)

create_oldest_task = PostgresOperator(
    task_id="create_oldest",
    dag=dag,
    sql="""
        BEGIN;
        DROP TABLE IF EXISTS older_riders;
        CREATE TABLE older_riders AS (
            SELECT * FROM trips WHERE birthyear > 0 AND birthyear <= 1945
        );
        COMMIT;
    """,
    postgres_conn_id="redshift"
)

log_oldest_task = PythonOperator(
    task_id="log_oldest",
    dag=dag,
    python_callable=log_oldest
)

log_yougest_task = PythonOperator(
    task_id='log_youngest',
    dag=dag,
    python_callable=log_u18
)

create_under_18_task = PostgresOperator(
    task_id='create_under_18',
    dag=dag,
    sql="""
        BEGIN;
        DROP TABLE IF EXISTS younger_riders;
        CREATE TABLE younger_riders AS (
            SELECT * FROM trips WHERE birthyear > 2000
        );
        COMMIT;
    """,
    postgres_conn_id='redshift'
)

ride_count_task = PostgresOperator(
    task_id='ride_count',
    dag=dag,
    sql="""
        BEGIN;
        DROP TABLE IF EXISTS lifetime_rides;
        CREATE TABLE lifetime_rides AS (
            SELECT bikeid, COUNT(bikeid)
            FROM trips
            GROUP BY bikeid
        );
        COMMIT;
    """
)

station_count_task = PostgresOperator(
    task_id='stations_count',
    dag=dag,
    sql="""
        BEGIN;
        DROP TABLE IF EXISTS city_station_counts;
        CREATE TABLE city_station_counts AS(
            SELECT city, COUNT(city)
            FROM stations
            GROUP BY city
        );
        COMMIT;
    """
)

create_oldest_task >> log_oldest_task
create_under_18_task >> log_youngest




##################### Exercise 3 #####################

##### DAG 
#Instructions
#In this exercise, we’ll place our S3 to RedShift Copy operations into a SubDag.
#1 - Consolidate HasRowsOperator into the SubDag
#2 - Reorder the tasks to take advantage of the SubDag Operators

import datetime

from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.subdag_operator import SubDagOperator
from airflow.operators.udacity_plugin import HasRowsOperator

from lesson3.exercise3.subdag import get_s3_to_redshift_dag
import sql_statements


start_date = datetime.datetime.utcnow()

dag = DAG(
    "lesson3.exercise3",
    start_date=start_date,
)

trips_task_id = "trips_subdag"
trips_subdag_task = SubDagOperator(
    subdag=get_s3_to_redshift_dag(
        "lesson3.exercise3",
        trips_task_id,
        "redshift",
        "aws_credentials",
        "trips",
        sql_statements.CREATE_TRIPS_TABLE_SQL,
        s3_bucket="udac-data-pipelines",
        s3_key="divvy/unpartitioned/divvy_trips_2018.csv",
        start_date=start_date,
    ),
    task_id=trips_task_id,
    dag=dag,
)

stations_task_id = "stations_subdag"
stations_subdag_task = SubDagOperator(
    subdag=get_s3_to_redshift_dag(
        "lesson3.exercise3",
        stations_task_id,
        "redshift",
        "aws_credentials",
        "stations",
        sql_statements.CREATE_STATIONS_TABLE_SQL,
        s3_bucket="udac-data-pipelines",
        s3_key="divvy/unpartitioned/divvy_stations_2017.csv",
        start_date=start_date,
    ),
    task_id=stations_task_id,
    dag=dag,
)

#
# TODO: Consolidate check_trips and check_stations into a single check in the subdag
#       as we did with the create and copy in the demo
#
check_trips = HasRowsOperator(
    task_id="check_trips_data",
    dag=dag,
    redshift_conn_id="redshift",
    table="trips"
)

check_stations = HasRowsOperator(
    task_id="check_stations_data",
    dag=dag,
    redshift_conn_id="redshift",
    table="stations"
)

location_traffic_task = PostgresOperator(
    task_id="calculate_location_traffic",
    dag=dag,
    postgres_conn_id="redshift",
    sql=sql_statements.LOCATION_TRAFFIC_SQL
)

#
# TODO: Reorder the Graph once you have moved the checks
#
trips_subdag_task >> check_trips
stations_subdag_task >> check_stations
check_stations >> location_traffic_task
check_trips >> location_traffic_task


##### SUBDAG 
#Instructions
#In this exercise, we’ll place our S3 to RedShift Copy operations into a SubDag.
#1 - Consolidate HasRowsOperator into the SubDag
#2 - Reorder the tasks to take advantage of the SubDag Operators

import datetime

from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.udacity_plugin import HasRowsOperator
from airflow.operators.udacity_plugin import S3ToRedshiftOperator

import sql


# Returns a DAG which creates a table if it does not exist, and then proceeds
# to load data into that table from S3. When the load is complete, a data
# quality  check is performed to assert that at least one row of data is
# present.
def get_s3_to_redshift_dag(
        parent_dag_name,
        task_id,
        redshift_conn_id,
        aws_credentials_id,
        table,
        create_sql_stmt,
        s3_bucket,
        s3_key,
        *args, **kwargs):
    dag = DAG(
        f"{parent_dag_name}.{task_id}",
        **kwargs
    )

    create_task = PostgresOperator(
        task_id=f"create_{table}_table",
        dag=dag,
        postgres_conn_id=redshift_conn_id,
        sql=create_sql_stmt
    )

    copy_task = S3ToRedshiftOperator(
        task_id=f"load_{table}_from_s3_to_redshift",
        dag=dag,
        table=table,
        redshift_conn_id=redshift_conn_id,
        aws_credentials_id=aws_credentials_id,
        s3_bucket=s3_bucket,
        s3_key=s3_key
    )

    #
    # TODO: Move the HasRowsOperator task here from the DAG
    #

    create_task >> copy_task
    #
    # TODO: Use DAG ordering to place the check task
    #

    return dag



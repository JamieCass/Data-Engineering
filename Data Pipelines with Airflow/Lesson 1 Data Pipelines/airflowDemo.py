import datetime
import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# To start airflow on course 
/opt/airflow/start.sh 

# TODO: Define a function for the PythonOperator to call

def my_function():
	logging.info('Hello world!!')

dag = DAG(
		'lesson1.demo',
		start_date=datetime.datetime.now())



greet_task = PythonOperator(
	task_id='test',
	python_callable=my_function, # this line calls the functions through the python operator
	dag=dag
	)


##################### Data Pipeline Example #####################
# Create a DAG with a start date and interval
divvy_day = DAG(
	'divvy',
	description='Analyzes Divvy Bikeshare data',
	start_date=datetime(2019, 2, 4),
	schedule_interval='@daily'
	)

# Create a function for the DAG to run
def hello_world():
	print('Hello World!!')

# Create the task that the DAG will run (calling the function to run)
task = PythonOperator(
	task_id='hello_world',
	python_callable=hello_world,
	dag=divvy_dag)


##################### Task Dependencies #####################

a >> b # means a comes before b
a << b # means a comes after b

hello_world_task=PythonOperator(task_id='hello_world', ...)
goodbye_world_task=PythonOperator(task_id='goodbye_world', ...)
...
# Use >> to denote that goodbye_world_task depends on hello_world_task
hello_world_task >> goodbye_world_task

# OR
a.set_downstream(b) # means a comes before b
a.set_upstream(b) # means a comes after b
hello_world_task.set_downstream(goodbye_world_task)


##################### Exercise 3 #####################
def hello_world():
    logging.info("Hello World")


def addition():
    logging.info(f"2 + 2 = {2+2}")


def subtraction():
    logging.info(f"6 -2 = {6-2}")


def division():
    logging.info(f"10 / 2 = {int(10/2)}")


dag = DAG(
    "lesson1.exercise3",
    schedule_interval='@hourly',
    start_date=datetime.datetime.now() - datetime.timedelta(days=1))

hello_world_task = PythonOperator(
    task_id="hello_world",
    python_callable=hello_world,
    dag=dag)

#
# TODO: Define an addition task that calls the `addition` function above
addition_task = PythonOperator(
    task_id='addition_task',
    python_callable=addition,
    dag=dag)

#
# TODO: Define a subtraction task that calls the `subtraction` function above
subtraction_task = PythonOperator(
    task_id='subtraction_task',
    python_callable=subtraction,
    dag=dag)

#
# TODO: Define a division task that calls the `division` function above
division_task = PythonOperator(
    task_id='division_task',
    python_callable=division,
    dag=dag)

#
# TODO: Configure the task dependencies such that the graph looks like the following:
#
#                    ->  addition_task
#                   /                 \
#   hello_world_task                   -> division_task
#                   \                 /
#                    ->subtraction_task
hello_world_task >> addition_task
hello_world_task >> subtraction_task
addition_task >> division_task
subtraction_task >> division_task



##################### Hooks #####################
from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python_operator import PythonOperator

def load():
# Create a PostgresHook option using the `demo` connection
    db_hook = PostgresHook(‘demo’)
    df = db_hook.get_pandas_df('SELECT * FROM rides')
    print(f'Successfully used PostgresHook to return {len(df)} records')

load_task = PythonOperator(task_id=’load’, python_callable=hello_world, ...)


##################### Connections #####################
import datetime
import logging

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.S3_hook import S3Hook

#
# TODO: There is no code to modify in this exercise. We're going to create a connection and a
# variable.
# 1. Open your browser to localhost:8080 and open Admin->Variables
# 2. Click "Create"
# 3. Set "Key" equal to "s3_bucket" and set "Val" equal to "udacity-dend"
# 4. Set "Key" equal to "s3_prefix" and set "Val" equal to "data-pipelines"
# 5. Click save
# 6. Open Admin->Connections
# 7. Click "Create"
# 8. Set "Conn Id" to "aws_credentials", "Conn Type" to "Amazon Web Services"
# 9. Set "Login" to your aws_access_key_id and "Password" to your aws_secret_key
# 10. Click save
# 11. Run the DAG

def list_keys():
    hook = S3Hook(aws_conn_id='aws_credentials')
    bucket = Variable.get('s3_bucket')
    prefix = Variable.get('s3_prefix')
    logging.info(f"Listing Keys from {bucket}/{prefix}")
    keys = hook.list_keys(bucket, prefix=prefix)
    for key in keys:
        logging.info(f"- s3://{bucket}/{key}")


dag = DAG(
        'lesson1.exercise4',
        start_date=datetime.datetime.now())

list_task = PythonOperator(
    task_id="list_keys",
    python_callable=list_keys,
    dag=dag
)



##################### Runtime Variables #####################
# Instructions
# Use the Airflow context in the pythonoperator to complete the TODOs below. Once you are done, run your DAG and check the logs to see the context in use.

import datetime
import logging

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.S3_hook import S3Hook


def log_details(*args, **kwargs):
    #
    # TODO: Extract ds, run_id, prev_ds, and next_ds from the kwargs, and log them
    # NOTE: Look here for context variables passed in on kwargs:
    #       https://airflow.apache.org/macros.html
    #
    ds = {kwargs['ds']}
    run_id = {kwargs['run_id']}
    previous_ds = {kwargs.get('prev_ds')}
    next_ds = {kwargs.get('next_ds')}

    logging.info(f"Execution date is {ds}")
    logging.info(f"My run id is {run_id}")
    if previous_ds:
        logging.info(f"My previous run was on {previous_ds}")
    if next_ds:
        logging.info(f"My next run will be {next_ds}")

dag = DAG(
    'lesson1.exercise5',
    schedule_interval="@daily",
    start_date=datetime.datetime.now() - datetime.timedelta(days=2)
)

list_task = PythonOperator(
    task_id="log_details",
    python_callable=log_details,
    provide_context=True,
    dag=dag
)




##################### S3 to Redshift Exercise #####################
# Instructions
# Similar to what you saw in the demo, copy and populate the trips table. Then, add another operator which creates a traffic analysis table from the trips table you created. Note, in this class, we won’t be writing SQL -- all of the SQL statements we run against Redshift are predefined and included in your lesson.

import datetime
import logging

from airflow import DAG
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator

import sql_statements


def load_data_to_redshift(*args, **kwargs):
    aws_hook = AwsHook("aws_credentials")
    credentials = aws_hook.get_credentials()
    redshift_hook = PostgresHook("redshift")
    redshift_hook.run(sql_statements.COPY_ALL_TRIPS_SQL.format(credentials.access_key, credentials.secret_key))


dag = DAG(
    'lesson1.exercise6',
    start_date=datetime.datetime.now()
)

create_table = PostgresOperator(
    task_id="create_table",
    dag=dag,
    postgres_conn_id="redshift",
    sql=sql_statements.CREATE_TRIPS_TABLE_SQL
)

copy_task = PythonOperator(
    task_id='load_from_s3_to_redshift',
    dag=dag,
    python_callable=load_data_to_redshift
)

location_traffic_task = PostgresOperator(
    task_id="calculate_location_traffic",
    dag=dag,
    postgres_conn_id="redshift",
    sql=sql_statements.LOCATION_TRAFFIC_SQL
)

create_table >> copy_task
copy_task >> location_traffic_task



####################################################################
# LESSON 2 
####################################################################



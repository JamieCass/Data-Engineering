import datetime
import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator 


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
a << b # means b comes before a

hello_world_task=PythonOperator(task_id='hello_world', ...)
goodbye_world_task=PythonOperator(task_id='goodbye_world', ...)
...
# Use >> to denote that goodbye_world_task depends on hello_world_task
hello_world_task >> goodbye_world_task

# OR
a.set_downstream(b) # means a comes before b 
a.set_upstream(b) 
hello_world_task.set_downstream(goodbye_world_task)










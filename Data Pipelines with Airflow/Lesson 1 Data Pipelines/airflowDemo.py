import datetime
import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator 


# TODO: Define a function for the PythonOperator to call

dag = DAG(
		'lesson1.demo',
		start_date=datetime.datetime.now())


# TODO: Uncomment the operator below and replace the arguments labeled <REPLACE>

greet_task = PythonOperator(
	task_id='<REPLACE>',
	python_callable=<REPLACE>,
	dag=<REPLACE>)




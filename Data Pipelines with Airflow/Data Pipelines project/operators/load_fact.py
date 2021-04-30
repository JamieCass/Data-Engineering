from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 # Example:
                 # conn_id = your-connection-name
                 redshift_conn_id='',
                 table='',
                 sql_statement='',
                 append_data='',
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        # self.conn_id = conn_id
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql_statement = sql_statement
        self.append_data = append_data 

    def execute(self, context):
        self.log.info('LoadFactOperator Running')
        redshift_hook = PostgresHook('redshift')
        self.log.info('Appending data')
        if self.append_data == True:
            sql_statement = f'INSERT INTO {self.table} {self.sql_statement}'
            redshift_hook.run(sql_statement)
        else:
            sql_statement = f'DELETE FROM {self.table}'
            redhsift_hook.run(sql_statement)
        sql_statement = f'INSERT INTO {self.table} {self.sql_statement}'
            redshift_hook.run(sql_statement)

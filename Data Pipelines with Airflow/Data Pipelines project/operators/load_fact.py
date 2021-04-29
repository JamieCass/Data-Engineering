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
                 table_columns='',
                 sql_to_load_tbl=''
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        # self.conn_id = conn_id
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.table_columns = table_columns
        self.sql_to_load_tbl = sql_to_load_tbl

    def execute(self, context):
        self.log.info('LoadFactOperator Running')
        redshift = PostgresHook('redshift')
        sql_statement = "INSERT INTO {} {} {}".format(self.table, self.table_columns,self.sql_to_load_tbl)
        redshift.run(sql_statement)

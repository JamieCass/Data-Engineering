import boto3
import json
import configparser
import psycopg2
import pandas as pd
import sql

config = configparser.ConfigParser()
config.read_file(open('/Users/jamie/Coding/keys/dwh.cfg'))

KEY                    = config.get('AWS','KEY')
SECRET                 = config.get('AWS','SECRET')

DWH_CLUSTER_TYPE       = config.get("DWH","DWH_CLUSTER_TYPE")
DWH_NUM_NODES          = config.get("DWH","DWH_NUM_NODES")
DWH_NODE_TYPE          = config.get("DWH","DWH_NODE_TYPE")

DWH_CLUSTER_IDENTIFIER = config.get("DWH","DWH_CLUSTER_IDENTIFIER")
DWH_DB                 = config.get("DWH","DWH_DB")
DWH_DB_USER            = config.get("DWH","DWH_DB_USER")
DWH_DB_PASSWORD        = config.get("DWH","DWH_DB_PASSWORD")
DWH_PORT               = config.get("DWH","DWH_PORT")

DWH_IAM_ROLE_NAME      = config.get("DWH", "DWH_IAM_ROLE_NAME")
DWH_ARN                = config.get('DWH', 'DWH_ARN')

(DWH_DB_USER, DWH_DB_PASSWORD, DWH_DB)

pd.DataFrame({"Param":
                  ["DWH_CLUSTER_TYPE", "DWH_NUM_NODES", "DWH_NODE_TYPE", "DWH_CLUSTER_IDENTIFIER", "DWH_DB", "DWH_DB_USER", "DWH_DB_PASSWORD", "DWH_PORT", "DWH_IAM_ROLE_NAME", 'DWH_ARN'],
              "Value":
                  [DWH_CLUSTER_TYPE, DWH_NUM_NODES, DWH_NODE_TYPE, DWH_CLUSTER_IDENTIFIER, DWH_DB, DWH_DB_USER, DWH_DB_PASSWORD, DWH_PORT, DWH_IAM_ROLE_NAME, DWH_ARN]
             })

##########################################
# Create clients for redshift, ec2, IAM and s3
##########################################
redshift = boto3.client('redshift',
                        region_name = 'us-west-2',
                        aws_access_key_id = KEY,
                        aws_secret_access_key = SECRET
                        )

ec2 = boto3.resource('ec2',
                     region_name = 'us-west-2',
                     aws_access_key_id = KEY,
                     aws_secret_access_key = SECRET
                     )

s3 = boto3.resource('s3',
                    region_name = 'us-west-2',
                    aws_access_key_id = KEY,
                    aws_secret_access_key = SECRET
                    )

iam = boto3.client('iam',
                  region_name='us-west-2',
                  aws_access_key_id=KEY,
                  aws_secret_access_key=SECRET
                  )

##########################################
# Sample data in s3 bucket
##########################################
sampleDbBucket = s3.Bucket('awssampledbuswest2')
for x in sampleDbBucket.objects.filter(Prefix='ssbgz'):
    print(x)

# Create a redshift cluster
try:
    response = redshift.create_cluster(
        # Hardware
        ClusterType = DWH_CLUSTER_TYPE,
        NodeType = DWH_NODE_TYPE,
        NumberOfNodes = int(DWH_NUM_NODES),

        # Identifiers and clients
        DBName = DWH_DB,
        ClusterIdentifier = DWH_CLUSTER_IDENTIFIER,
        MasterUsername = DWH_DB_USER,
        MasterUserPassword = DWH_DB_PASSWORD,

        # Role to allow S3 access
        IamRoles =[DWH_ARN]
    )
except Exception as e:
    print(e)

##########################################
# See clusters status
##########################################
def prettyRedshiftProps(props):
    pd.set_option('display.max_colwidth', -1)
    keysToShow = ["ClusterIdentifier", "NodeType", "ClusterStatus", "MasterUsername", "DBName", "Endpoint", "NumberOfNodes", 'VpcId']
    x = [(k, v) for k,v in props.items() if k in keysToShow]
    return pd.DataFrame(data=x, columns=["Key", "Value"])

myClusterProps = redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)['Clusters'][0]
prettyRedshiftProps(myClusterProps)

##########################################
# Get endpoint
##########################################
DWH_ENDPOINT = myClusterProps['Endpoint']['Address']
DWH_ENDPOINT

##########################################
# Check security group
##########################################
try:
    vpc = ec2.Vpc(id=myClusterProps['VpcId'])
    defaultSg = list(vpc.security_groups.all())[0]
    print(defaultSg)

except Exception as e:
    print(e)

##########################################
# Connect to cluster
##########################################
conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(DWH_ENDPOINT, DWH_DB, DWH_DB_USER, DWH_DB_PASSWORD, DWH_PORT))
cur = conn.cursor()

##########################################
# Check to see if you can execute the query
##########################################
staging_events_table_create = ("""CREATE TABLE IF NOT EXISTS stage_events (
                                  artist  varchar,
                                  auth  varchar,
                                  first_name varchar,
                                  gender  varchar,
                                  item_in_session int,
                                  last_name varchar,
                                  length decimal,
                                  level  varchar,
                                  location varchar,
                                  method varchar,
                                  page  varchar,
                                  registration numeric,
                                  session_id int,
                                  song varchar,
                                  status numeric,
                                  ts timestamp,
                                  user_agent varchar,
                                  user_id int)
""")

cur.execute(staging_events_table_create)
conn.commit()

##########################################
# Delete the cluster
##########################################
redshift.delete_cluster(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,  SkipFinalClusterSnapshot=True)

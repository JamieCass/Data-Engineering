##########################################
# Example of IaC
##########################################
import pandas as pd
import boto3
import json
import configparser

config = configparser.ConfigParser()
config.read_file(open('dwh.cfg')) # will need to change this to my own file location

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

(DWH_DB_USER, DWH_DB_PASSWORD, DWH_DB)

pd.DataFrame({"Param":
                  ["DWH_CLUSTER_TYPE", "DWH_NUM_NODES", "DWH_NODE_TYPE", "DWH_CLUSTER_IDENTIFIER", "DWH_DB", "DWH_DB_USER", "DWH_DB_PASSWORD", "DWH_PORT", "DWH_IAM_ROLE_NAME"],
              "Value":
                  [DWH_CLUSTER_TYPE, DWH_NUM_NODES, DWH_NODE_TYPE, DWH_CLUSTER_IDENTIFIER, DWH_DB, DWH_DB_USER, DWH_DB_PASSWORD, DWH_PORT, DWH_IAM_ROLE_NAME]
             })


##########################################
# Create clients for EC2, S3, IAM and Redshift
##########################################
ec2 = boto3.resource('ec2',
                  region_name='us-west-2',
                  aws_access_key_id=KEY,
                  aws_secret_access_key=SECRET
                  )

s3 = boto3.resource('s3',
                 region_name='us-west-2',
                 aws_access_key_id=KEY,
                 aws_secret_access_key=SECRET
                 )

iam = boto3.client('iam',
                  region_name='us-west-2',
                  aws_access_key_id=KEY,
                  aws_secret_access_key=SECRET
                  )

redshift = boto3.client('redshift',
                       region_name='us-west-2',
                       aws_access_key_id=KEY,
                       aws_secret_access_key=SECRET
                       )

##########################################
# Check the sample data source on S3
##########################################
sampleDbBucket =  s3.Bucket("awssampledbuswest2")

# TODO: Iterate over bucket objects starting with "ssbgz" and print
for x in sampleDbBucket.objects.filter(Prefix = 'ssbgz'):
    print(x)


##########################################
# Step 1:      IAM Role
##########################################
# Create IAM role that makes Redshift able to access S3 bucket (readonly)
# TODO: Create the IAM role
try:
    print('1.1 Creating a new IAM Role')
    dwhRole = iam.create_role(
    Path='/',
    RoleName=DWH_IAM_ROLE_NAME,
    Description='Allows Redshift cluster to call AWS services on your behalf.',
    AssumeRolePolicyDocument=json.dumps(
        {'Statement' : [{'Action' : 'sts:AssumeRole',
                         'Effect' : 'Allow',
                         'Principal' : {'Service' : 'redshift.amazonaws.com'}}],
         'Version' : '2012-10-17'})
    )
    

except Exception as e:
    print(e)

# TODO: Attach Policy
try:
    print('1.2 Attaching Policy')
    iam.attach_role_policy(RoleName=DWH_IAM_ROLE_NAME,
                           PolicyArn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
                          )['ResponseMetadata']['HTTPStatusCode']
except Exception as e:
    print(e)

# TODO: Get and print the IAM role ARN
print('1.3 Get the IAM role ARN')
roleArn = iam.get_role(RoleName=DWH_IAM_ROLE_NAME)['Role']['Arn']

print(roleArn)


##########################################
# Step 2:      Redshift Cluster
##########################################
# Create a Redshift cluster
try:
    response = redshift.create_cluster(        
        # HW
        ClusterType=DWH_CLUSTER_TYPE,
        NodeType=DWH_NODE_TYPE,
        NumberOfNodes=int(DWH_NUM_NODES),
        
        # Identifiers & Credentials
        DBName=DWH_DB,
        ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,
        MasterUsername=DWH_DB_USER,
        MasterUserPassword=DWH_DB_PASSWORD,
        
        # Role (to allow s3 access)
        IamRoles=[roleArn]
    )
except Exception as e:
    print(e)


##########################################
# Step 2.1: Describe cluster to see its status
##########################################
def prettyRedshiftProps(props):
    pd.set_option('display.max_colwidth', -1)
    keysToShow = ["ClusterIdentifier", "NodeType", "ClusterStatus", "MasterUsername", "DBName", "Endpoint", "NumberOfNodes", 'VpcId']
    x = [(k, v) for k,v in props.items() if k in keysToShow]
    return pd.DataFrame(data=x, columns=["Key", "Value"])

myClusterProps = redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)['Clusters'][0]
prettyRedshiftProps(myClusterProps)


#!!!!!!!!!! DONT RUN UNTIL CLUSTER IS AVAILABLE !!!!!!!!!!
DWH_ENDPOINT = myClusterProps['Endpoint']['Address']
DWH_ROLE_ARN = myClusterProps['IamRoles'][0]['IamRoleArn']
print("DWH_ENDPOINT :: ", DWH_ENDPOINT)
print("DWH_ROLE_ARN :: ", roleArn)


##########################################
# Step 3: Open incoming TCP port to access cluster endpoint
##########################################
try:
    vpc = ec2.Vpc(id=myClusterProps['VpcId'])
    defaultSg = list(vpc.security_groups.all())[0]
    print(defaultSg)
    
    defaultSg.authorize_ingress(
        GroupName=defaultSg.group_name,  # TODO: fill out
        CidrIp='0.0.0.0/0',  # TODO: fill out
        IpProtocol='TCP',  # TODO: fill out
        FromPort=int(DWH_PORT),
        ToPort=int(DWH_PORT)
    )
except Exception as e:
    print(e)



##########################################
# Step 4: Make sure you can connect to cluster
##########################################
%load_ext sql
conn_string="postgresql://{}:{}@{}:{}/{}".format(DWH_DB_USER, DWH_DB_PASSWORD, DWH_ENDPOINT, DWH_PORT, DWH_DB)
print(conn_string)
%sql $conn_string


##########################################
# Step 5: Clean up resources
##########################################
#### CAREFUL!!
#-- Uncomment & run to delete the created resources
redshift.delete_cluster( ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,  SkipFinalClusterSnapshot=True)
#### CAREFUL!!

#### CAREFUL!!
#-- Uncomment & run to delete the created resources
iam.detach_role_policy(RoleName=DWH_IAM_ROLE_NAME, PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess")
iam.delete_role(RoleName=DWH_IAM_ROLE_NAME)
#### CAREFUL!!



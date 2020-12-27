##########################################
# Create Redshift cluster
##########################################

redshift = boto3.client('redshift',
						region_name='us-west-2',
						aws_access_key_id=KEY,
						aws_secret_access_key=SECRET
						)

response = redshift.create.cluster(
	# HW
	ClusterType=DWH_CLUSTER_TYPE,
	NodeType=DWH_NODE_TYPE,
	NumberOfNodes=int(DWH_NUM_N
	# Identifiers & Credentials 
	DBName=DWH_DB,
	ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,
	MasterUsername=DWH_DB_USER,
	MasterUserPassword=DWH_DB_PA
	# Roles (for S3 access)
	IamRoles=[roleArn]
)

##########################################
# Create new IAM role and Attaching Policy
##########################################
# Create IAM role
dwhRole = iam.create_role(
	Path='/',
	RoleName=DWH_IAM_ROLE_NAME,
	Description='Allows Redshift cluster to call AWS services on your behalf',
	AssumeRolePolicyDocuments=json.dumps(
		{'Statment' : [{'Action': 'sts:AssumeRole',
			'Effect' : 'Allow',
			'Principal' : {'Service' : 'redshift.amazonaws.com'}}],
		 'Version' : '2012-10-17'})
)
# Attach policy to IAM role
iam.attach_role_policy(RoleName=DWH_IAM_ROLE_NAME,
	PolicyArn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
	)['ResponseMetadata']['HTTPStatusCode']


##########################################
# E.g. Open an incoming TCP port to access the cluster endpoint
##########################################
vpc = ec2.Vpc(id=myClusterProps['VpcId'])
defaultSg = list(vpc.security_groups.all())[0]
defaultSg.authorize_ingress(
	GroupName=defaultSg.group_name,
	CidrIp='0.0.0.0/0',
	IpProtocol='TCP',
	FromPort=int(DWH_PORT),
	ToPort=int(DWH_PORT)
)





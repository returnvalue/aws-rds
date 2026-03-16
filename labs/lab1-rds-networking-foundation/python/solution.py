import boto3

ec2 = boto3.client('ec2', endpoint_url="http://localhost:4566", region_name="us-east-1")
rds = boto3.client('rds', endpoint_url="http://localhost:4566", region_name="us-east-1")

vpc_response = ec2.create_vpc(CidrBlock='10.0.0.0/16')
vpc_id = vpc_response['Vpc']['VpcId']

subnet_a_response = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.0.1.0/24', AvailabilityZone='us-east-1a')
subnet_a = subnet_a_response['Subnet']['SubnetId']

subnet_b_response = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.0.2.0/24', AvailabilityZone='us-east-1b')
subnet_b = subnet_b_response['Subnet']['SubnetId']

rds.create_db_subnet_group(
    DBSubnetGroupName='my-db-subnets',
    DBSubnetGroupDescription='Primary DB Subnet Group',
    SubnetIds=[subnet_a, subnet_b]
)

rds.create_db_instance(
    DBInstanceIdentifier='primary-db',
    DBInstanceClass='db.t3.micro',
    Engine='postgres',
    MasterUsername='dbadmin',
    MasterUserPassword='supersecret123',
    AllocatedStorage=20,
    DBSubnetGroupName='my-db-subnets',
    MultiAZ=False
)

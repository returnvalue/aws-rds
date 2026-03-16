import boto3
import json

secretsmanager = boto3.client('secretsmanager', endpoint_url="http://localhost:4566", region_name="us-east-1")
iam = boto3.client('iam', endpoint_url="http://localhost:4566", region_name="us-east-1")
rds = boto3.client('rds', endpoint_url="http://localhost:4566", region_name="us-east-1")
ec2 = boto3.client('ec2', endpoint_url="http://localhost:4566", region_name="us-east-1")

secret_response = secretsmanager.create_secret(
    Name='RDSProxyCredentials',
    SecretString=json.dumps({"username":"dbadmin","password":"supersecret123"})
)
secret_arn = secret_response['ARN']

trust_policy = {
  "Version": "2012-10-17",
  "Statement": [{"Effect": "Allow", "Principal": {"Service": "rds.amazonaws.com"}, "Action": "sts:AssumeRole"}]
}

with open('proxy-trust.json', 'w') as f:
    json.dump(trust_policy, f)

role_response = iam.create_role(
    RoleName='RDSProxyRole',
    AssumeRolePolicyDocument=json.dumps(trust_policy)
)
proxy_role_arn = role_response['Role']['Arn']

subnets = ec2.describe_subnets()
subnet_ids = [s['SubnetId'] for s in subnets['Subnets'][:2]]

if not subnet_ids:
    subnet_ids = ['subnet-1', 'subnet-2']

rds.create_db_proxy(
    DBProxyName='lambda-db-proxy',
    EngineFamily='POSTGRESQL',
    Auth=[
        {
            'AuthScheme': 'SECRETS',
            'SecretArn': secret_arn,
            'IAMAuth': 'DISABLED'
        }
    ],
    RoleArn=proxy_role_arn,
    VpcSubnetIds=subnet_ids
)

rds.register_db_proxy_targets(
    DBProxyName='lambda-db-proxy',
    TargetGroupName='default',
    DBInstanceIdentifiers=['primary-db']
)

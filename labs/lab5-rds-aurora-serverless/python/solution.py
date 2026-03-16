import boto3

rds = boto3.client('rds', endpoint_url="http://localhost:4566", region_name="us-east-1")

rds.create_db_cluster(
    DBClusterIdentifier='serverless-cluster',
    Engine='aurora-postgresql',
    EngineMode='serverless',
    MasterUsername='admin',
    MasterUserPassword='supersecret123',
    DBSubnetGroupName='my-db-subnets'
)

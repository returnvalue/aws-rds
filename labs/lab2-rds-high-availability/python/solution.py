import boto3

rds = boto3.client('rds', endpoint_url="http://localhost:4566", region_name="us-east-1")

rds.modify_db_instance(
    DBInstanceIdentifier='primary-db',
    MultiAZ=True,
    ApplyImmediately=True
)

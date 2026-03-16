import boto3

kms = boto3.client('kms', endpoint_url="http://localhost:4566", region_name="us-east-1")
rds = boto3.client('rds', endpoint_url="http://localhost:4566", region_name="us-east-1")

kms_response = kms.create_key(Description='RDS Encryption Key')
kms_key_id = kms_response['KeyMetadata']['KeyId']

rds.create_db_instance(
    DBInstanceIdentifier='secure-primary-db',
    DBInstanceClass='db.t3.micro',
    Engine='postgres',
    MasterUsername='dbadmin',
    MasterUserPassword='supersecret123',
    AllocatedStorage=20,
    DBSubnetGroupName='my-db-subnets',
    StorageEncrypted=True,
    KmsKeyId=kms_key_id,
    EnableIAMDatabaseAuthentication=True
)

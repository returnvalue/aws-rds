# Lab 6: Serverless Connection Pooling (RDS Proxy)

**Goal:** Prevent thousands of concurrent Lambda invocations from exhausting the database connections by placing an RDS Proxy between the application and the database.

```bash
# 1. Store the DB credentials securely in AWS Secrets Manager
SECRET_ARN=$(awslocal secretsmanager create-secret \
  --name RDSProxyCredentials \
  --secret-string '{"username":"dbadmin","password":"supersecret123"}' \
  --query 'ARN' --output text)
SECRET_ARN=$(aws secretsmanager create-secret \
  --name RDSProxyCredentials \
  --secret-string '{"username":"dbadmin","password":"supersecret123"}' \
  --query 'ARN' --output text)

# 2. Create an IAM Role for the Proxy to read the Secret
cat <<EOF > proxy-trust.json
{
  "Version": "2012-10-17",
  "Statement": [{"Effect": "Allow", "Principal": {"Service": "rds.amazonaws.com"}, "Action": "sts:AssumeRole"}]
}
EOF
PROXY_ROLE_ARN=$(awslocal iam create-role --role-name RDSProxyRole --assume-role-policy-document file://proxy-trust.json --query 'Role.Arn' --output text)
PROXY_ROLE_ARN=$(aws iam create-role --role-name RDSProxyRole --assume-role-policy-document file://proxy-trust.json --query 'Role.Arn' --output text)

# 3. Create the RDS Proxy attached to our primary database
awslocal rds create-db-proxy \
  --db-proxy-name lambda-db-proxy \
  --engine-family POSTGRESQL \
  --auth "AuthScheme=SECRETS,SecretArn=$SECRET_ARN,IAMAuth=DISABLED" \
  --role-arn $PROXY_ROLE_ARN \
  --vpc-subnet-ids $SUBNET_A $SUBNET_B
aws rds create-db-proxy \
  --db-proxy-name lambda-db-proxy \
  --engine-family POSTGRESQL \
  --auth "AuthScheme=SECRETS,SecretArn=$SECRET_ARN,IAMAuth=DISABLED" \
  --role-arn $PROXY_ROLE_ARN \
  --vpc-subnet-ids $SUBNET_A $SUBNET_B

# 4. Register the primary database as the proxy target
awslocal rds register-db-proxy-targets \
  --db-proxy-name lambda-db-proxy \
  --target-group-name default \
  --db-instance-identifiers primary-db
aws rds register-db-proxy-targets \
  --db-proxy-name lambda-db-proxy \
  --target-group-name default \
  --db-instance-identifiers primary-db
```

## 🧠 Key Concepts & Importance

- **Amazon RDS Proxy:** A fully managed, highly available database proxy for Amazon Relational Database Service (RDS) that makes applications more scalable, more resilient to database failures, and more secure.
- **Connection Pooling:** RDS Proxy maintains a pool of established database connections. This reduces the CPU and memory overhead on the database by reusing existing connections instead of opening a new one for every request.
- **Serverless Integration:** Ideal for serverless applications (like AWS Lambda) that can frequently open and close database connections, potentially exhausting database connection limits.
- **Improved Resiliency:** During a database failover, RDS Proxy can continue to hold application connections and automatically route them to the new primary instance, reducing application downtime.
- **Security with Secrets Manager:** RDS Proxy integrates with AWS Secrets Manager to securely manage database credentials, eliminating the need to hardcode them in application code.

## 🛠️ Command Reference

- `secretsmanager create-secret`: Creates a new secret in AWS Secrets Manager.
    - `--name`: The name of the secret.
    - `--secret-string`: The secret data (e.g., database credentials).
- `iam create-role`: Creates an IAM role with a trust policy.
- `rds create-db-proxy`: Creates a new DB proxy.
    - `--db-proxy-name`: Unique name for the proxy.
    - `--engine-family`: The engine family (e.g., `POSTGRESQL`).
    - `--auth`: Authentication settings, including the Secrets Manager ARN.
    - `--role-arn`: The IAM role ARN for the proxy to use.
    - `--vpc-subnet-ids`: The subnets for the proxy.
- `rds register-db-proxy-targets`: Associates a database instance or cluster with the DB proxy.
    - `--db-instance-identifiers`: The identifier for the DB instance.

---

💡 **Pro Tip: Using `aws` instead of `awslocal`**

If you prefer using the standard `aws` CLI without the `awslocal` wrapper or repeating the `--endpoint-url` flag, you can configure a dedicated profile in your AWS config files.

### 1. Configure your Profile
Add the following to your `~/.aws/config` file:
```ini
[profile localstack]
region = us-east-1
output = json
# This line redirects all commands for this profile to LocalStack
endpoint_url = http://localhost:4566
```

Add matching dummy credentials to your `~/.aws/credentials` file:
```ini
[localstack]
aws_access_key_id = test
aws_secret_access_key = test
```

### 2. Use it in your Terminal
You can now run commands in two ways:

**Option A: Pass the profile flag**
```bash
aws iam create-user --user-name DevUser --profile localstack
```

**Option B: Set an environment variable (Recommended)**
Set your profile once in your session, and all subsequent `aws` commands will automatically target LocalStack:
```bash
export AWS_PROFILE=localstack
aws iam create-user --user-name DevUser
```

### Why this works
- **Precedence**: The AWS CLI (v2) supports a global `endpoint_url` setting within a profile. When this is set, the CLI automatically redirects all API calls for that profile to your local container instead of the real AWS cloud.
- **Convenience**: This allows you to use the standard documentation commands exactly as written, which is helpful if you are copy-pasting examples from AWS labs or tutorials.

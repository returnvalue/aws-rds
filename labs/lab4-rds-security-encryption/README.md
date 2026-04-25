# Lab 4: Advanced Security (Encryption & IAM Auth)

**Goal:** Provision a completely new database that is encrypted at rest using a Customer Managed KMS Key from day one, and enable IAM Database Authentication so we can eventually phase out static passwords.

```bash
# 1. Create a KMS Key for the database encryption
KMS_KEY=$(awslocal kms create-key --description "RDS Encryption Key" --query 'KeyMetadata.KeyId' --output text)
KMS_KEY=$(aws kms create-key --description "RDS Encryption Key" --query 'KeyMetadata.KeyId' --output text)

# 2. Provision a new, fully encrypted RDS instance with IAM Auth enabled
awslocal rds create-db-instance \
  --db-instance-identifier secure-primary-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username dbadmin \
  --master-user-password supersecret123 \
  --allocated-storage 20 \
  --db-subnet-group-name my-db-subnets \
  --storage-encrypted \
  --kms-key-id $KMS_KEY \
  --enable-iam-database-authentication
aws rds create-db-instance \
  --db-instance-identifier secure-primary-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username dbadmin \
  --master-user-password supersecret123 \
  --allocated-storage 20 \
  --db-subnet-group-name my-db-subnets \
  --storage-encrypted \
  --kms-key-id $KMS_KEY \
  --enable-iam-database-authentication
```

## 🧠 Key Concepts & Importance

- **Encryption at Rest:** Protects your data from unauthorized access to the underlying storage. For RDS, this is achieved by using keys that you manage through AWS Key Management Service (KMS).
- **KMS Key Management:** By using a Customer Managed Key (CMK), you have full control over the key's lifecycle, including rotation and access policies.
- **IAM Database Authentication:** Allows you to authenticate to your DB instance using IAM users or roles and an authentication token instead of a password.
- **Security Best Practices:**
    - **No Shared Passwords:** Each user or application uses their own IAM identity.
    - **Temporary Credentials:** Authentication tokens have a lifespan of 15 minutes, reducing the risk of compromised long-term credentials.
    - **Centralized Management:** Manage database access through IAM policies alongside other AWS resources.

## 🛠️ Command Reference

- `kms create-key`: Creates a unique customer managed KMS key.
    - `--description`: A description of the key.
- `rds create-db-instance`: Creates a new DB instance with advanced security.
    - `--storage-encrypted`: Specifies that the DB instance is encrypted at rest.
    - `--kms-key-id`: The identifier for the KMS key to use for encryption.
    - `--enable-iam-database-authentication`: Enables IAM database authentication for the DB instance.

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

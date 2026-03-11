# Lab 4: Advanced Security (Encryption & IAM Auth)

**Goal:** Provision a completely new database that is encrypted at rest using a Customer Managed KMS Key from day one, and enable IAM Database Authentication so we can eventually phase out static passwords.

```bash
# 1. Create a KMS Key for the database encryption
KMS_KEY=$(awslocal kms create-key --description "RDS Encryption Key" --query 'KeyMetadata.KeyId' --output text)

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

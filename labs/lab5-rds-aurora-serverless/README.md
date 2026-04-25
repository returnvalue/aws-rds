# Lab 5: Serverless Workloads (Aurora Serverless)

**Goal:** Deploy a database for an application with highly unpredictable traffic spikes. Aurora Serverless automatically scales compute capacity (ACUs) up and down based on demand.

```bash
# Create an Aurora Serverless v2 PostgreSQL cluster
awslocal rds create-db-cluster \
  --db-cluster-identifier serverless-cluster \
  --engine aurora-postgresql \
  --engine-mode serverless \
  --master-username admin \
  --master-user-password supersecret123 \
  --db-subnet-group-name my-db-subnets
aws rds create-db-cluster \
  --db-cluster-identifier serverless-cluster \
  --engine aurora-postgresql \
  --engine-mode serverless \
  --master-username admin \
  --master-user-password supersecret123 \
  --db-subnet-group-name my-db-subnets
```

## 🧠 Key Concepts & Importance

- **Amazon Aurora Serverless:** An on-demand, auto-scaling configuration for Amazon Aurora. It automatically starts up, shuts down, and scales capacity up or down based on your application's needs.
- **ACU (Aurora Capacity Unit):** A combination of processing and memory capacity. Aurora Serverless scales in terms of ACUs.
- **Cost Efficiency:** You pay only for the database capacity you consume when the database is active. This is ideal for infrequent, intermittent, or unpredictable workloads.
- **Scalability:** It provides a simple, cost-effective option for infrequent or unpredictable workloads, while still providing the performance and availability of Amazon Aurora.
- **DB Cluster:** A serverless configuration consists of a DB cluster with no instances. Instead, it has a pool of resources that are used to satisfy requests.

## 🛠️ Command Reference

- `rds create-db-cluster`: Creates a new Amazon Aurora DB cluster.
    - `--db-cluster-identifier`: The DB cluster identifier.
    - `--engine`: The name of the database engine to be used for this DB cluster (e.g., `aurora-postgresql`).
    - `--engine-mode`: The engine mode of the DB cluster (set to `serverless`).
    - `--master-username`: The name of the master user for the DB cluster.
    - `--master-user-password`: The password for the master user.
    - `--db-subnet-group-name`: A DB subnet group to associate with this DB cluster.

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

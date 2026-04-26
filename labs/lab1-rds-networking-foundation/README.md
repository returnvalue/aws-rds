# Lab 1: Networking Foundation & Base RDS Deployment

**Goal:** RDS requires a DB Subnet Group spanning at least two Availability Zones. We will create the underlying VPC, the Subnet Group, and deploy our primary unencrypted PostgreSQL database.
```bash
# 1. Create a VPC and two Subnets in different AZs
VPC_ID=$(awslocal ec2 create-vpc --cidr-block 10.0.0.0/16 --query 'Vpc.VpcId' --output text)
VPC_ID=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query 'Vpc.VpcId' --output text)
SUBNET_A=$(awslocal ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.1.0/24 --availability-zone us-east-1a --query 'Subnet.SubnetId' --output text)
SUBNET_A=$(aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.1.0/24 --availability-zone us-east-1a --query 'Subnet.SubnetId' --output text)
SUBNET_B=$(awslocal ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.2.0/24 --availability-zone us-east-1b --query 'Subnet.SubnetId' --output text)
SUBNET_B=$(aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.2.0/24 --availability-zone us-east-1b --query 'Subnet.SubnetId' --output text)

# 2. Create the DB Subnet Group
awslocal rds create-db-subnet-group \
  --db-subnet-group-name my-db-subnets \
  --db-subnet-group-description "Primary DB Subnet Group" \
  --subnet-ids $SUBNET_A $SUBNET_B
aws rds create-db-subnet-group \
  --db-subnet-group-name my-db-subnets \
  --db-subnet-group-description "Primary DB Subnet Group" \
  --subnet-ids $SUBNET_A $SUBNET_B

# 3. Provision the primary RDS PostgreSQL Instance
awslocal rds create-db-instance \
  --db-instance-identifier primary-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username dbadmin \
  --master-user-password supersecret123 \
  --allocated-storage 20 \
  --db-subnet-group-name my-db-subnets \
  --no-multi-az
aws rds create-db-instance \
  --db-instance-identifier primary-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username dbadmin \
  --master-user-password supersecret123 \
  --allocated-storage 20 \
  --db-subnet-group-name my-db-subnets \
  --no-multi-az
```

## 🧠 Key Concepts & Importance

- **DB Subnet Group:** A collection of subnets (typically private) that you create in a VPC and that you then designate for your DB instances. Each DB subnet group should have subnets in at least two Availability Zones in a given AWS Region.
- **VPC Isolation:** Placing your RDS instances within a custom VPC allows you to control the networking environment, including IP address range, subnets, and configuration of route tables and network gateways.
- **Relational Database Service (RDS):** A managed service that makes it easy to set up, operate, and scale a relational database in the AWS Cloud.
- **Managed Service Benefits:** AWS handles undifferentiated heavy lifting like hardware provisioning, database setup, patching, and backups.

## 🛠️ Command Reference

- `ec2 create-vpc`: Creates a VPC with the specified IPv4 CIDR block.
- `ec2 create-subnet`: Creates a subnet in the specified VPC and Availability Zone.
- `rds create-db-subnet-group`: Creates a new DB subnet group.
    - `--db-subnet-group-name`: Name for the group.
    - `--subnet-ids`: The list of subnets to include.
- `rds create-db-instance`: Creates a new DB instance.
    - `--db-instance-identifier`: Unique name for the instance.
    - `--db-instance-class`: The compute and memory capacity of the DB instance.
    - `--engine`: The name of the database engine (e.g., `postgres`).
    - `--master-username`: The name of the master user for the DB instance.
    - `--allocated-storage`: The amount of storage (in gigabytes) to be initially allocated.
    - `--no-multi-az`: Specifies that the DB instance is not a Multi-AZ deployment.

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

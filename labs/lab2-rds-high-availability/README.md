# Lab 2: High Availability (Multi-AZ Conversion)

**Goal:** Our database is currently in a single AZ. To prepare for production, modify the instance to enable Multi-AZ deployment for synchronous standby replication and automatic failover.

```bash
# Modify the instance to Multi-AZ
awslocal rds modify-db-instance \
  --db-instance-identifier primary-db \
  --multi-az \
  --apply-immediately
aws rds modify-db-instance \
  --db-instance-identifier primary-db \
  --multi-az \
  --apply-immediately
```

## 🧠 Key Concepts & Importance

- **Multi-AZ Deployment:** RDS automatically provisions and maintains a synchronous standby replica in a different Availability Zone. The primary DB instance is synchronously replicated across Availability Zones to a standby replica to provide data redundancy, eliminate I/O freezes, and minimize latency spikes during system backups.
- **High Availability & Failover:** In the event of a planned or unplanned outage of your DB instance, Amazon RDS automatically switches to a standby replica in another Availability Zone. This failover happens without manual intervention.
- **DNS Endpoint Reliability:** RDS handles the failover automatically so that you can resume database operations as quickly as possible without manual administrative intervention. The DNS endpoint for your DB instance remains the same after a failover.
- **Synchronous Replication:** Data is written to the primary and the standby simultaneously before the write is considered complete, ensuring no data loss during a failover.

## 🛠️ Command Reference

- `rds modify-db-instance`: Modifies settings for a DB instance.
    - `--db-instance-identifier`: The identifier for the DB instance to be modified.
    - `--multi-az`: Specifies that the DB instance should be a Multi-AZ deployment.
    - `--apply-immediately`: Specifies that the modifications should be applied immediately, rather than waiting for the next maintenance window.

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

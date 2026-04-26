# Lab 3: Backup & Retention Policies

**Goal:** Meet strict compliance requirements by extending the automated backup retention period to the maximum allowable limit (35 days) and defining a specific maintenance window to prevent performance degradation during peak business hours.
```bash
# Modify the primary database to enforce maximum automated backup retention
awslocal rds modify-db-instance \
  --db-instance-identifier primary-db \
  --backup-retention-period 35 \
  --preferred-backup-window "02:00-03:00" \
  --apply-immediately
aws rds modify-db-instance \
  --db-instance-identifier primary-db \
  --backup-retention-period 35 \
  --preferred-backup-window "02:00-03:00" \
  --apply-immediately
```

## 🧠 Key Concepts & Importance

- **Automated Backups:** RDS creates and saves automated backups of your DB instance during the backup window. RDS saves the automated backups of your DB instance according to the backup retention period that you specify.
- **Backup Retention Period:** The number of days for which automated backups are retained. Setting this to 35 days ensures maximum data recovery capability.
- **Backup Window:** A daily time range during which RDS performs automated backups of your DB instance. It's best practice to schedule this during the period of lowest expected traffic.
- **Point-in-Time Recovery (PITR):** You can restore a DB instance to any point in time during the backup retention period.
- **Maintenance Window:** A weekly time range during which RDS performs maintenance tasks such as OS and database engine patching.

## 🛠️ Command Reference

- `rds modify-db-instance`: Modifies settings for a DB instance.
    - `--backup-retention-period`: The number of days to retain automated backups (1-35 days).
    - `--preferred-backup-window`: The daily time range (in UTC) during which automated backups are created.
    - `--apply-immediately`: Applies the changes during the current session rather than the next maintenance window.

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

# Lab 3: Backup & Retention Policies

**Goal:** Meet strict compliance requirements by extending the automated backup retention period to the maximum allowable limit (35 days) and defining a specific maintenance window to prevent performance degradation during peak business hours.

```bash
# Modify the primary database to enforce maximum automated backup retention
awslocal rds modify-db-instance \
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

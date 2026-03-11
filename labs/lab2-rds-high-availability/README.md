# Lab 2: High Availability (Multi-AZ Conversion)

**Goal:** Our database is currently in a single AZ. To prepare for production, modify the instance to enable Multi-AZ deployment for synchronous standby replication and automatic failover.

```bash
# Modify the instance to Multi-AZ
awslocal rds modify-db-instance \
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

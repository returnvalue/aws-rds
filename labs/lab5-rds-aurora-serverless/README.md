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

# AWS Relational Database Service (RDS) Labs (LocalStack Pro)

![AWS](https://img.shields.io/badge/AWS-RDS_Database-FF9900?style=for-the-badge&logo=amazonaws)
![LocalStack](https://img.shields.io/badge/LocalStack-Pro-000000?style=for-the-badge)

This repository contains hands-on labs demonstrating core Amazon RDS concepts, from foundational networking and instance provisioning to high availability and data security. Using [LocalStack Pro](https://localstack.cloud/), we simulate a complete AWS database environment locally.

## 🎯 Architecture Goals & Use Cases Covered
Based on AWS best practices (SAA-C03), these labs cover:
* **Networking Foundation:** Designing DB Subnet Groups for multi-AZ reliability.
* **RDS Provisioning:** Launching managed relational databases (PostgreSQL).
* **High Availability:** (Upcoming) Implementing Multi-AZ deployments for failover.
* **Read Scalability:** (Upcoming) Offloading read traffic with Read Replicas.
* **Security & Encryption:** (Upcoming) Securing data at rest with SSE-KMS.
* **Disaster Recovery:** (Upcoming) Managing snapshots and automated backups.

## ⚙️ Prerequisites

* [Docker](https://docs.docker.com/get-docker/) & Docker Compose
* [LocalStack Pro](https://app.localstack.cloud/) account and Auth Token
* [`awslocal` CLI](https://github.com/localstack/awscli-local) (a wrapper around the AWS CLI for LocalStack)

## 🚀 Environment Setup

1. Configure your LocalStack Auth Token in `.env`:
   ```bash
   echo "YOUR_TOKEN=your_auth_token_here" > .env
   ```

2. Start LocalStack Pro:
   ```bash
   docker-compose up -d
   ```

> [!IMPORTANT]
> **Cumulative Architecture:** These labs are designed as a cumulative scenario. You are building an evolving database infrastructure.
>
> **Session Persistence:** These labs rely on bash variables (like `$VPC_ID`, `$SUBNET_A`, etc.). Run all commands in the same terminal session to maintain context.

## 📚 Labs Index
1. [Lab 1: Networking Foundation & Base RDS Deployment](./labs/lab1-rds-networking-foundation/README.md)

resource "aws_rds_cluster" "serverless" {
  cluster_identifier      = "serverless-cluster"
  engine                  = "aurora-postgresql"
  engine_mode             = "serverless"
  master_username         = "admin"
  master_password         = "supersecret123"
  db_subnet_group_name    = var.db_subnet_group_name
  skip_final_snapshot     = true

  scaling_configuration {
    auto_pause               = true
    max_capacity             = 16
    min_capacity             = 2
    seconds_until_auto_pause = 300
  }
}

resource "aws_secretsmanager_secret" "db_creds" {
  name = "RDSProxyCredentials"
}

resource "aws_iam_role" "proxy_role" {
  name = "RDSProxyRole"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "rds.amazonaws.com" }
    }]
  })
}

resource "aws_db_proxy" "main" {
  name                   = "lambda-db-proxy"
  engine_family          = "POSTGRESQL"
  role_arn               = aws_iam_role.proxy_role.arn
  vpc_subnet_ids         = var.subnet_ids

  auth {
    auth_scheme = "SECRETS"
    secret_arn  = aws_secretsmanager_secret.db_creds.arn
    iam_auth    = "DISABLED"
  }
}

resource "aws_db_proxy_target" "primary" {
  db_instance_identifier = var.db_instance_id
  db_proxy_name          = aws_db_proxy.main.name
  target_group_name      = "default"
}

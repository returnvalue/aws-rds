resource "aws_kms_key" "rds_key" {
  description = "RDS Encryption Key"
}

resource "aws_db_instance" "secure_primary" {
  identifier                          = "secure-primary-db"
  allocated_storage                   = 20
  engine                              = "postgres"
  instance_class                      = "db.t3.micro"
  username                            = "dbadmin"
  password                            = "supersecret123"
  db_subnet_group_name                = var.db_subnet_group_name
  storage_encrypted                   = true
  kms_key_id                          = aws_kms_key.rds_key.arn
  iam_database_authentication_enabled = true
  skip_final_snapshot                 = true
}

resource "aws_db_instance" "primary" {
  identifier              = "primary-db"
  backup_retention_period = 35
  preferred_backup_window = "02:00-03:00"
  apply_immediately       = true
  # ... other existing attributes
}

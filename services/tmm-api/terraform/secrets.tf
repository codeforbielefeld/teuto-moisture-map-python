

resource "aws_secretsmanager_secret" "lambda_secret" {
  for_each = toset([
    "INFLUXDB_V2_URL",
    "INFLUXDB_V2_ORG",
    "INFLUXDB_V2_TOKEN",
    "TMM_BUCKET",
    "TMM_AUTH_SECRET"
  ])
  name = "${local.prefix}-${each.key}"
}

resource "aws_secretsmanager_secret_version" "lambda_secret_version" {
  secret_id = aws_secretsmanager_secret.lambda_secret[each.key].id
  for_each = {
    INFLUXDB_V2_URL   = var.influx_url
    INFLUXDB_V2_ORG   = var.influx_org
    INFLUXDB_V2_TOKEN = var.influx_token
    TMM_BUCKET        = var.influx_bucket
    TMM_AUTH_SECRET   = var.tmm_auth_secret
  }
  secret_string = each.value
}


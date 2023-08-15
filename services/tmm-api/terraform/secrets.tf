
resource "aws_ssm_parameter" "lambda_secret" {
  type  = "SecureString"
  value = each.value
  name  = "/${local.prefix}/lambda_secret/${each.key}"
  for_each = {
    INFLUXDB_V2_URL   = var.influx_url
    INFLUXDB_V2_ORG   = var.influx_org
    INFLUXDB_V2_TOKEN = var.influx_token
    TMM_BUCKET        = var.influx_bucket
    TMM_AUTH_SECRET   = var.tmm_auth_secret
  }
}

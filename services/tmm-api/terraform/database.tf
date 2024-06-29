

resource "aws_dynamodb_table" "tmm_sensors" {
    name           = local.sensors_table_name
    billing_mode   = "PAY_PER_REQUEST"
    hash_key       = "sensor_id"

    attribute {
        name = "sensor_id"
        type = "S"
    }
}

data "archive_file" "initial_dummy_code" {
  type = "zip"
  output_path = "${path.module}/dummy_lambda_function_package.zip"
  source {
    content = "dummy"
    filename = "dummy.txt"
  }
}

resource "aws_lambda_function" "api_lambda_function" {

  filename      = data.archive_file.initial_dummy_code.output_path
  function_name = local.lambda_function_name
  role          = aws_iam_role.api_lambda_function_role.arn
  handler       = local.lambda_function_handler
  runtime       = "python3.10"

  source_code_hash = data.archive_file.initial_dummy_code.output_sha256

  # we can check the memory usage in the lambda dashboard, sklearn is a bit memory hungry..
  # memory_size = 256

  # Uncomment the next line if you have an M1 processor
  # architectures = [ "arm64" ] 
  depends_on = [aws_cloudwatch_log_group.lambda_log]

  lifecycle {
    ignore_changes = [ filename, source_code_hash ]
  }

  environment {
    variables = {
      INFLUXDB_V2_URL   = var.influx_url
      INFLUXDB_V2_ORG   = var.influx_org
      INFLUXDB_V2_TOKEN = var.influx_token
      TMM_BUCKET        = var.influx_bucket
      ENABLE_WRITE      = var.tmm_enable_write
      TMM_AUTH_SECRET   = var.tmm_auth_secret
    }
  }
}

# as per https://learn.hashicorp.com/tutorials/terraform/lambda-api-gateway
# provide role with no access policy initially
resource "aws_iam_role" "api_lambda_function_role" {
  name = "api-lambda-function-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = "sts:AssumeRole"
      Sid    = ""
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "api_lambda_function_policy_attachement" {
  role       = aws_iam_role.api_lambda_function_role.name
  policy_arn = aws_iam_policy.api_lambda_function_policy.arn
}

resource "aws_iam_policy" "api_lambda_function_policy" {
  name = "api-lambda-function-policy"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

resource "aws_cloudwatch_log_group" "lambda_log" {
  name = "/aws/lambda/${local.lambda_function_name}"

  retention_in_days = local.lambda_log_retention
}

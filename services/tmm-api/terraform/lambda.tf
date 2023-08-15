resource "aws_s3_bucket" "lambda_source_bucket" {
  bucket = "${local.prefix2}-lambda-source"
}

data "archive_file" "initial_dummy_code" {
  type        = "zip"
  output_path = "${path.module}/dummy_lambda_function_package.zip"
  source {
    filename = "tmm_api.py"
    content  = "def handler(_e,_c):\n  return {'statusCode': 200, 'body': 'Hello World'}"
  }
}

resource "aws_s3_object" "lambda_source_code" {
  bucket = aws_s3_bucket.lambda_source_bucket.id
  key    = "dummy_lambda_function_package.zip"
  source = data.archive_file.initial_dummy_code.output_path
  etag   = data.archive_file.initial_dummy_code.output_sha256

  lifecycle {
    ignore_changes = [source, etag]
  }
}

resource "aws_lambda_function" "api_lambda_function" {
  function_name = "${local.prefix}_lambda"
  runtime       = "python3.11"
  role          = aws_iam_role.api_lambda_function_role.arn

  handler          = local.lambda_function_handler
  source_code_hash = aws_s3_object.lambda_source_code.version_id
  s3_bucket        = aws_s3_bucket.lambda_source_bucket.id
  s3_key           = aws_s3_object.lambda_source_code.key

  depends_on = [aws_cloudwatch_log_group.lambda_log]

  lifecycle {
    ignore_changes = [source_code_hash, s3_bucket, s3_key, filename]
  }

  environment {
    variables = {
      ENABLE_WRITE               = var.tmm_enable_write
      INFLUXDB_V2_URL_SSM_NAME   = aws_ssm_parameter.lambda_secret["INFLUXDB_V2_URL"].name
      INFLUXDB_V2_ORG_SSM_NAME   = aws_ssm_parameter.lambda_secret["INFLUXDB_V2_ORG"].name
      INFLUXDB_V2_TOKEN_SSM_NAME = aws_ssm_parameter.lambda_secret["INFLUXDB_V2_TOKEN"].name
      TMM_BUCKET_SSM_NAME        = aws_ssm_parameter.lambda_secret["TMM_BUCKET"].name
      TMM_AUTH_SECRET_SSM_NAME   = aws_ssm_parameter.lambda_secret["TMM_AUTH_SECRET"].name
    }
  }
}


# as per https://learn.hashicorp.com/tutorials/terraform/lambda-api-gateway
# provide role with no access policy initially
resource "aws_iam_role" "api_lambda_function_role" {
  name = "${local.prefix}_api-lambda-function-role"

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
  name = "${local.prefix}-api-lambda-function-policy"

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
      },
      {
        "Effect" : "Allow",
        "Action" : "ssm:GetParameter",
        "Resource" : [for secret in aws_ssm_parameter.lambda_secret : secret.arn]
      }
    ]
  })
}

resource "aws_cloudwatch_log_group" "lambda_log" {
  name = "/aws/lambda/${local.prefix}_lambda"

  retention_in_days = local.lambda_log_retention
}

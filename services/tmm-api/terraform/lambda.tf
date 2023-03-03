resource "aws_lambda_function" "api_lambda_function" {

  filename      = local.lambda_function_package
  function_name = local.lambda_function_name
  role          = aws_iam_role.api_lambda_function_role.arn
  handler       = local.lambda_function_handler
  runtime       = "python3.9"

  source_code_hash = filebase64sha256(local.lambda_function_package)

  # we can check the memory usage in the lambda dashboard, sklearn is a bit memory hungry..
  # memory_size = 256

  # Uncomment the next line if you have an M1 processor
  # architectures = [ "arm64" ] 
}

# as per https://learn.hashicorp.com/tutorials/terraform/lambda-api-gateway
# provide role with no access policy initially
resource "aws_iam_role" "api_lambda_function_role" {
  name = "api-lambda-function-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "api_lambda_function_policy_attachement" {
  role       = aws_iam_role.api_lambda_function_role.name
  policy_arn = aws_iam_policy.api_lambda_function_policy.arn
}

resource "aws_iam_policy" "api_lambda_function_policy" {
  name = "api-lambda-function-policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
EOF
}
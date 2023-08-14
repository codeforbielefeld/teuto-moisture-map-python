resource "aws_iam_role" "lambda_deploy_role" {
  name = "${local.prefix}_lambda_deploy_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = var.deployment_identity_provider
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
            "token.actions.githubusercontent.com:sub" = local.deploy_subject
          }
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda_deploy_role_policy" {
  name = "${local.prefix}_lambda_deploy_role_policy"
  role = aws_iam_role.lambda_deploy_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["sts:GetCallerIdentity"]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = ["s3:ListBucket"]
        Resource = aws_s3_bucket.lambda_source_bucket.arn
      },
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"]
        Resource = "${aws_s3_bucket.lambda_source_bucket.arn}/lambda_package.zip"
      },
      {
        Effect   = "Allow"
        Action   = ["lambda:GetFunction", "lambda:ListVersionsByFunction", "lambda:GetFunctionCodeSigningConfig", "lambda:UpdateFunctionCode", "lambda:UpdateFunctionConfiguration"]
        Resource = aws_lambda_function.api_lambda_function.arn
      }
    ]
  })
}

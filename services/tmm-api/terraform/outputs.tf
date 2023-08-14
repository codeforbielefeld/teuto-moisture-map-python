# Output value definitions

output "apigwy_url" {
  description = "URL for API Gateway"
  value       = aws_apigatewayv2_api.api_gw.api_endpoint
}

output "lambda_name" {
  description = "Name of the lambda function"
  value       = aws_lambda_function.api_lambda_function.function_name
}

output "lambda_source_bucket" {
  description = "Bucket for the lambda function code"
  value       = aws_s3_bucket.lambda_source_bucket.id

}

output "lambda_deploy_role" {
  description = "Deploy role for the lambda"
  value       = aws_iam_role.lambda_deploy_role.arn

}

# Output value definitions

output "apigwy_url" {
  description = "URL for API Gateway"
  value = aws_apigatewayv2_api.api_gw.api_endpoint
  sensitive = true
}

resource "aws_apigatewayv2_api" "api_gw" {
  name          = "${local.prefix}_gw"
  protocol_type = "HTTP"
  description   = "Api Gateway for the tmm api"

  cors_configuration {
      allow_credentials = false
      allow_headers     = []
      allow_methods     = [
          "GET",
          "HEAD",
          "OPTIONS",
          "POST",
      ]
      allow_origins     = [
          "*",
      ]
      expose_headers    = []
      max_age           = 0
  }
}


resource "aws_apigatewayv2_stage" "default" {
  api_id = aws_apigatewayv2_api.api_gw.id

  name        = "$default"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw.arn

    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
      }
    )
  }
  depends_on = [aws_cloudwatch_log_group.api_gw]
}

resource "aws_apigatewayv2_integration" "app" {
  api_id = aws_apigatewayv2_api.api_gw.id

  integration_uri    = aws_lambda_function.api_lambda_function.invoke_arn
  integration_type   = "AWS_PROXY"
}

resource "aws_apigatewayv2_route" "any" {
  api_id = aws_apigatewayv2_api.api_gw.id
  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.app.id}"
}

resource "aws_cloudwatch_log_group" "api_gw" {
  name = "/aws/api_gw/${aws_apigatewayv2_api.api_gw.name}"

  retention_in_days = local.apigw_log_retention
}

resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api_lambda_function.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.api_gw.execution_arn}/*/*"
}
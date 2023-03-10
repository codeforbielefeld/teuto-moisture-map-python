# constant settings
locals {
  
  lambda_function_name = "tmm_api_lambda"

  lambda_function_package = "lambda_package.zip"

  lambda_function_handler = "tmm_api.handler"

  lambda_log_retention = 7

  apigw_log_retention = 7
  
  api_gw_name = "tmm-api"

}

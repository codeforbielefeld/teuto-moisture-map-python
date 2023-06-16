# constant settings
locals {
  
  lambda_function_name = "tmm_api_lambda"

  lambda_function_package = "lambda_package.zip"

  lambda_function_handler = "tmm_api.handler"

  lambda_log_retention = 7

  apigw_log_retention = 7
  
  api_gw_name = "tmm-api"

}

variable "influx_url" {
  description = "Url for the influx database"
  type = string
  sensitive = true
}

variable "influx_org" {
  description = "Organisaiton for the influx database"
  type = string
  sensitive = true
}

variable "influx_token" {
  description = "Token for the influx database"
  type = string
  sensitive = true
}

variable "influx_bucket" {
  description = "Bucket for the influx database"
  type = string
  sensitive = true
}

variable "tmm_enable_write" {
  description = "Whether or not to enable write access in the api"
  type = bool
  sensitive = true
}

variable "tmm_auth_secret" {
  description = "The auth secret used to validate api keys"
  type = string
  sensitive = true
}


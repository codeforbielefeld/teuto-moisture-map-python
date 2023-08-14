# constant settings
locals {

  name = "tmm_api"

  prefix = "${local.name}_${var.env}"

  prefix2 = replace(local.prefix, "_", "-")

  lambda_function_handler = "tmm_api.handler"

  lambda_log_retention = 7

  apigw_log_retention = 7

  deploy_subject = "repo:codeforbielefeld/teuto-moisture-map-python:environment:aws_${var.env}"

}

variable "env" {
  description = "Environment"
  default  = "dev"
  type        = string

}

variable "influx_url" {
  description = "Url for the influx database"
  type        = string
  sensitive   = true
}

variable "influx_org" {
  description = "Organisaiton for the influx database"
  type        = string
  sensitive   = true
}

variable "influx_token" {
  description = "Token for the influx database"
  type        = string
  sensitive   = true
}

variable "influx_bucket" {
  description = "Bucket for the influx database"
  type        = string
  sensitive   = true
}

variable "tmm_enable_write" {
  description = "Whether or not to enable write access in the api"
  type        = bool
  sensitive   = true
}

variable "tmm_auth_secret" {
  description = "The auth secret used to validate api keys"
  type        = string
  sensitive   = true
}


variable "deployment_identity_provider" {
  description = "The ARN of the identity provider for the deploy role"
  type = string
}
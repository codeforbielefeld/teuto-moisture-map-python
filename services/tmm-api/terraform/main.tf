terraform {
  backend "s3" {
    bucket = "code4bielefeld-tmm-backend-terraform"
    key    = "tmm-backend.tfstate"
    region = "eu-central-1"
  }

  required_providers {
    aws = {
      version = ">= 4.66.0"
      source  = "hashicorp/aws"
    }
  }
}

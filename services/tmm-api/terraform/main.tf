terraform {
  backend "s3" {
    bucket = "tmm-terraform"
    key    = "terraform.tfstate"
    region = "eu-central-1"
  }

  required_providers {
    aws = {
      version = ">= 4.66.0"
      source  = "hashicorp/aws"
    }
  }
}

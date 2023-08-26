provider "aws" {
  region = "ap-southeast-2"
  # profile = "<insert_name_here>"
  default_tags {
    tags = {
      deployed_by = "<insert_name_here>"
      project     = "priceChecker"
    }
  }
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "2.3.0"
    }
  }
}

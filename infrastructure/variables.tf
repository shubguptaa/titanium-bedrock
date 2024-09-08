variable "region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "s3_bucket_name" {
  description = "S3 bucket for model data"
  default     = "titanium-model-data-bucket"
}

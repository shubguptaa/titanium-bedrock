provider "aws" {
  region = var.region
}

resource "aws_s3_bucket" "model_data" {
  bucket = var.s3_bucket_name
}

resource "aws_iam_role" "bedrock_role" {
  name = "bedrock_exec_role"
  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Principal": {
          "Service": "bedrock.amazonaws.com"
        },
        "Effect": "Allow"
      }
    ]
  })
}

resource "aws_iam_role_policy" "s3_access" {
  name   = "bedrock_s3_policy"
  role   = aws_iam_role.bedrock_role.id
  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": ["s3:GetObject", "s3:PutObject"],
        "Effect": "Allow",
        "Resource": [
          "${aws_s3_bucket.model_data.arn}/*"
        ]
      }
    ]
  })
}

output "bucket_name" {
  value = aws_s3_bucket.model_data.id
}

output "bedrock_role_arn" {
  value = aws_iam_role.bedrock_role.arn
}

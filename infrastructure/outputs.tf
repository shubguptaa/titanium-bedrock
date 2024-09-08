output "bucket_name" {
  value = aws_s3_bucket.model_data.id
}

output "bedrock_role_arn" {
  value = aws_iam_role.bedrock_role.arn
}

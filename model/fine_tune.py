import boto3
import os
from s3_data_loader import load_training_data
from bedrock import BedrockClient

# Initialize the Bedrock client
bedrock_client = BedrockClient()

# S3 Data Loading
s3_bucket = os.getenv("S3_BUCKET_NAME")
training_data = load_training_data(s3_bucket, "training-data/")

# Fine-tune the Titan model
def fine_tune_model():
    model_id = "amazon.titan"
    fine_tune_job = bedrock_client.create_fine_tune_job(
        ModelId=model_id,
        InputDataConfig={"S3Uri": f"s3://{s3_bucket}/training-data/"},
        OutputDataConfig={"S3Uri": f"s3://{s3_bucket}/output/"},
        TrainingParameters={}
    )
    
    return fine_tune_job

if __name__ == "__main__":
    fine_tune_job = fine_tune_model()
    print(f"Fine-tuning job started: {fine_tune_job['JobId']}")

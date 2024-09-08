import streamlit as st
import boto3
import os

# Initialize S3 client
s3 = boto3.client('s3')
s3_bucket = os.getenv("S3_BUCKET_NAME")

# Streamlit UI
st.title("Project Titanium - AI Insights")
st.write("Fine-tuned AI Model Outputs")

# Load outputs from S3
def load_model_output():
    output_key = "output/results.json"
    response = s3.get_object(Bucket=s3_bucket, Key=output_key)
    result = response['Body'].read().decode('utf-8')
    return result

# Display the results
if st.button("Show Insights"):
    st.write("Loading AI-generated insights...")
    insights = load_model_output()
    st.json(insights)

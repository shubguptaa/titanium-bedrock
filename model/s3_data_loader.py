import boto3

def load_training_data(bucket, prefix):
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    
    data_files = []
    for obj in response.get('Contents', []):
        data_files.append(obj['Key'])
    
    return data_files

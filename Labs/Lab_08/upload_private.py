import boto3

s3 = boto3.client('s3', region_name='us-east-1')

bucket = 'ds2002-f25-zry3fr'
local_file = 'PNG_transparency_demonstration_1.png'  # Replace with your file
s3_key = 'private_image.png'  # This is how it will appear in S3

with open(local_file, 'rb') as data:
    s3.put_object(Body=data, Bucket=bucket, Key=s3_key)

print(f"{local_file} uploaded to {bucket}/{s3_key} as private.")


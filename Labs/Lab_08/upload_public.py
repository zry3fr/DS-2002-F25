import boto3

s3 = boto3.client('s3', region_name='us-east-1')

bucket = 'ds2002-f25-zry3fr'
local_file = 'PNG_transparency_demonstration_1.png'  # Replace with your file
s3_key = 'public_image.png'

s3.upload_file(
    Filename=local_file,
    Bucket=bucket,
    Key=s3_key,
    ExtraArgs={'ACL': 'public-read'}
)

print(f"{local_file} uploaded to {bucket}/{s3_key} as public.")


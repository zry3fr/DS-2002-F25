#!/usr/bin/env python3

import boto3
import urllib.request
import sys
import os

if len(sys.argv) != 4:
    print("Usage: python3 upload_and_presign.py <file_url> <bucket_name> <expiration_in_seconds>")
    sys.exit(1)

file_url = sys.argv[1]
bucket_name = sys.argv[2]
expires_in = int(sys.argv[3])

local_file = os.path.basename(file_url)

s3_key = local_file

print(f"Downloading {local_file} from {file_url}...")
urllib.request.urlretrieve(file_url, local_file)
print(f"Saved {local_file} locally.")

s3 = boto3.client('s3', region_name='us-east-1')

print(f"Uploading {local_file} to s3://{bucket_name}/ ...")
s3.upload_file(local_file, bucket_name, s3_key)
print("Upload complete.")

presigned_url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': bucket_name, 'Key': s3_key},
    ExpiresIn=expires_in
)

print("\nPresigned URL (copy to browser to access file):")
print(presigned_url)


#!/bin/bash

if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <local_file> <bucket_name> <expiration_in_seconds>"
  exit 1
fi

LOCAL_FILE=$1
BUCKET_NAME=$2
EXPIRATION=$3

echo "Uploading $LOCAL_FILE to s3://$BUCKET_NAME/..."
aws s3 cp "$LOCAL_FILE" "s3://$BUCKET_NAME/"

echo "Generating presigned URL for $LOCAL_FILE (expires in $EXPIRATION seconds)..."
aws s3 presign "s3://$BUCKET_NAME/$(basename $LOCAL_FILE)" --expires-in "$EXPIRATION"


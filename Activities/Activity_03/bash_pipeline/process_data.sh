#!/bin/bash

# A variable to store the name of our input file
DATA_FILE="breeds.json"

# Check if the data file exists
if [ ! -f "$DATA_FILE" ]; then
    echo "Error: Data file '$DATA_FILE' not found. Please run fetch_data.sh first." >&2
    exit 1
fi

# Use jq to count the number of top-level keys in the 'message' field
echo "Processing data from '$DATA_FILE'..."
NUM_BREEDS=$(jq '.message | keys | length' "$DATA_FILE")

# Output the result
echo "Total number of unique dog breeds: $NUM_BREEDS"


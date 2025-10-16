#!/bin/bash

read -p "Enter the TCG Card Set ID (e.g., base1, base4): " SET_ID

if [ -z "$SET_ID" ]; then
    echo "Error: Set ID cannot be empty." >&2
    exit 1
fi

OUTPUT_DIR="card_set_lookup"
OUTPUT_FILE="${OUTPUT_DIR}/${SET_ID}.json"

mkdir -p "$OUTPUT_DIR"

echo "Fetching card data for set: $SET_ID..."

curl -s "https://api.pokemontcg.io/v2/cards?q=set.id:${SET_ID}" -o "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo "Card data for '${SET_ID}' saved to: $OUTPUT_FILE"
else
    echo "Failed to fetch data for set '${SET_ID}'." >&2
    exit 1
fi


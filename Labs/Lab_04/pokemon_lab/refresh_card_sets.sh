#!/bin/bash

echo "Refreshing all card sets in card_set_lookup/..."

if [ ! -d "card_set_lookup" ]; then
    echo "Error: card_set_lookup/ directory not found." >&2
    exit 1
fi

for FILE in card_set_lookup/*.json; do

    [ -e "$FILE" ] || { echo "No JSON files found to refresh."; exit 0; }

    SET_ID=$(basename "$FILE" .json)

    echo "Updating card set: $SET_ID..."

    curl -s "https://api.pokemontcg.io/v2/cards?q=set.id:${SET_ID}" -o "$FILE"

    echo "Data for '$SET_ID' updated and saved to $FILE."
done

echo "All card sets have been refreshed"


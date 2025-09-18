#!/bin/bash
set -e  # Exit on error

# Define variables
RAW_DATA_DIR="raw_metars"
OUTPUT_FILE="weather_report.csv"

# Write header line to the CSV
echo "ICAO,ObservationTime,WindDirection,WindSpeed,TemperatureC,FlightCategory" > "$OUTPUT_FILE"

echo "Analyzing METAR data..."

# Loop through JSON files
for json_file in "$RAW_DATA_DIR"/*.json; do
    if [ -f "$json_file" ]; then
        if [ "$(jq 'length' "$json_file")" -gt 0 ]; then
            jq -r '.[0] | [.icaoId, .reportTime, .wdir, .wspd, .temp, .fltCat] | @csv' "$json_file" >> "$OUTPUT_FILE"
        else
            echo "Warning: No METAR data found in $json_file. Skipping." >&2
        fi
    fi
done

echo "Analysis complete. Results are in '$OUTPUT_FILE'."


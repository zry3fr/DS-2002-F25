# Lab 3: Bash Scripting with Aviation Weather Data ✈️

This lab guides you through building a simple but complete data pipeline using Bash scripts and a `Makefile`. You'll use `curl` to fetch raw weather data from the Aviation Weather API, `jq` to process the JSON, and `make` to automate the entire workflow. The goal is to fetch and analyze METAR data (a weather report for airports) for a list of U.S. airports.

---

### Step 1: Set Up Your Project

1.  Open your terminal (`Git Bash` on Windows or `Terminal` on macOS).
2.  Navigate to the `Labs/Lab_03` directory within your `DS-2002-F25` repository.
3.  Create and switch to a new branch for this lab:
    ```bash
    git checkout -b Lab_3
    ```
4.  Create a new directory for this lab and move into it:
    ```bash
    mkdir aviation_weather_pipeline && cd aviation_weather_pipeline
    ```
5.  Create a file named `airport_codes.txt` and add the following airport identifiers. These are **ICAO codes** that uniquely identify airports worldwide. In the U.S., they typically start with a 'K'.
    ```bash
    touch airport_codes.txt
    ```
6.  Open `airport_codes.txt` with a text editor (`nano`, `vim`, or any other) and add these codes, each on a new line:
    ```
    KBWI
    KDCA
    KIAD
    KJFK
    KPHL
    ```

---

### Step 2: Create the `fetch_metars.sh` Script

This script will use `curl` to fetch JSON data for each airport and save it to a separate file.

1.  Create the script file and make it executable:
    ```bash
    touch fetch_metars.sh
    chmod +x fetch_metars.sh
    ```
2.  Open `fetch_metars.sh` and add the following code, line by line.

    **Add the Shebang and `set -e`**
    ```bash
    #!/bin/bash
    # Exit immediately if a command exits with a non-zero status.
    set -e
    ```
    The **shebang** `#!` tells the operating system to execute this file using `/bin/bash`. The `set -e` command is a crucial safety measure in Bash scripting that will **immediately exit the script if any command fails**. This prevents a pipeline from running with bad or missing data.

    **Define Variables**
    ```bash
    API_URL="[https://aviationweather.gov/api/data/metar](https://aviationweather.gov/api/data/metar)"
    OUTPUT_DIR="raw_metars"
    AIRPORT_CODES_FILE="airport_codes.txt"

    mkdir -p "$OUTPUT_DIR"
    echo "Fetching METAR data for airports..."
    ```
    Using **variables** makes your script cleaner and easier to modify. The `mkdir -p` command creates a directory for our raw data. The `-p` flag ensures it won't throw an error if the directory already exists.

    **Loop Through the Airport Codes**
    ```bash
    while read -r airport_code; do
      if [ -z "$airport_code" ]; then
        continue
      fi

      URL="$API_URL?ids=$airport_code&format=json"
      OUTPUT_FILE="$OUTPUT_DIR/${airport_code}.json"

      echo "  -> Fetching data for $airport_code..."
      
      curl -s "$URL" -o "$OUTPUT_FILE" 2>&1
    
      if [ $? -ne 0 ]; then
          echo "Error: curl failed for $airport_code." >&2
          exit 1
      fi
      
      if [ ! -s "$OUTPUT_FILE" ] || [ "$(jq 'length' "$OUTPUT_FILE")" -eq 0 ]; then
          echo "Warning: No METAR data found for $airport_code. The API returned an empty response." >&2
      else
          echo "  -> Data for $airport_code saved successfully."
      fi
    done < "$AIRPORT_CODES_FILE"
    
    echo "Data fetching complete. Check the '$OUTPUT_DIR' directory."
    ```
    The **`while read` loop** iterates through each line of the `airport_codes.txt` file. We construct a unique URL and output file name for each airport. The **`curl`** command fetches the data. The `-s` flag makes it silent (no progress bar), and `-o` specifies the output file. The `2>&1` redirects standard error to standard output so that any error messages from `curl` are visible. We then check **`$?`**, a special variable that holds the exit status of the previous command. A value of `0` means success, so we exit if it's not `0`. We also check if the output file is empty or if its JSON array has a length of zero using `jq`, which indicates no data was found.

---

### Step 3: Create the `analyze_data.sh` Script

This script will read the JSON files, use `jq` to extract key information, and save it all to a single CSV file.

1.  Create the script file and make it executable:
    ```bash
    touch analyze_data.sh
    chmod +x analyze_data.sh
    ```
2.  Open `analyze_data.sh` and add the following code.

    **Add the Shebang and `set -e`**
    ```bash
    #!/bin/bash
    set -e
    ```

    **Define Variables and Write the Header**
    ```bash
    RAW_DATA_DIR="raw_metars"
    OUTPUT_FILE="weather_report.csv"

    echo "ICAO,ObservationTime,WindDirection,WindSpeed,TemperatureC,FlightCategory" > "$OUTPUT_FILE"
    echo "Analyzing METAR data..."
    ```
    Here, we define our input and output files. The `echo` command with the single `>` redirects and **overwrites** the output file, ensuring it starts fresh with only the header row.

    **Loop Through the JSON Files and Process with `jq`**
    ```bash
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
    ```
    The **`for` loop** iterates through every file ending in `.json` inside our `raw_metars` directory. The **`jq`** command is the core of this script. It:
    * `jq -r`: Tells `jq` to output raw strings without quotes.
    * `'.[0]'`: Selects the first (and only) element from the JSON array.
    * `'| [.icaoId, .reportTime, ...]'`: Creates a new array with the values from the specified keys in the JSON object.
    * `'| @csv'`: Converts that array of values into a single comma-separated line.
    The `>>` redirects and **appends** this new line to the `weather_report.csv` file, so we don't overwrite the header or the previous data.

---

### Step 4: Create a `Makefile` to Automate the Pipeline

The `Makefile` will orchestrate your scripts, ensuring they run in the correct order.

1.  Create a file named `Makefile`:
    ```bash
    touch Makefile
    ```
2.  Open `Makefile` and add the following rules. **NOTE: The indentation for the commands must be a single tab character, not spaces.**

    ```makefile
    .PHONY: all fetch analyze clean

    # The default target. Running 'make' will execute this rule.
    all: analyze

    # Rule to fetch the raw METAR data.
    fetch:
    	@echo "--- Fetching data from the Aviation Weather API ---"
    	bash ./fetch_metars.sh

    # Rule to analyze the raw data.
    analyze: fetch
    	@echo "--- Analyzing raw METAR data ---"
    	bash ./analyze_data.sh
    	@echo "--- Pipeline complete. Results in weather_report.csv ---"

    # Rule to clean up all generated files and directories.
    clean:
    	@echo "--- Cleaning up generated files and directories ---"
    	rm -rf raw_metars/ weather_report.csv
    ```
    A `Makefile` defines a series of **targets** (e.g., `fetch`, `analyze`) and their **prerequisites**. When you run `make analyze`, it first sees that `fetch` is a prerequisite, so it runs the `fetch` target first. This automatically enforces the correct order of operations. The `clean` target is a common convention for removing temporary or generated files.

---

### Step 5: Run the Pipeline and Verify

1.  Run the full pipeline with a single command:
    ```bash
    make
    ```
    This command will execute both scripts in the correct order and produce the final `weather_report.csv` file.

2.  Verify the output by using `cat` or `less`:
    ```bash
    cat weather_report.csv
    ```

3.  Finally, clean up your workspace:
    ```bash
    make clean
    ```

4.  Add, commit, and push your changes to GitHub to submit your work for grading.
    ```bash
    git add .
    git commit -m "Complete Lab 3: Aviation Weather Pipeline"
    git push --set-upstream origin Lab_3
    ```

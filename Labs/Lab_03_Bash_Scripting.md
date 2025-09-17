# Lab 3: Bash Scripting with the Star Wars API
Welcome to Lab 3! This week, you'll apply what you've learned about Bash scripting to build a more complex data pipeline. You'll use curl to fetch data from the Star Wars API, jq to process that JSON, and a Makefile to automate the entire process. This lab will require you to think critically about how to chain commands, handle errors, and use Bash's control flow features. The final product should be a set of scripts that fetches data for all Star Wars films, extracts specific details, and outputs a formatted report.

<br>

## Step 0. Setup
1. Open your Terminal (macOS) or Git Bash (WIndows) and navigate to your DS-2002-F25 repository.
2. Run the `update_repo.sh` script.
3. Create a new branch called `Lab_3` and move into it:
```
git checkout -b Lab_3
```
4. Make a new directory for this lab in your Lab_03 directory, and navigate into your new directory:
```
mkdir Labs/Lab_03/sw_api_pipeline && cd Labs/Lab_03/sw_api_pipeline
```

Step 1: Create the fetch_films.sh Script
This script will fetch details for all Star Wars films from the SWAPI (Star Wars API). Unlike the last activity, the API data is paginated, which means you'll need to use a loop to fetch all the data.

Create the script: Create a new file named fetch_films.sh.

Add the shebang and error handling: Start the script with a shebang and set -e to ensure the script exits immediately if any command fails.

Bash

#!/bin/bash
set -e
Define a variable: Define a variable URL to hold the initial API endpoint URL: https://swapi.dev/api/films/.

Loop to fetch all films: Use a while loop to repeatedly fetch data until there are no more pages.

Inside the loop, use curl to fetch the JSON data from the current $URL.


Licensed by Google
* Use `jq` to extract the `results` array and append it to a temporary file, let's say `all_films.json`. Then, extract the URL for the next page from the `next` key in the JSON response.
* The loop should continue as long as the `$URL` variable is not empty.
Output success or error:

After the loop, check if the all_films.json file was created and is not empty. If it is, output a success message to stdout.

If the file is not created or is empty, output an error message to stderr and exit with a non-zero status.

Make the script executable:

Bash

chmod +x fetch_films.sh
Step 2: Create the process_films.sh Script
This script will read the all_films.json file, extract key information for each film, and save the output to a new file in a more readable format.

Create the script: Create a new file named process_films.sh.

Add the shebang and error handling: Start the script with a shebang and set -e.

Check for input file: Add a conditional statement (if) to check if all_films.json exists and is not empty. If it doesn't, print an error to stderr and exit.

Process the JSON:

Use jq to read the all_films.json file.

Pipe the output of that command to a second jq command to iterate over the array of films.

For each film in the array, extract the title, director, episode_id, and release_date.

Format the output as a clean, human-readable report. For example, a single line for each film that says something like, "Title: <title>, Episode: <id>, Directed by: <director>, Released: <date>".

Redirect this formatted output to a new file, film_report.txt.

Output success: If the processing is successful, print a message to stdout indicating the report was created.

Make the script executable:

Bash

chmod +x process_films.sh
Step 3: Create the Makefile
Automate the entire process with a Makefile. This file should define targets that perform the fetching, processing, and cleanup of your project files.

Create the file: Create a new file named Makefile.

Add a default target: Create an all target that depends on a report target.

Add a fetch target: Create a fetch target that runs the fetch_films.sh script.

Add a report target: This target should depend on fetch to ensure the data is fetched before it's processed. The recipe should run the process_films.sh script.

Add a clean target: Add a phony target clean that removes the all_films.json and film_report.txt files to reset the project. This is a crucial step for good data engineering practice.

Remember to use a tab for indentation within the Makefile's recipes.

Step 4: Run the Lab and Submit!
Run the pipeline: From your sw_api_pipeline directory, run the following command to execute the full pipeline:

Bash

make
Inspect the output: Check the film_report.txt file to ensure the data was fetched and processed correctly.

Clean up: Run the clean target to remove the generated files:

Bash

make clean
Stage, Commit, Push, and Submit:

Stage all your changes: git add .

Commit your changes: git commit -m "Completed Lab 3: SW API Pipeline"

Push your branch to GitHub: git push --set-upstream origin Lab_3

Navigate to your forked repository on GitHub, find your Lab_3 branch, and copy the URL of your sw_api_pipeline directory.

Paste the URL into the Lab 3 assignment on Canvas.

This lab should test your understanding of how to use these tools together to solve a more complex problem. Good luck! May the source be with you. 😉

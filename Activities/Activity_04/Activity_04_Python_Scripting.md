### In-Class Activity: Converting JSON to CSV with Python

**Objective:** In this activity, you will use `curl` to fetch JSON data from a public API, and then write and run a Python script to parse that JSON and convert it into a well-structured CSV file. This demonstrates how to combine Bash for data retrieval and Python for data transformation.

---

### Step 1: Get the Data 📥

First, we need some data to work with. We'll use a public API that generates random user data in JSON format. Use the `curl` command to download this data and save it to a file.

1.  **Create a new directory** for this activity and navigate into it.

    ```bash
    mkdir python_activity && cd python_activity
    ```

2.  **Use `curl`** to get the data from the API and save it to a file named `users.json`.

    ```bash
    curl -o users.json [https://randomuser.me/api?results=5](https://randomuser.me/api?results=5)
    ```

**What happened:** The `curl` command fetched a JSON file containing information for 5 random users from the specified URL. The `-o` flag told `curl` to save the output directly into a file named `users.json`.

---

### Step 2: Write the Python Script 📝

Now, we'll write a Python script that will read the JSON data you just downloaded. We'll start by reading the JSON and just printing out some of the information.

1.  **Create a new Python file** named `process_users.py`.

    ```bash
    touch process_users.py
    ```

2.  **Make the script executable** and open it for editing.

    ```bash
    chmod +x process_users.py
    ```

3.  **Copy and paste the following code** into `process_users.py`. This script will import the necessary modules, open the JSON file, and load the data into a Python dictionary.

    ```python
    #!/usr/bin/env python3

    import json

    # Open the JSON file and load the data
    with open('users.json', 'r') as f:
        data = json.load(f)

    # Get the list of users from the 'results' key
    users = data['results']

    # We will add more code here to process the data
    print("User data loaded successfully!")
    ```

---

### Step 3: Parse and Print the Data 👨‍💻

The JSON data has a nested structure. Now, let's add some code to our script to access specific fields (like first name, last name, and email) for each user.

1.  **Copy and paste the following `for` loop** to the end of your `process_users.py` file. This loop will iterate through the list of users and print out their name and email.

    ```python
    for user in users:
        first_name = user['name']['first']
        last_name = user['name']['last']
        email = user['email']

        print(f"Name: {first_name} {last_name}, Email: {email}")
    ```

2.  **Run the script** from your terminal. You should see the names and emails of the 5 random users.

    ```bash
    ./process_users.py
    ```

---

### Step 4: Transform to CSV ✨

The real power of Python is its ability to transform data into a different format. Now, let's modify the script to convert the JSON data into a clean CSV file using the built-in `csv` module.

1.  **Replace the `for` loop in `process_users.py`** with the following code. It will still read from the JSON but will now write the output to a new file in CSV format.

    ```python
    import csv

    # We will still open the JSON file here as before...
    # with open('users.json', 'r') as f:
    #     data = json.load(f)
    # users = data['results']

    # Now, open a new file to write the CSV data to
    with open('users.csv', 'w', newline='') as csv_file:
        # Define the column headers for our CSV file
        fieldnames = ['first_name', 'last_name', 'email']

        # Create a DictWriter to easily write rows from a dictionary
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Loop through the users and write each one as a row
        for user in users:
            # Create a dictionary with the data we want to write
            writer.writerow({
                'first_name': user['name']['first'],
                'last_name': user['name']['last'],
                'email': user['email']
            })

    print("CSV file created successfully!")
    ```

2.  **Run the script** again. A new file named `users.csv` will be created in your directory.

    ```bash
    ./process_users.py
    ```

3.  **View the contents** of the new file to see the clean, tabular data.

    ```bash
    cat users.csv
    ```

**What you did:** You built a simple but powerful pipeline. Bash handled the initial data retrieval, while your Python script took on the more complex job of parsing the nested data and transforming it into a structured, tabular format, ready for analysis.

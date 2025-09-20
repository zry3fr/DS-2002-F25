# Welcome to DS-2002 Windows User Setup Guide!

If you are a Windows User, you are in the right place! If you are a MacOS user, please click [here](https://github.com/austin-t-rivera/DS-2002-F25/blob/main/Setup/macOS_Users.md) to follow the MacOS User Setup Guide.

In this Setup Guide, you will find easy to navigate instructions for downloading and installing the tools you will need this semester:
- Environments ⛰️
- Languages 🗣️
- Packages 📦
- Tools 🛠️
- Etc. 🤷‍♀️

<br>

---

# Early Semester Must Haves

## Git Bash 💻
Git Bash is a command-line interface (CLI) for Windows that emulates a Unix-like shell environment. It provides essential Unix commands like `ls`, `cd`, `grep`, and a robust environment for using Git. Git Bash is important because it allows Windows users to work with the same commands and workflows as developers on macOS and Linux, which is crucial for consistency in software development and data science.

Please follow these steps and read each step carefully:
1. Download the Git Bash setup from the official website: https://git-scm.com/
2. Download the installer by clicking on "**Download for Windows**" for the **Latest Source Release**
3. Run the .exe file you just downloaded and follow the instructions in the installer.​
4. Open Git Bash by doing one of the following:
  - Open the Start menu, type "Git Bash", and the either click it to open it normally or right click and select "Run as administrator" if you need administrator privileges.
  - Open by right-clicking on any directory (folder in your file system) and selecting the **Git Bash Here** option from the context menu (i.e. right-click menu).

<br>

## Chocolatey 🍫
**Chocolatey** is a package manager for Windows. Think of it as an "app store" for the command line. It's important because it automates the process of installing, updating, and removing software from the command line. Instead of manually downloading an installer, you can use a single command like `choco install make` to automatically download and set up a program. This saves time and ensures your tools are consistently managed.

Please follow these steps and read each step carefully:
1. Open the Start menu, type "PowerShell," and right-click on it to select "Run as administrator."
2. Copy and paste the Chocolatey installation command:
```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```
3. Press Enter. This command will download and install the Chocolatey package manager. Once it finishes, you can close the PowerShell window.
4. Open Powershell back up and run:
```
choco
```
  - If everything has installed properly, you should see an output like this: `Chocolatey v2.5.1`

<br>

---

# Python, Packages, and Libraries

## Python - Programming Language 🐍
Python is a high-level, general-purpose programming language that is widely used for a variety of tasks, from web development to data science and automation. Its design emphasizes code readability and a simple, clean syntax. It's often called a "glue language" because it can easily integrate with components written in other languages, which is why it's a great tool for building pipelines with Bash.

Due to its extensive standard library and many third-party packages, Python is an incredibly versatile language. It also handles complex data structures like dictionaries and lists with ease, making it a popular choice for data-related tasks.

### Check if you have Python installed for your environment
1. Open Git Bash and run:
```
python3 --version
```
  - If a version number like `Python 3.10.6` is displayed, Python 3 is already installed. You are all set for Python!
  - If you get a `command not found` error, you need to install Python following the instructions below.

### Install Python
Windows users should use Chocolatey to manage your Python installation.
1. **Install Python**: If `python3 --version` failed, you need to run the following command in your Git Bash terminal. This will install the latest version of Python and include pip.
```
choco install python3
```
  - **Explanation**: The choco command uses Chocolatey, a popular package manager for Windows, to automatically download and install Python for you. It handles the details of adding Python to the system's PATH, which is a common source of errors.

2. **Verify the Installation**: Close and reopen the Git Bash terminal. This is a crucial step to ensure the changes to the system's PATH are recognized. Once the terminal is restarted, run the check for Python again:
```
python3 --version
```
3. Verify PIP was also installed:
```
pip3 --version
```
  - Similar to Python, you should see either a version number or an error. If you see a version number, you are all set!
4. If you are getting an error that PIP does not exist, and you have confirmed you have Python installed properly, run the following to manually download PIP.
```
python3 -m ensurepip
```
  - For more information on PIP, see below!

<br>

## PIP - Package Management System

PIP stands for "Pip Installs Packages". It is a recursive acronym, which means that the acronym itself is part of its definition. PIP is a package management system used to install and manage software packages written in Python.

### Key Principles of PIP
PIP connects to an online repository of public packages called the Python Package Index (PyPI). It can also be configured to connect to other package repositories, both local and remote, provided they comply with Python Enhancement Proposal 503. PIP is included by default in Python versions 3.4 and later, as well as Python 2.7.9 and later.

PIP is an essential tool for Python developers as it simplifies the process of managing dependencies and packages. It is recommended by the Python Software Foundation for installing Python applications and their dependencies. By understanding and utilizing PIP, developers can efficiently manage their Python environments and ensure that their projects have all the necessary dependencies.

### Why do I need both Chocolatey and PIP?
You need both a system-level package manager like `Chocolatey` and a language-specific one like `pip` because they serve different purposes.

`Chocolatey` manages applications and tools at the operating system level. They install software like web browsers, text editors, development tools (like Git), and the Python interpreter itself. Think of them as a universal app store for your computer.

`Pip` is specific to Python. Its sole job is to install, manage, and remove Python libraries and packages. These are code modules that your Python scripts use, such as `requests` for making web calls or `pandas` for data analysis.

It's good to have both because they specialize in different layers of your system. You use `Chocolatey` to install the foundation (Python), and you use `pip` to install the building blocks (libraries) that your Python code needs to run.

### PIP Usage
PIP is used through the command line interface. Here are some common commands:
- Install a package:
```
pip install package-name
```

- Uninstall a package:
```
pip uninstall package-name
```

- Install packages from a requirements file:
```
pip install -r requirements.txt
```

- List installed packages:
```
pip list
```

### Example
To install a package named `requests`, you would use the following command:
```
pip install requests
```
After installation, you can use the package in your Python code:
```
import requests

response = requests.get('https://api.github.com')
print(response.status_code)
```

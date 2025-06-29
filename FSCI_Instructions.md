# General Instructions
## How to Use the Provided Colab Notebook?
### Step 1: Open the Colab Notebook
* Click the shared link
* The notebook will open in Google Colab.
* File → Save a copy in Drive
* This creates your own editable copy, work on your copy.
### Step 2: Run the Code Cells
* Press Shift + Enter or click the play/run icon on the left of each code block to execute it.
* Make sure to run cells in order (top to bottom).
* There's no need to manually install anything, all installations and setups are already written in the notebook cells.
### Step 3: Make Your Own Changes
You’re encouraged to experiment and practice. You can:
* Change file names or file paths in the commands to work with your own data:
* Replace names or text in print/log statements if needed.
* Modify query terms, parameters, or output folders to test your understanding.
### for example in the summarisation colab notebook you will find command as
```sh
!pygetpapers --query '"wildlife" AND "biodiversity"' --pdf --limit 5 --output downloaded_file --save_query
```
here you can 
* Change the Search Terms- You can replace **"wildlife" and "biodiversity"** with your own keywords like **"phytochemicals"**
* Change the Number of Papers- you can replace *--limit* **5** to **10** or any other you want 
* Change the Output Folder Name- You can rename *--output* to any folder name you want
* Reminder: Just make sure to keep the quotation format and spacing proper when editing queries.
## Set Up Environment + Install SemanticClimate Tools
### Create a Virtual Environment
* Prerequisites- Make sure Python is installed, If not installed, download from [Download python here](https://www.python.org/downloads/)
 Check with:
```sh
python --version
```
* To create venv
 In  macOS / Linux
```sh
python3 -m venv venv
source venv/bin/activate
```
* To create venv
In windows
```sh
python -m venv venv
venv\Scripts\activate
```
* Always activate the venv before installing packages with `pip install ...`
### Install the Tools in terminal
The SemanticClimate Toolkit includes three powerful tools for working with scientific literature.
Requirements for Installing Tools with pip :
* Ensure that Python is installed on your system.
* Verify that pip is installed by running
 ```sh
  pip --version
  ```
**amilib**:
* A library for semantic analysis, extracting structured data like figures, tables, and keywords from scientific papers.
* *Developed By: Peter Murray-Rust*
* *code repository* -[amilib github](https://github.com/petermr/amilib)
* Installation - Use the below code to install amilib
```sh
pip install amilib
```
* Check the successful installation with command
```sh
amilib --help
```
**pygetpapers**:
* A command-line tool to search and download open-access papers using custom queries.
* *Developed By: Ayush Garg*
* *code repository*- [pygetpapers github](https://github.com/petermr/pygetpapers)
* Installation - Use the below code to install pygetpapers
```sh
pip install pygetpapers
```
* Check the successful installation with command
```sh
pygetpapers --help
```
**docanalysis**:
* Helps analyze and process downloaded documents, preparing them for NLP or summarization.
* *Developed By: Shweata N. Hegde*
* *code repository*- [docanalysis github](https://github.com/petermr/docanalysis)
* Installation - Use the below code to install docanalysis
```sh
 pip install docanalysis
```
* Check the successful installation with command
```sh
docanalysis --help
```
for more details you can go through the [semanticclimate tools](https://semanticclimate.github.io/p/en/tools/)
##  Common Errors & How to Fix Them
### 1. ModuleNotFoundError
**Example:**  
You encounter an error like:
```python
ModuleNotFoundError: No module named 'pygetpapers'
```
* Make sure the tool is installed inside your virtual environment
### 2. Command Not Found
**Example:**  
when you run 
```sh
pygetpapers --help
```
You encounter an error like:
```python
pygetpapers: command not found
```
* Activate the virtual environment before running the command. Or run using Python directly if it's installed as a module.
```sh
python -m pygetpapers --help
```
### 3. PermissionError
**Example:**  
You encounter an error like:
```sh
PermissionError: [Errno 13] Permission denied: '/usr/local/lib/...'
```
* Avoid installing globally without permission, instead use a virtual environment.
### 4. FileNotFoundError
**Example:**  
You encounter an error like:
```sh
FileNotFoundError: [Errno 2] No such file or directory: 'input/data.txt'
```
* Double-check the file path and spelling.
* If using Colab, make sure you've uploaded the file.
* If you uploaded a file in Colab, use the correct uploaded path.

import os
import subprocess

# input and output file path
wordlist_path = r"C:\ipcc_dict\wordlist_cp10.txt" 
ditct_path = r"C:\ipcc_dict\dict.html"


# Define amilib command
command = [
    "amilib", "DICT",
    "--words", wordlist_path,
    "--description", "wikipedia", "wiktionary", # Fetch definitions from Wikipedia & Wiktionary
    "--figures",
    "--dict", ditct_path,
    "--operation", "create"

 ]

# Run the command
try:
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    print("Dictionary crated successfully")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print("Error executing amilib command!:")
    print(e.stderr)
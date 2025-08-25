# Task

This project implements a **keyword/keyphrase extraction pipeline** using Hugging Face's `transformers` library.  
It automatically extracts the most frequent and meaningful keyphrases from a `.txt` document

### Status
## Convert HTML to TXT

### 1. Download the Chapter
First, download the required chapter from the [IPCC cleaned content repository](https://github.com/semanticClimate/ipcc/tree/main/cleaned_content).
### 2. Convert HTML to Text
Use the following Python script to extract plain text from the HTML file:

```python
from bs4 import BeautifulSoup

# Load HTML and extract text
with open("IPCC_AR6_WGII_Chapter04.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Extract text from HTML
text = soup.get_text()

# Save to a text file
with open("Chapter04_text.txt", "w", encoding="utf-8") as output:
    output.write(text)
```

This script reads the HTML file, extracts the raw text content using BeautifulSoup, and saves it as `Chapter04_text.txt`.

---

## Create Virtual Environment 

Open the terminal and execute the following commands:

### a) Create a new virtual environment
```sh
python -m venv venv
```

### b) Activate the virtual environment
```sh
venv\Scripts\activate
```

### c) Install required dependencies
```sh
pip install -r requirements.txt
```

### Required Dependencies
Ensure that your `requirements.txt` file contains the following packages:

```
transformers>=4.40.0
torch>=2.0.0
pandas>=2.0.0
tqdm>=4.65.0
```
### Clone the Repository
```
git clone https://github.com/semanticClimate/internship_sC/blob/udita/keyword_extraction
```
## Extract Keywords
Use the following command to extract keywords from your text file:
```sh
python keyword_extraction.py -t text_file_path.txt -s ./
```
### Here is the Wordlist that I got
[GitHub: semanticClimate IPCC WG1 CHAPTER5 WORDLIST](https://github.com/semanticClimate/internship_sC/blob/udita/Keyword_Extraction/top_1000_keypharses.csv)








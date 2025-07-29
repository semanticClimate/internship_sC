# Keyword Extraction for IPCC AR6 WG1 Chapter 04
## Task:
Generate a wordlist, encyclopedia, and Graphviz visualization for WG1/Chapter04 to support semantic analysis and climate research.
## Description:
This project focuses on extracting meaningful keywords from WG1/Chapter04 of the IPCC AR6 report. It includes:

- Wordlist Creation: Extract important acronyms, models (e.g., CMIP, RCP, SSP), and climate science terms using regular expressions and domain-specific filters.

- Encyclopedia Generation: Use extracted keywords to build a structured, referenced encyclopedia using amilib.

- Graphviz Visualization: Create a concept map using the extracted keywords and chapter relationships.
### Step 1: Convert HTML to Plain Text
#### a)Download Chapter HTML:
Download the cleaned HTML version of WG1/Chapter04 from [IPCC cleaned content repoistory](https://github.com/semanticClimate/ipcc/tree/main/cleaned_content)
#### b)Convert HTML to TXT:
Use this script to extract plain text from the HTML
> python extract_chapter4.py
```
from bs4 import BeautifulSoup
import re

# Load and parse HTML
with open("IPCC_AR6_WGI_Chapter04.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Extract and clean visible text
text = soup.get_text(separator=" ")
text = re.sub(r"\[\d+\]", "", text)

# Save to file
with open("Chapter04_text.txt", "w", encoding="utf-8") as output:
    output.write(text)
```
###  Step 2: Create Virtual Environment
#### a) Create Conda environment:
```
conda create -n keyword_extraction python==3.8.10
```
#### b)Activate environment
```
conda activate keyword_extraction
```
#### c)Install dependencies
```
pip install -r requirements.txt
```
> requirements.txt:
```
acidification
carbon
CMIP6
ENSO
feedback
GMST
monsoon
precipitation
RCP8.5
SSP1-2.6
temperature
warming
```
### Step 3: Extract Keywords:
Run your keyword_extractor.py file
```
python keyword_extraction.py
```
It identifies:

- Acronyms like GMST, GSAT

- Scenario identifiers like SSP2-4.5, RCP8.5

- Model references like CMIP6

- Climate-related terms like monsoon, acidification, sensitivity, etc.
The output is saved to:
```
WG1_CH04_wordlist.txt
```
### Example Output:
```
acidification
carbon
CMIP6
ENSO
feedback
GMST
monsoon
precipitation
RCP8.5
SSP1-2.6
temperature
warming
```
### Reference for Keyword Extraction Code
The keyword extraction script is based on the implementation available at:  
[GitHub: semanticClimate keyword extraction](Keyword_Extraction/scripts/keyword_extraction.py)
### Here is the Wordlist that I got
[GitHub: semanticClimate IPCC WG1 CHAPTER4 WORDLIST](Keyword_Extraction/WG1_CH04_wordlist.txt)

### Step 4: Use amilib to create a dictionary
```
pip install amilib==0.3.9
```
Use this code to create dictionary
```
amilib DICT --words your_wordlist_path.txt  --description wikipedia --dict output_dict_path.html --figures --operation create
```
edits path names accordingly.
### Here is the Wordlist that i got
[https://github.com/semanticClimate/internship_sC/blob/280886ae2fd18118fe55c4247f6cc6f4c3931bd9/Keyword_Extraction/WG1_CH04_dict.html](WG1/CH04_Dictionary)






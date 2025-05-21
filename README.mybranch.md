### MONDAY(19-05-2025)
- **Task:**  
  Run unit test scripts to identify any issues.

- **Steps Performed:**
  - Installed **PyCharm** as the development environment.
  - Cloned the repository: `amilib`.
  - Ran some test scripts( `test_html.py`,`test_headless.py`)
  - executed tests successfully with no issues found.
- **Next Steps:**
   - Execute remaining test scripts.
   - Monitor for errors, warnings, or failures.
   - Update documentation as required based on test results.               
---
### TUESDAY(20-05-2025)
  ## Task
Generate a wordlist and encyclopedia for WG2/Chapter04, and create a Graphviz visualization for the chapter.

### Description
As part of the WG2/Chapter04 project, the following objectives should be undertaken:
- **Wordlist and Encyclopedia Creation:** Extract key terms and definitions from the chapter to build a comprehensive wordlist and associated encyclopedia.
- **Graphviz Visualization:** Develop a visual representation of chapter structure or key concepts using Graphviz to enhance understanding and presentation

### Status
## Step 1: Convert HTML to TXT

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

## Step 2: Create Virtual Environment in Anaconda Navigator

Open the terminal and execute the following commands:

### a) Create a new virtual environment
```sh
conda create -n keyword_extractor python==3.8.10
```

### b) Activate the virtual environment
```sh
conda activate keyword_extractor
```

### c) Install required dependencies
```sh
pip install -r requirements.txt
```

### Required Dependencies
Ensure that your `requirements.txt` file contains the following packages:

```

certifi==2024.8.30
charset-normalizer==3.3.2
colorama==0.4.6
filelock==3.16.1
fsspec==2024.9.0
huggingface-hub==0.25.1
idna==3.10
Jinja2==3.1.4
MarkupSafe==2.1.5
mpmath==1.3.0
networkx==3.1
numpy==1.24.4
packaging==24.1
pandas==2.0.3
python-dateutil==2.9.0.post0
pytz==2024.2
PyYAML==6.0.2
regex==2024.9.11
requests==2.32.3
six==1.16.0
sympy==1.13.3
tokenizers==0.13.3
torch==2.4.1
tqdm==4.66.5
transformers==4.25.1
typing_extensions==4.12.2
tzdata==2024.2
urllib3==2.2.3
```
---

## Step 3: Extract Keywords
Use the following command to extract keywords from your text file:

```sh
python keyword_extractions.py --text_file "<path_to_your_txt_file>" --saving_path "<path_to_save_output>"
```
Replace `<path_to_your_txt_file>` with the actual path to your text file and `<path_to_save_output>` with your desired output directory.But the output mainly contains names of countries and people, not the important terms from the chapter. I’m trying to improve this using model-based methods, but it’s taking a lot of time to load and process.I have uploaded the folder with all this data in this repository named**IPCC_Keyword_Project**.

---


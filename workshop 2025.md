#bioAI Workshop


**Date:** January 23, 2025  
**Topic:** Text Summarization Using Transformers  
**Model Used:** `sshleifer/distilbart-cnn-12-6`  
**Presentation PPT:** [Here’s the markdown version of your workshop presentation details and code. You can copy and paste this into a `README.md` file in your `workshop` folder on GitHub.

---

```markdown
# Workshop: Text Summarization Using Transformers

**Date:** January 23, 2025  
**Topic:** Text Summarization Using Transformers  
**Model Used:** `sshleifer/distilbart-cnn-12-6`  
**Presentation PPT:** [Download PPT](#) *(Link to your PPT file)*  

---

## Overview
In this workshop, I presented on **Text Summarization Using Transformers**, where I demonstrated how to use the `sshleifer/distilbart-cnn-12-6` model for summarizing text. The workshop covered the following steps:

1. **Installation of Required Libraries**
2. **Importing Libraries**
3. **Initializing the Tokenizer and Model**
4. **Downloading Research Papers Using `pygetpapers`**
5. **Creating JQuery Datatables for Retrieved Articles Using `amilib`**
6. **Displaying Datatables (HTML Output)**
7. **Loading and Extracting Text from PDF**
8. **Splitting Text into Chunks**
9. **Generating Summaries for Each Chunk**
10. **Displaying the Final Summary**

---

## Code Implementation

### Step 1: Installation of Required Libraries
```bash
!pip install transformers[sentencepiece] pymupdf nltk
!pip install pygetpapers
!pip install -- amilib==0.3.9
```

### Step 2: Importing Libraries
```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import fitz  # PyMuPDF
import nltk
import re
from IPython.display import HTML, display
```

### Step 3: Initialize the Tokenizer and Model
```python
# Initialize the model and tokenizer
checkpoint = "sshleifer/distilbart-cnn-12-6"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)

# Download the necessary NLTK tokenizer
nltk.download('punkt_tab')
```

### Step 4: Download Research Papers Using `pygetpapers`
```bash
!pygetpapers --query 'A review medicinal and traditional uses on Tulsi plant (Ocimum sanctum L.)' --pdf --limit 3 --output downloaded_file --save_query
```

### Step 5: Create JQuery Datatables for Retrieved Articles Using `amilib`
```bash
!amilib HTML --operation DATATABLES --indir downloaded_file
```

### Step 6: Displaying Datatables (HTML Output)
```python
from IPython.core.display import display, HTML

# Path to the HTML file
html_file_path = '/content/downloaded_file/datatables.html'

# Read the HTML file
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Display the HTML content
display(HTML(html_content))
```

### Step 7: Loading and Extracting Text from PDF
```python
# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

# Replace with the path of your uploaded PDF file
pdf_path = "/content/downloaded_file/PMC11678315/fulltext.pdf"
file_content = extract_text_from_pdf(pdf_path)
```

### Step 8: Split the Text into Chunks
```python
# Split the text into sentences using NLTK
sentences = nltk.tokenize.sent_tokenize(file_content)

# Chunk the text based on token limits of the model
max_chunk_length = tokenizer.model_max_length  # Maximum number of tokens the model can handle
chunks = []
length = 0
chunk = ""

for sentence in sentences:
    sentence_length = len(tokenizer.tokenize(sentence))
    if length + sentence_length <= max_chunk_length:
        chunk += sentence + " "
        length += sentence_length
    else:
        chunks.append(chunk.strip())
        chunk = sentence + " "
        length = sentence_length

# Add the last chunk if there's any left
if chunk:
    chunks.append(chunk.strip())
```

### Step 9: Generate Summaries for Each Chunk
```python
# Set a maximum output length for the summary
max_output_length = 50  # You can adjust this value

# Generate summaries for each chunk
summaries = []
for chunk in chunks:
    inputs = tokenizer(chunk, return_tensors="pt", truncation=True, padding=True)
    output = model.generate(
        **inputs,
        max_length=max_output_length,
        min_length=10,
        length_penalty=0.8,
        early_stopping=True,
        no_repeat_ngram_size=3  # Ensures less repetition
    )
    decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)

    # Remove standalone numbers and decimals
    cleaned_output = re.sub(r'\b(?:figure|fig)\s*\d+', '', decoded_output)
    cleaned_output = re.sub(r'\[\d+(?:,\d+)*\]', '', cleaned_output)
    cleaned_output = re.sub(r'\d+(\.\d+)+', '', cleaned_output)

    summaries.append(cleaned_output.strip())
```

### Step 10: Display the Final Summary
```python
# Concatenate all summaries into one paragraph
final_summary = " ".join(summaries)

# Function to display the final summary vertically
def display_summary_vertically(summary, line_width=90):
    print("\n".join([summary[i:i+line_width] for i in range(0, len(summary), line_width)]))

# Display the final summary
display_summary_vertically(final_summary)
```

---

## Additional Resources
- **Presentation PPT:** [Download PPT](#) *(Link to your PPT file)*  
- **GitHub Repository:** [Workshop Repository](#) *(Link to your repository)*  

---

## Conclusion
This workshop demonstrated the power of transformer models like `sshleifer/distilbart-cnn-12-6` for text summarization. The code and steps provided can be adapted for various use cases, including research paper summarization, article summarization, and more.

---

Feel free to customize the markdown further as needed! Let me know if you need additional assistance. 😊
```](#) *(Link to your PPT file)*  

---

## Overview
In this workshop, I presented on **Text Summarization Using Transformers**, where I demonstrated how to use the `sshleifer/distilbart-cnn-12-6` model for summarizing text. The workshop covered the following steps:

1. **Installation of Required Libraries**
2. **Importing Libraries**
3. **Initializing the Tokenizer and Model**
4. **Downloading Research Papers Using `pygetpapers`**
5. **Creating JQuery Datatables for Retrieved Articles Using `amilib`**
6. **Displaying Datatables (HTML Output)**
7. **Loading and Extracting Text from PDF**
8. **Splitting Text into Chunks**
9. **Generating Summaries for Each Chunk**
10. **Displaying the Final Summary**

---

## Code Implementation

### Step 1: Installation of Required Libraries
```
!pip install transformers[sentencepiece] pymupdf nltk
!pip install pygetpapers
!pip install -- amilib==0.3.9
```

### Step 2: Importing Libraries
```
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import fitz  # PyMuPDF
import nltk
import re
from IPython.display import HTML, display
```

### Step 3: Initialize the Tokenizer and Model
```
# Initialize the model and tokenizer
checkpoint = "sshleifer/distilbart-cnn-12-6"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)

# Download the necessary NLTK tokenizer
nltk.download('punkt_tab')
```

### Step 4: Download Research Papers Using `pygetpapers`
```
!pygetpapers --query 'A review medicinal and traditional uses on Tulsi plant (Ocimum sanctum L.)' --pdf --limit 3 --output downloaded_file --save_query
```

### Step 5: Create JQuery Datatables for Retrieved Articles Using `amilib`
```
!amilib HTML --operation DATATABLES --indir downloaded_file
```

### Step 6: Displaying Datatables (HTML Output)
```
from IPython.core.display import display, HTML

# Path to the HTML file
html_file_path = '/content/downloaded_file/datatables.html'

# Read the HTML file
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Display the HTML content
display(HTML(html_content))
```

### Step 7: Loading and Extracting Text from PDF
```
# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

# Replace with the path of your uploaded PDF file
pdf_path = "/content/downloaded_file/PMC11678315/fulltext.pdf"
file_content = extract_text_from_pdf(pdf_path)
```

### Step 8: Split the Text into Chunks
```
# Split the text into sentences using NLTK
sentences = nltk.tokenize.sent_tokenize(file_content)

# Chunk the text based on token limits of the model
max_chunk_length = tokenizer.model_max_length  # Maximum number of tokens the model can handle
chunks = []
length = 0
chunk = ""

for sentence in sentences:
    sentence_length = len(tokenizer.tokenize(sentence))
    if length + sentence_length <= max_chunk_length:
        chunk += sentence + " "
        length += sentence_length
    else:
        chunks.append(chunk.strip())
        chunk = sentence + " "
        length = sentence_length

# Add the last chunk if there's any left
if chunk:
    chunks.append(chunk.strip())
```

### Step 9: Generate Summaries for Each Chunk
```
# Set a maximum output length for the summary
max_output_length = 50  # You can adjust this value

# Generate summaries for each chunk
summaries = []
for chunk in chunks:
    inputs = tokenizer(chunk, return_tensors="pt", truncation=True, padding=True)
    output = model.generate(
        **inputs,
        max_length=max_output_length,
        min_length=10,
        length_penalty=0.8,
        early_stopping=True,
        no_repeat_ngram_size=3  # Ensures less repetition
    )
    decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)

    # Remove standalone numbers and decimals
    cleaned_output = re.sub(r'\b(?:figure|fig)\s*\d+', '', decoded_output)
    cleaned_output = re.sub(r'\[\d+(?:,\d+)*\]', '', cleaned_output)
    cleaned_output = re.sub(r'\d+(\.\d+)+', '', cleaned_output)

    summaries.append(cleaned_output.strip())
```

### Step 10: Display the Final Summary
```
# Concatenate all summaries into one paragraph
final_summary = " ".join(summaries)

# Function to display the final summary vertically
def display_summary_vertically(summary, line_width=90):
    print("\n".join([summary[i:i+line_width] for i in range(0, len(summary), line_width)]))

# Display the final summary
display_summary_vertically(final_summary)
```

---


## Conclusion
This workshop demonstrated the power of transformer models like `sshleifer/distilbart-cnn-12-6` for text summarization. The code and steps provided can be adapted for various use cases, including research paper summarization, article summarization, and more.


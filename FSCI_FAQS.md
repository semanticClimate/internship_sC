# Semantic Climate Tools – Basic FAQ
## Topics Covered :
a. PyGetPapers
b. AMILIB
c. AMIClimate
d. DocAnalysis
e. LLMRAG


1. What is the main purpose of Semantic Climate tools?
   > They help researchers download, analyze, and query climate science papers using AI.
2.  What tools are included?
 - PyGetPapers: Download papers from arXiv/Crossref.
 - AMLIB: Manage metadata (titles, authors, etc.).
 - AMIClimate: Analyze climate-specific content.
- DocAnalysis: Extract tables/figures from PDFs.
- LLMRAG: AI-powered Q&A over climate papers.
3. How do I install these tools?
```
pip install pygetpapers amlib amiclimate docanalysis
git clone https://github.com/semanticClimate/llmrag.git
cd llmrag && pip install -r requirements.txt
```
4.  What are the basic requirements?
- Python 3.8+
- Git (to clone LLMRAG)
- PIP updated (pip install --upgrade pip)
## Setup & Common Errors:
5. I get "ModuleNotFoundError" in Windows. How to fix?
- Step 1: Check if the module is installed (pip list).
- Step 2: If missing, install it (pip install module_name).
- Step 3: If the error persists, try:
  ```
  python -m pip install module_name  # Forces correct Python env
  ```
6. PyGetPapers fails with "SSL Error" on Windows.<br> Run:
```
pip install certifi  # Update certificates
set REQUESTS_CA_BUNDLE=C:\Python39\Lib\site-packages\certifi\cacert.pem
```
7. LLMRAG gives "CUDA not found" errors (GPU issue).
<br>Use CPU mode:
```
python run_llmrag.py --device cpu  # Forces CPU usage
```
8. "SyntaxError" when running scripts.
>  Ensure you’re using Python 3.8+ (check with python --version).
9. How to resolve "Permission Denied" errors on Linux/Mac?
<br> Use sudo or fix permissions:
```
sudo chown -R $USER /path/to/project
```
## How to Run the Tools
10.  How to download climate papers with PyGetPapers?
```
docanalysis --input ./papers/ --output ./tables/ --extract_tables
```
11. How to extract tables from PDFs with DocAnalysis?
```
docanalysis --input ./papers/ --output ./tables/ --extract_tables
```
12. How to ask questions about papers with LLMRAG?
```
 python llmrag.py --query "What are impacts of sea level rise?" --corpus ./papers/
```
13. How to clean metadata with AMLIB?
```
amlib --input ./papers/metadata.csv --output ./cleaned_metadata.csv
```
14. How to filter climate papers with AMIClimate?
```
amiclimate --input ./papers/ --filter --output ./climate_papers/
```
## Troubleshooting Checklist:
15. If Tool won’t run after installation?
- Check Python version (python --version).
- Reinstall (pip uninstall tool && pip install tool).
- Restart your terminal/IDE.
16. "API limit reached" in PyGetPapers.
 <br>Use your own API key:
```
pygetpapers -q "..." --api_key YOUR_CROSSREF_KEY
```
17. LLMRAG is slow?
<br> Use smaller models ``` --model tiny-bert ``` or reduce corpus size.
18. DocAnalysis crashes on large PDFs?
 <br>Split PDFs first ``` pdfseparate input.pdf output_%d.pdf ```.
20.  "Out of memory" error?
<br>  Run tools with ``` --batch_size 10 ```(process fewer files at once).
### General 
- Setup: pip install + Git clone.
- Fix Errors:

> ModuleNotFound → Reinstall.

> SSL/API → Update certificates/keys.

> GPU → Use --device cpu.
21. Do I need to install anything before these tools?
<br>  Just Python 3.8+ and Git. Install them from:
- python.org
- git-scm.com
22. How to check if Python is installed correctly?
  <br>Run in Command Prompt:
  ```
  python --version
  ```
  If you see Python 3.8 or higher, you're good to go.
23. : The tool says "command not found" after installation?
  <br> Try:
  ``` python -m pygetpapers --help  # Replace with your tool name ```
  (This bypasses PATH issues on Windows/Mac.)
24. How to download 100 climate papers quickly?
  ``` pygetpapers -q "climate change" -o ./papers --limit 100```
25.  Where do downloaded files go?
<br>In the folder you specify after ``` -o``` (e.g.,``` ./papers``` in the example above).
26. How to ask LLMRAG about a paper I downloaded?
  <br> Point it to the paper's folder:
  ```python llmrag.py --query "What methods did this study use?" --corpus ./papers/paper1.pdf```
27. Can I analyze multiple PDFs at once?
  <br> Yes! Point to a folder:
  ``` docanalysis --input ./papers/ --output ./results/```
 ### Common Errors & Fixes
 28. "No module named 'nltk'" error?
<br> Install missing dependencies:``` pip install nltk```
29. Tool crashes immediately on Windows?
<br>Try:
Open Command Prompt as Admin.

Run:```
  python -m pip install --upgrade pip setuptools wheel```
30. "SyntaxError: invalid syntax" when running scripts?
  <br>You might be using Python 2. Check version with ```python --version``` and install Python 3+ if needed.
31.  PyGetPapers gets stuck at "Downloading..."?
<br>Press `Ctrl+C` to stop, then retry with fewer papers `--limit 10`.
32. "File not found" error even though the file exists?
<br>Use full paths (e.g., ```C:/Users/name/papers/```) or move files to your current folder.
### Tool-Specific Tips:
33. How to stop DocAnalysis after 10 PDFs?
<br> Use:
```docanalysis --input ./papers/ --limit 10```
34. Can LLMRAG read DOCX files?
<br>Not directly. Convert to PDF first or extract text with `pandoc`.
35. PyGetPapers gives "403 Forbidden" errors.
<br>Wait 1 hour (API rate limit) or use ```--api_key YOUR_KEY```.
36. How to see all AMIClimate options?
<br> Always check help:
```amiclimate --help```
### For Absolute Beginners:
37. I'm new to Python. Can I still use these?
<br> Yes! Just copy-paste the commands we provided.
38. What's the FIRST thing I should try?
<br>Start small:
``` pygetpapers -q "climate" -o ./test --limit 3 ```Then check the ./test folder.
39. How to uninstall if something goes wrong?
``` pip uninstall pygetpapers  # Replace with tool name ```
40. Where can I learn more?
<br>Visit:
- Semantic Climate [https://semanticclimate.github.io/p/en/]
41.  What is LLMRAG in the context of Semantic Climate?
<br>LLMRAG, or Large Language Model - Retrieval Augmented Generation, refers to the application of RAG principles to climate documents within the Semantic Climate framework. It involves using LLMs to generate answers by first retrieving relevant information from a knowledge base (our semantically enriched climate data) rather than relying solely on the LLM's pre-trained knowledge.
42. How does LLMRAG generally work?
<br>In a typical RAG pipeline, when a user asks a question:
- The question is used to retrieve relevant documents or passages from a knowledge base (e.g., a vector store containing IPCC data).
- The retrieved context, along with the original question, is fed to an LLM.
- The LLM then generates an answer based on the provided context.
43.  What is pygetpapers?
  <br>pygetpapers is a Python library developed by Semantic Climate that allows automated searching and downloading of scientific literature from various open-access repositories using textual queries and metadata. It's designed for bulk download and is extensible to new repositories.
44. What are the main functionalities of pygetpapers?
  <br>pygetpapers can:

- Query scientific literature repositories using various search terms and metadata (e.g., dates, authors).

- Download full-text articles and associated metadata in bulk.

- Handle cursor-based API querying for large result sets.

- Store metadata as JSON in a structured CProject directory, and individual article metadata in CTrees.
45. What is amiclimate?
  <br>amiclimate refers to the overall NLP and semantic software and material developed by the Semantic Climate project for managing climate knowledge. It encompasses the broader set of Python code and methodologies for accessing and transforming key climate documents, particularly the IPCC reports.
46. What are the main objectives of amiclimate?
  <br>The main objectives of amiclimate are to:

- Convert IPCC documents (and other climate-related texts) from PDF into semantic HTML and XML.

- Extract and analyze terms, their usage, and meaning within these documents.

- Link these terms to existing knowledge bases (like Wikidata) to build enriched dictionaries.

- Develop tools for effective navigation, search, and display of this semantically enhanced climate information.
46. What kind of "material" does amiclimate include besides software?
  <br>Beyond Python code, amiclimate includes "material" such as:

- Analyzed IPCC chapters (e.g., wordlists, dictionaries in XML and semantic HTML).

- Tutorials and documentation for using the tools.

- Project reports and summaries from interns.
47. Does amiclimate directly handle PDF conversion?
  <br>While ` amiclimate` is the overarching framework, the actual PDF parsing and content extraction might be handled by specialized components or integrated libraries within `amiclimate`, or by external tools that `amiclimate` orchestrates.
48. What are "wordlists" and "dictionaries" in the context of amiclimate?
  - **Wordlists:** Lists of terms extracted from IPCC chapters, often with their frequencies and locations.
  - **Dictionaries:** More structured collections of these terms, potentially with definitions, relationships to other terms, and links to external knowledge bases (like Wikidata IDs). These are a key product of the amiclimate effort.
  49. Does amiclimate offer any tutorials for new users or contributors?
    <br> Yes, the Semantic Climate project's website and GitHub repositories often feature tutorials, such as "Introduction to amilib: Tutorial" (which might be part of the amiclimate documentation), and guides for contributing to the project.
 50.  What is docanalysis?
  <br>docanalysis is a Command Line Tool developed by the Semantic Climate project for carrying out text analysis of documents, particularly corpora organized as CProjects. It performs various NLP and text-mining operations, including sectioning, dictionary generation, and entity extraction.
51. What are the primary functions of docanalysis?
<br>docanalysis focuses on:
- **Sectioning:** Splitting documents into logical sections (e.g., sentences, paragraphs).

- **NLP/Text-mining:** Applying various natural language processing techniques.

- **Dictionary Generation:** Creating word and term dictionaries from the analyzed text.

- **Entity Extraction and Annotation:** Identifying and annotating specific entities within the text
52. What are "CProjects" in the context of docanalysis?
  <br>In docanalysis, "CProjects" refer to corpora (collections of documents) that have been previously processed and organized, often by tools like `pygetpapers`, into a standardized directory structure. docanalysis then ingests these CProjects for further analysis.
53. What is a "virtual environment" and why is it important for these tools?
<br>A virtual environment `venv` is an isolated Python environment that allows you to install project-specific dependencies without interfering with other Python projects or your system's global Python installation. It's crucial for managing dependencies and avoiding conflicts, ensuring the tools run smoothly.
54. How do I create and activate a virtual environment?
<br> To create: python3 -m venv my_env (replace my_env with your desired name).
  <br>To activate:
- On Windows: `my_env\Scripts\activate`
- On macOS/Linux: `source my_env/bin/activate`
55. What are the general hardware/software requirements to run these tools?
  - Operating System: Linux, macOS, or Windows.
- Python: Python 3.7+ is generally recommended.
- RAM: Sufficient RAM for processing large text corpora (e.g., 8GB+ is a good starting point, more for LLMs).
- Disk Space: Enough space to store downloaded documents and generated outputs.
- Internet Connection: Required for pygetpapers to access online repositories and for LLM APIs (if used externally).
- Optional (for LLMs): GPU access might be beneficial for training or fine-tuning large models, but inference can often run on CPU.
  
56. Do I need programming experience to use these tools?
<br>Basic command-line familiarity is helpful for `pygetpapers` and `docanalysis`. For more advanced use or contributions, Python programming skills are essential. However, the project also welcomes non-programmers for content-based tasks.

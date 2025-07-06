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
6. PyGetPapers fails with "SSL Error" on Windows.
  Run:
```
pip install certifi  # Update certificates
set REQUESTS_CA_BUNDLE=C:\Python39\Lib\site-packages\certifi\cacert.pem
```
7. LLMRAG gives "CUDA not found" errors (GPU issue).
Use CPU mode:
```
python run_llmrag.py --device cpu  # Forces CPU usage
```
8. "SyntaxError" when running scripts.
>  Ensure you’re using Python 3.8+ (check with python --version).
9. How to resolve "Permission Denied" errors on Linux/Mac?
 Use sudo or fix permissions:
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
 Use your own API key:
```
pygetpapers -q "..." --api_key YOUR_CROSSREF_KEY
```
17. LLMRAG is slow?
 Use smaller models > --model tiny-bert or reduce corpus size.
18. DocAnalysis crashes on large PDFs?
 Run tools with --batch_size 10 (process fewer files at once).
 
     

### MONDAY(02-06-2025)
## Task:Test Execution in amilib & pygetpapers

### Steps Performed:
- Installed **PyCharm** and cloned the **amilib** repository.
- Ran **amilib** on local system (Windows, latest Python version):
  - Encountered **Keras installation errors**; informed **Peter**.
  - Some issues resolved, errors reduced.
- Ran **pygetpapers** successfully.
- Selected **WG1 Chapter 4** for analysis: *Future Global Climate Scenario-Based Projections and Near-Term Information*.

### Next Steps:
- Continue working on **WG1 Chapter 4**.
- Ensure **amilib** and **pygetpapers** run successfully on latest system versions.
- Execute remaining **amilib** test scripts and monitor for issues.
- Update documentation as required.

### TUESDAY(03-06-2025)
## Task: Running pygetpapers after cloning the latest repository from GitHub, Checkout branch pmr_datatables and code input 
```python -m pygetpapers.pygetpapers --query '"wildlife" AND "biodiversity"' --pdf --limit 5 --output downloaded_file --api openalex```
## Output:
- Ran successfully for 5 papers and got pdfs
- Ran for 50 papers successfully and got pdfs
python -m pygetpapers.pygetpapers --query '"wildlife" AND "biodiversity"' --pdf --limit 50 --output downloaded_file --api openalex 
<frozen runpy>:128: RuntimeWarning: 'pygetpapers.pygetpapers' found in sys.modules after import of package 'pygetpapers', but prior to execution of 'pygetpapers.pygetpapers'; this may result in unpredictable behaviour
```INFO: Making Request to OpenAlex
https://api.openalex.org/works?search=wildlife AND biodiversity&cursor=*&per-page=20
https://api.openalex.org/works?search=wildlife AND biodiversity&cursor=IlsyNzMuMzMxNjcsIDEzMDQyOTQ0MDAwMDAsICdodHRwczovL29wZW5hbGV4Lm9yZy9XMjE0MjIxMTQxMiddIg==&per-page=20
https://api.openalex.org/works?search=wildlife AND biodiversity&cursor=IlsyMTQuOTA5MTIsIDEyNjE0NDAwMDAwMDAsICdodHRwczovL29wZW5hbGV4Lm9yZy9XMjE2NzE5NTExNCddIg==&per-page=20
WARNING: no paper_key for id=https://openalex.org/W1252137655
WARNING: no paper_key for id=https://openalex.org/W641944307
INFO: Downloading Pdfs for papers
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 48/48 [00:53<00:00,  1.11s/it]
INFO: Wrote metadata file for the query
INFO: Writing metadata file for the papers at C:\Users\manda\OneDrive\문서\Semantic Climate\pygetpapers\downloaded_file
 60%|█████████████████████████████████████████████████████████████████████████████████████▏                                                       | 29/48 [00:00<00:00, 289.71it/s]WARNING: Could not write metadata file for the paper 30
WARNING: Could not write metadata file for the paper 40
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 48/48 [00:00<00:00, 304.49it/s]  what does this mean did i got the required pdfs```
```
### WEDNESDAY(04-06-2025)
## Tasks Performed :
- Running amilib after cloning the latest repository from GitHub, Checkout branch pmr2025may and testing.
- Solved few error by myself.

### THURSDAY(05-06-2025)
## Tasks performed: 
- Gone through LLM-RAG colab notebook
- Ran pygetpapers and get an overview
  ## Output:
  pygetpapers output and commands list after runing in commandline

  C:\Users\manda>pygetpapers
```
usage: pygetpapers [-h] [--config CONFIG] [-v] [-q QUERY] [-o OUTPUT] [--save_query] [-x] [-p] [-s] [-z]
                   [--references REFERENCES] [-n] [--citations CITATIONS] [-l LOGLEVEL] [-f LOGFILE] [-k LIMIT] [-r]
                   [-u] [--onlyquery] [-c] [--makehtml] [--synonym] [--startdate STARTDATE] [--enddate ENDDATE]
                   [--terms TERMS] [--notterms NOTTERMS] [--api API] [--filter FILTER]

Welcome to Pygetpapers version 1.2.5. -h or --help for help

..................
```
### FRIDAY(06-06-2025)
## Tasks Performed :
- Gone through Anna rahr LLM-RAG model and tried it out
- Manually gone through WG1 Chspter4 to get an idea about further process
- Gone through read me file of pygetpapers
## Next Steps:
- Will start working on creating a wordlist for the report.

### MONDAY(09-06-2025)
## Tasks Performed :
- Attended The Research AI meeting by NIPGR.

### TUESDAY(10-06-2025)
## Tasks Performed :
- Attended The Research AI meeting by NIPGR.

### WEDNESDAY(11-06-2025)
## Tasks Performed :
- Manually gone through "AR6/WG1/ Chapter 4 :Future Global Climate.
- Saw tutorials of semantic tools for further process.
- Proposed an IDEA:
 ## Proposal:
 **"AI-Powered Chatbot and Voice Assistant"** for Semantic Climate 

 ```
 [ I would like to propose the development of an AI-powered chatbot and voice assistant for Semantic Climate that serves as an interactive guide for new interns,    visitors, and collaborators. The goal is to streamline knowledge transfer and improve orientation by providing easy access to the following information:
  - Ongoing and completed projects by Semantic Climate interns
  - Founders' vision and core objectives
  - Past publications and research contributions
  - A startup guide for new interns
  A compiled and searchable list of IPCC records and reports already worked on, to prevent duplication of effort

   Additionally, by incorporating multilingual support—including both local and international languages—this assistant can help people from diverse linguistic        backgrounds understand the projects and resources in their preferred language. This fosters greater inclusivity and global collaboration within the Semantic       Climate community.

   This system would offer a conversational interface—both text and voice-based—to make the onboarding experience more engaging and informative, while also           reducing redundant work and saving valuable time for both interns and mentors. ]
```
### THURSDAY(12-06-2025)
## Tasks Performed :
- Have researched about "How to develop AI-powered chatbot"
- Saw few tutorials and notebooks in semantic climate for working on ipcc report
- Working on wg1/chapter 4 :Future Global Climate
- Ran pygetpapers
  # Output:
```
  ========================= short test summary info =========================
FAILED tests/_test.py::test_eupmc_does_update_work - assert (5 + 10) == 5
FAILED tests/_test.py::test_does_zip_work - assert False
FAILED tests/_test.py::test_does_supplementary_work - assert False
FAILED tests/_test.py::test_does_arxiv_work - assert False == True
================= 4 failed, 7 passed in 72.67s (0:01:12) ==================
```

### FRIDAY(13-06-2025)
## Tasks Performed :
- Ran amilib and some errors tried to solve them 
- Ran pytest and tried to resolve them in my local system
- Have researched about "How to develop AI-powered chatbot"

### MONDAY(16-06-2025)
## Tasks Performed :
- Created an issue on errors when tested amilib from main branch
- Ran pytest and got 3 assertion errors
- Have researched about "How to develop AI-powered chatbot"
- Gone through ar6/wg1/chapter 4 to create a word list

  ### TUESDAY(17-06-2025)
## Tasks Performed :
- Rerun the updated pygetpapers
- Gone through ar6/wg1/chapter 4 to create a word list.
### WEDNESDAY(18-06-2025)
- Facing issue with keyword_extraction.py for creating wordlist for WG1 CHAPTER4 
- Tried solving that
### THURSDAY(19-06-2025)
- Gone through LLM-RAG disscussion created by Peter sir
- Tried to understand the functioning
- Registered for FSCI Scholarship Program
### FRIDAY(20-06-2025)
- Learned about Transformers and LLM functionality
- Gone through LLM-RAG disscussion created by Peter sir
- Created a wordlist for ar6/wg1/ch4
- ```
  https://github.com/semanticClimate/internship_sC/tree/Deepika/Keyword_Extraction
  ```
- Should make the folders in order to submit.
### MONDAY(23-06-2025)
## Tasks Performed:
- Ran llmrag from
   ```
  git clone https://github.com/semanticClimate/llmrag/blob/main/README.md#test
   ```
- Conclusion: All tests ran successfully.
- Reported the result in discussions.

  ### TUESDAY(24-06-2025)
  ## Tasks Performed:
  - Ran llmrag and worked by incorporating it with my WG1/CH04.
  - Got some errors and reported in llmrag discussions.
  - Resolved errors of llmrag test myself and successfully ran.

  ### WEDNESDAY(25-05-2025)
  ## Tasks Performed :
  - Ran the updated version of llmrag and did pytest
  - Got 6 errors mostly-syntax errors, import error.
  - Reported in discussion page of llmrag.




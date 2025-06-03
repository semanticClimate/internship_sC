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

### Tuesday(03-06-2025)
## Task: Running pygetpapers after cloning the latest repository from GitHub, Checkout branch pmr_datatables and code input 
```python -m pygetpapers.pygetpapers --query '"wildlife" AND "biodiversity"' --pdf --limit 5 --output downloaded_file --api openalex```
## Output:
- <frozen runpy>:128: RuntimeWarning: 'pygetpapers.pygetpapers' found in sys.modules after import of package 'pygetpapers', but prior to execution of 'pygetpapers.pygetpapers'; this may result in unpredictable behaviour
INFO: Making Request to OpenAlex
https://api.openalex.org/works?search=wildlife AND biodiversity&cursor=*&per-page=20
INFO: Downloading Pdfs for papers
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 5/5 [00:00<00:00, 61500.06it/s]
INFO: Wrote metadata file for the query
INFO: Writing metadata file for the papers at C:\Users\manda\OneDrive\문서\Semantic Climate\pygetpapers\downloaded_file
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 5/5 [00:00<00:00, 352.53it/s] 

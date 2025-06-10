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
## Task: Running amilib after cloning the latest repository from GitHub, Checkout branch pmr2025may and testing.
## Output:
```============================ short test summary info =============================
FAILED test/test_bib.py::AmiCorpusTest::test_get_column_from_data_tables - AssertionError: assert 'wg1\\Chapter...with_ids.html' == 'wg1/Chapter0...with_...
FAILED test/test_extract_text.py::ExtractTextTest::test_extract_title_id_para_from_
ipcc_syr - UnicodeEncodeError: 'charmap' codec can't encode character '\u2265' in positio...
FAILED test/test_extract_text.py::ExtractTextTest::test_extract_title_id_para_from_
ipcc_wg123 - UnicodeEncodeError: 'charmap' codec can't encode character '\u2212' in positio...
FAILED test/test_extract_text.py::ExtractTextTest::test_extract_title_id_para_from_makespace - AssertionError: assert False
FAILED test/test_extract_text.py::ExtractTextTest::test_keybert_ipcc_wg1 - UnicodeEncodeError: 'charmap' codec can't encode character '\u0117' in positio...
FAILED test/test_file.py::File0Test::test_list_children - AssertionError: assert ['C:\\Users\\...files\\file1'] == ['/Users/pm28..._file...
FAILED test/test_file.py::File0Test::test_relative_pathname - AssertionError: assert 'd\\e.txt' == 'd/e.txt'
FAILED test/test_graph.py::AmiGraphTest::test_chapter_graph - graphviz.backend.execute.ExecutableNotFound: failed to execute WindowsPath('do...
FAILED test/test_graph.py::AmiGraphTest::test_create_report - graphviz.backend.execute.ExecutableNotFound: failed to execute WindowsPath('do...
FAILED test/test_graph.py::AmiGraphTest::test_extract_toc_graph_from_report_toplevel - AttributeError: 'HtmlEditor' object has no attribute 'html_elem'
FAILED test/test_graph.py::AmiGraphTest::test_graphviz2 - graphviz.backend.execute.ExecutableNotFound: failed to execute WindowsPath('do...
FAILED test/test_graph.py::AmiGraphTest::test_strip_single_child_divs - AttributeError: type object 'HtmlLib' has no attribute 'remove_single_child_di...
FAILED test/test_graph.py::AmiGraphTest::test_toc_workflow - AttributeError: 'HtmlEditor' object has no attribute 'html_elem'
FAILED test/test_graph.py::AmiGraphTest::test_toc_workflow1 - AttributeError: 'HtmlEditor' object has no attribute 'html_elem'
FAILED test/test_headless.py::DriverTest::test_download_ancillary_html - selenium.common.exceptions.InvalidSessionIdException: Message: invalid session...
FAILED test/test_headless.py::DriverTest::test_download_ipcc_syr_longer_report - selenium.common.exceptions.NoSuchWindowException: Message: no such window: tar...    
FAILED test/test_headless.py::DriverTest::test_download_syr_annexes_and_index - selenium.common.exceptions.InvalidSessionIdException: Message: invalid session...     
FAILED test/test_headless.py::DriverTest::test_download_wg1_chapter_1 - selenium.common.exceptions.InvalidSessionIdException: Message: invalid session...
FAILED test/test_headless.py::DriverTest::test_download_wg2_cross_chapters - selenium.common.exceptions.InvalidSessionIdException: Message: invalid session...        
FAILED test/test_ipcc.py::TestIPCC::test_add_ipcc_hyperlinks_curly - NameError: name 'CURLY_RE' is not defined
FAILED test/test_ipcc.py::TestIPCC::test_cmdline_download_sr_reports - ValueError: bad command arguments SystemExitFail_2 (see log output)
FAILED test/test_ipcc.py::TestIPCC::test_cmdline_search - ValueError: bad command arguments SystemExitFail_2 (see log output)
FAILED test/test_ipcc.py::TestIPCC::test_commandline_search - AssertionError: assert False
FAILED test/test_ipcc.py::TestIPCC::test_commandline_search_with_filename_wildcards_and_join_indir - AssertionError: assert False
FAILED test/test_ipcc.py::TestIPCC::test_commandline_search_with_indir - AssertionError: assert False
FAILED test/test_ipcc.py::TestIPCC::test_commandline_search_with_wildcards - AssertionError: assert False
FAILED test/test_ipcc.py::TestIPCC::test_download_wg_chapter_spm_ts_IMPORTANT - AssertionError: ElementTree not initialized, missing root
FAILED test/test_ipcc.py::TestIPCC::test_download_wg_chapter_spm_ts_using_dict_IMPO
RTANT - selenium.common.exceptions.NoSuchWindowException: Message: no such window: tar...
FAILED test/test_ipcc.py::TestIPCC::test_faq_xpath - ValueError: bad command arguments SystemExitFail_2 (see log output)
FAILED test/test_ipcc.py::TestIPCC::test_output_bug - ValueError: bad command arguments SystemExitFail_2 (see log output)
FAILED test/test_ipcc.py::TestIPCC::test_parse_kwords - ValueError: bad command arguments SystemExitFail_2 (see log output)
FAILED test/test_ipcc.py::TestIPCC::test_pdfplumber_doublecol_create_pages_for_WGs_
HACKATHON - AssertionError: json dict should exist C:\Users\manda\OneDrive\문서\Semantic C...
FAILED test/test_ipcc.py::TestIPCC::test_search_with_xpaths - OSError: Error reading file 'C:\Users\manda\OneDrive\문서\Semantic Climate\ami...
FAILED test/test_ipcc.py::TestIPCC::test_strip_decorations_from_raw_expand_wg3_ch09_old - AssertionError: assert False
FAILED test/test_ipcc.py::TestIPCC::test_symbol_indir - ValueError: bad command arguments SystemExitFail_2 (see log output)
FAILED test/test_ipcc.py::TestIPCC::test_symbolic_xpaths - ValueError: bad command arguments SystemExitFail_2 (see log output)
FAILED test/test_wikimedia.py::WikipediaTest::test_insert_br_for_lone_period - TypeError: Argument '_parent' has incorrect type (expected lxml.etree._Element...      
FAILED test/test_xml.py::Xml0Test::test_skeleton_html - TypeError: Argument '_parent' has incorrect type (expected lxml.etree._Element...
= 38 failed, 396 passed, 88 skipped, 1 xfailed, 10575 warnings in 1176.60s (0:19:36) =

```
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






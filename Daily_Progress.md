## WEDNESDAY(4-6-2025)
* started to work on the graphviz for chapter 4
* Opened the Colab notebook shared by the team. Ran all cells to ensure the full workflow is good
* Modified the paper count limit from **15** to **50** to test batch downloads.
* Customized the search query, the notebook worked successfully with all changes.
## TUESDAY(3-6-2025)
* Successfully ran `pygetpapers` from the command line after cloning the latest repository from GitHub.
* Checked out the `pmr_datatables` branch and executed the following command:
  ```bash
  python -m pygetpapers.pygetpapers --query "\"wildlife\" AND \"biodiversity\"" --pdf --limit 5 --output downloaded_file --api openalex
* The PDFs were downloaded successfully.
## MONDAY(2-06-2025)
* Created a wordlist and dictionary for IPCC WG2 Chapter 4. 
* The final wordlist for the chapter [GitHub: wordlist](https://github.com/semanticClimate/internship_sC/blob/Haarthi/Keyword_Extraction/IPCC-Ch04-Wordlist)
* the dictionary corresponding to the wordlist [GitHub: Dictionary](https://github.com/semanticClimate/internship_sC/blob/Haarthi/wg2chap04_dict.html)
* Attempted to run pytest on the amilib repository.
* Encountered and reported errors in the amilib repo; discussed these issues during the meeting.
## Friday(30-05-2025)
* While extracting keywords from the chapter, nearly 6000 words were retrieved.
* Began automating the cleaning process to remove irrelevant or simple words.
* Fixed import errors and reran pytest successfully.
* Learned about different types of Python errors and debugging techniques.
## Thursday(29-05-2025)
* Created a dictionary from the wordlist using the command line.
Added the corresponding HTML file to the repository: [GitHub: html file for dictionary](https://github.com/semanticClimate/internship_sC/blob/Haarthi/wg2chap04_dict.html)
## WEDNESDAY (28-05-2025)
* Started building the dictionary.
* Faced issues with amilib: the code failed to extract information from Wikipedia when run in Google Colab, especially for figures.
* Explored how to run pytest on amilib and encountered some import errors.
## TUESDAY(27-05-2025)
Documented the process for extracting the keywords.[GitHub: semanticClimate process for extracting keywords](https://github.com/semanticClimate/internship_sC/blob/Haarthi/Keyword_Extraction_Process.md)
Here is the Wordlist that I got
[GitHub: semanticClimate IPCC WG2 CHAPTER4 WORDLIST](https://github.com/semanticClimate/internship_sC/blob/Haarthi/Keyword_Extraction/keyphrases.csv)
## MONDAY(26-05-2025)
* Successfully extracted keywords from IPCC WG2 AR6 Chapter 4 (Water).
* Reviewed the output to filter out irrelevant or simple terms.
* Began work on building the dictionary.
## FRIDAY(23-05-2025)
* Used YAKE for keyword extraction.
* Generated a wordlist and attached it under *Keyword_Extractor*.
* However, the extracted terms still lacked relevance to the core chapter content.
### THURSDAY(22-05-2025)
* Explored various keyword extraction models such as KeyBERT and YAKE.
* Experimented with their outputs for improved relevance.
## WEDNESDAY(21-05-2025)
tried to fix the problem, used [GitHub: semanticClimate keyword extraction](https://github.com/petermr/semanticClimate/blob/main/keyword_extraction/code_v2/keyword_extraction_v2_test.py)
but got the output as empty file. I replaced the model in this to another but it has its own drawbacks
## TUESDAY(20-05-2025)
* Initial attempts at keyword extraction from IPCC WG2 AR6 Chapter 4 resulted in mostly country and people names.
* Began improving this using model-based methods, though processing time was significantly high.
## MONDAY(19-05-2025)
- *Task:*  
  Run unit test scripts to identify any issues.
- *Steps Performed:*
  - Installed *PyCharm* as the development environment.
  - Cloned the repository: amilib.
  - Ran some test scripts, executed tests successfully with no issues found.
- *Next Steps:*
   - Execute remaining test scripts.
   - Monitor for errors, warnings, or failures.
   - Update documentation as required based on test results.               


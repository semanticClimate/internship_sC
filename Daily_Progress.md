## TUESDAY(24-6-2025)
* gone through the meeting recordings as i couldn't be able to attend the meeting on monday to keep updated
* gone through readme file and ran the llmrag test and ran it successfully
* updated the report on llmrag discussions and on slack
* added my details in the spreadsheets(included my chapters, report of llmrag test) 
## FRIDAY(20-6-2025)
* Tried to know about the github actions and how it works
* understood about the tests written in llmrag
* Gone through llmrag
* cloned the llmrag repository
## THURSDAY(19-6-2025)
* gone through the llmrag and tried to understand the files included in it
* got to know what exactly each file consists of and about what it does.
## WEDNESDAY(18-6-2025)
* created a .env file placed my open api key, and can't use kisski_url because it is private, so i replaced it with `KISSKI_URL=https://api.openai.com/v1/`
* and replaced models as
```sh
 LLAMA =  'gpt-3.5-turbo'
 GEMMA = 'gemma-3-27b-it'
```
and ran the command 
```sh
python ipcc_rag.py --model LLAMA --rebuild
```
i got the error as 
```sh
PS C:\Users\Dell\Anna's RAG\KISSKI-RAG-4-IPCC> python ipcc_rag.py --model LLAMA --rebuild
Loaded 1 document(s).
Generating chunks...
Generated 329 chunks.
1 in 4.8s (0.21/s)
Creating index...
1 in 43.7s (0.02/s)
Index stored in ./faiss_index
Enter your question (or type 'q' to quit): name some islands near india?
Traceback (most recent call last):
File "C:\Users\Dell\Anna's RAG\KISSKI-RAG-4-IPCC\ipcc_rag.py", line 221, in <module>
ask_question(index, ask_openai_llm)
File "C:\Users\Dell Anna's RAG\KISSKI-RAG-4-IPCC\ipcc_rag.py", line 206, in ask_question
answer = ask_openai_1lm(full_prompt)
File "C:\Users\Dell\Anna's RAG KISSKI-RAG-4-IPCC\ipcc_rag.py", line 175, in ask_openai_1lm
openai.RateLimitError: Error code: 429 {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', 'type': 'insufficient_quota', 'param": None, 'code': 'insufficient_quota'}} PS C:\Users\Dell\Anna's RAG KISSKI-RAG-4-IPCC>
```
## TUESDAY(17-6-2025)
* Had to uninstall Ollama because the system wasn’t responding properly and kept getting stuck due to insufficient memory while running the model setup.
* figuring out how I can run the ipcc_rag.py file with available resources 
## MONDAY(16-6-2025)
* while installing the requirements when working on anna's RAG model `ipcc_rag_local.py`, it showed an error saying system configuration isn't supported and much memory is required than available
```sh
raise ConnectionError(CONNECTION FRROR MESSAGE) from None
ConnectionError: Failed to connect to Ollama. Please check that Ollama is downloaded, running and accessible: https://ollama.com/download
```
while installing ollama the following error is encountered
```sh
Error: model requires more system memory (5.9 GiB) than is available (4.1 GiB)
```
## FRIDAY(13-6-2025)
* ran pytest on amilib and checked if there are any new errors
* started to work on anna's RAG model
* installed some requirements required
* looked into the models used in the code and got an overview
## THURSDAY(12-6-2025)
* ran pytest on amilib
* ran pytest on pygetpapers
* got an overview about anna's RAG model
* should start working with that model on my chapter
## WEDNESDAY (11-6-2025)
* created the graphviz for chapter 4
* uploaded code on github  [GitHub: graphviz](https://github.com/semanticClimate/internship_sC/tree/Haarthi/graphviz)
## TUESDAY(10-6-2025)
* Attended the reasearch AI summit
* Gone through the colab notebooks
## MONDAY(9-6-2025)
* gathered the table of contents for IPCC AR6 WG2 Chapter4
* Attended the Research AI Summit 
## FRIDAY(6-6-2025)
*  looked into the README file of pygetpapers
*  ran some commands to get the overview of the pygetpapers
## THURSDAY(5-6-2025)
* explored about pygetpapers, datatables
* understood how to use the graphviz tool by going through the **Tutorial to learn graphviz tool**
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


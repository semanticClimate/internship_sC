## FRIDAY(4-7-2025)
* Tried running the Streamlit from the `sarth` branch of the `llmrag` repository.
* Applied the `WG2 Chapter 4` and attempted to load the chapter into the application.
* The chapter took approximately `1 hour` to load completely.
* Asked the chatbot multiple questions, but it did not return relevant answers, discussed about the problem in the meeting.
* Shared these observations in the Discussions of the llmrag repository.- [Github:discussions](https://github.com/semanticClimate/llmrag/discussions/12#discussion-8529753)
* Updated the spreadsheet with chapter chunking and progress details
## THURSDAY (3-7-2025)
* pulled the latest llmrag and ran pytest
* posted the output on llmrag discussion-[Github:discussions](https://github.com/semanticClimate/llmrag/discussions/10#discussion-8524698)
* have gone through sarth branch of llmrag and tested it to make sure that streamlit(drop down to select the chapter and WG) is working on my machine
* should go through the md in the llmrag repository 
## WEDNESDAY(2-7-2025)
* discussed about the problem in the meeting
* going through the instructions given by the cursor
* remove the cloned files and cloned again
* solved the errors and all tests ran successfully( ran pytest on llmrag)
```sh
(venv) (base) C:\Users\Dell\llmrag>pip install -e .
Obtaining file:///C:/Users/Dell/llmrag
  Installing build dependencies ... done
  Checking if build backend supports build_editable ... done
  Getting requirements to build editable ... done
  Preparing editable metadata (pyproject.toml) ... done
Building wheels for collected packages: llmrag
  Building editable for llmrag (pyproject.toml) ... done
  Created wheel for llmrag: filename=llmrag-0.1.1-0.editable-py3-none-any.whl size=13657 sha256=124657e39924f2382e41ece7d8ffcc3019ea533cd7f706466d40f8ddf3be1a18
  Stored in directory: C:\Users\Dell\AppData\Local\Temp\pip-ephem-wheel-cache-f1lyod4s\wheels\75\f6\40\893f94ea7ab9cfc4e2345322d1a63d92410ddc37716cd7d98c
Successfully built llmrag
Installing collected packages: llmrag
Successfully installed llmrag-0.1.1

[notice] A new release of pip is available: 24.2 -> 25.1.1
[notice] To update, run: python.exe -m pip install --upgrade pip

(venv) (base) C:\Users\Dell\llmrag>pytest
...............................                                                                                                                      [100%]
31 passed in 147.20s (0:02:27)
```
## TUESDAY(1-7-2025)
* tried to resolve the error obtaining due to the command `pip install -e .`
* couldn't actually solve it, took help of chatgpt and tried the suggested commands but didn't workout
* the following are the commands i tried
```sh
#  Upgrade build tools
pip install --upgrade pip setuptools wheel
#  Try editable install again
pip install -e .
# Run in verbose mode to see where it's freezing:
pip install -e . -v
``` 
## MONDAY(30-6-2025)
* made some changes in the markdown about the general instructions
* have to look into the llmrag and should resolve the errors
## FRIDAY(27-6-2025)
* added the general instructions in the readme created
* it included - how to use the colab, how to upload file and copy the path, how to setup venv, how to install semantic tools, about the basic errors
* tried to resolve llmrag error
## THURSDAY(26-6-2025)
* Assigned a task to create a md of the general instructions needed for the participants in FSCI
* started to gather the topics that need to be included in the md
* created a readmefile as `FSCI_Instructions.md`
## WEDNESDAY(25-6-2025)
* gone through the meeting recording of tuesday's second session
* tested the latest version of llmrag
* tried to resolve some errors
*  reported the issues on llmrag discussions
## TUESDAY(24-6-2025)
* gone through the meeting recordings as i couldn't be able to attend the meeting on monday to keep updated
* gone through readme file and ran the llmrag test and ran it successfully
* updated the report on llmrag discussions and on slack
* added my details in the spreadsheets(included my chapters, report of llmrag test)
* tested the llmrag working on my chapter wg2 chapter 4
* posted the results in the llmrag discussions
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


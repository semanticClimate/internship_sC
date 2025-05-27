### MONDAY(19-05-2025)
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
### TUESDAY(20-05-2025)
Worked on extracting the keywords in the IPCC WG2 AR6 Chapter 4-water.But the output obtained  mainly contains names of countries and people, not the important terms from the chapter. I’m trying to improve this using model-based methods, but it’s taking a lot of time to load and process.I have uploaded the folder with all this data in this repository named*IPCC_Keyword_Project*.
### WEDNESDAY(21-05-2025)
tried to fix the problem, used [GitHub: semanticClimate keyword extraction](https://github.com/petermr/semanticClimate/blob/main/keyword_extraction/code_v2/keyword_extraction_v2_test.py)
but got the output as empty file. I replaced the model in this to another but it has its own drawbacks
### THURSDAY(22-05-2025)
explored various models that might help in extracting the keywords (kryBERT, YAKE),tried using them
### FRIDAY(23-05-2025)
used YAKE and got some of the keywords, attached the code and wordlist obtained *Keyword_Extractor*. But those are also not the main keywords that are needed.
### MONDAY(26-05-2025)
Successfully extracted the keywords from the IPCC WG2 AR6 Chapter 4-water. checked if there are any  irrelevant and simple words,started to work on the dictionary.
### TUESDAY(27-05-2025)
Documented the process for extracting the keywords.[GitHub: semanticClimate process for extracting keywords](https://github.com/semanticClimate/internship_sC/blob/Haarthi/Keyword_Extraction_Process.md)
Here is the Wordlist that I got
[GitHub: semanticClimate IPCC WG2 CHAPTER4 WORDLIST](https://github.com/semanticClimate/internship_sC/blob/Haarthi/Keyword_Extraction/keyphrases.csv)
and while creating the dictionary I got an issue in amilib that the code is not extracting information from Wikipedia when we are using the google colab 

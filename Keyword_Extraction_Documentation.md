## Getting started with keyword extraction
* Install the python version 3.12 from https://www.python.org/downloads/
* Create a virtual environment in your terminal or command prompt and activate it
* -Use the code py -3.12 -m venv aminew to create virtual env. Replace aminew with your name of the environment. python==3.12 has been added to this venv
* -aminew\Scripts\activate
* Install the latest version of txt2phrases from PyPI (pip install txt2phrases (Copy the complete command along with version number to install the latest version you can find it by going to this link https://pypi.org/project/txt2phrases/ and then click on  release history  and then when you click on it you will get the most latest version from there just copy the command and run it  (starts installing))
* For extracting the keywords you need a html version of your chapter which is present in the github link : https://github.com/semanticClimate/ipcc/tree/main/cleaned_content you need to download the html_with_ids.html file for your chapter
* To convert your html file to text file Use the command-   html2txt -i your (input folder path) -o (output folder path)
* To extract keyphrases run the command : extract_keywords -i your (input folder path) -o (output folder path)
* You may come across an import error for Pytorch if it is not avaliable in your environment. Run the command- pip install torch to install the missing library
* Once, keywords are extracted it will be saved as a .csv file , remove the duplicates and the noise keywords from the file and select the list of keywords you want to create an encyclopedia for and save the list of keywords in a .txt file.
## CREATING AN ENCYCLOPEDIA OF THE EXTRATCED KEYWORDS
* Install latest version amilib from PyPI to create the dictionary from extracted keywords (similar to installation of txt2phrases)
* Once, installed run the command amilib --help to check for successful installation. If not installed successfully you will get an error such as ModuleNotFoundError: No module named 'sklearn'
* For this error run the command pip install scikit-learn and then again run the amilib --help to check for successful installation , if installed successfully no error will be seen and information regarding amilib will be visible on screen.
* After successfully installing amilib run the command amilib DICT --words your_wordlist_path.txt  --description wikipedia --dict output_dict_path.html --figures --operation create In this command you need to give the file name of your keyphrases in place of your_wordlist_path.txt (eg: keyphrases.txt)




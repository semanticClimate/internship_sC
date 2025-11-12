## Getting started with keyword extraction
* create and activate a virtual enviroment
* Install the python version 3.12 from https://www.python.org/downloads/
* Install the latest version of txt2phrases from PyPI 
* To convert your html file to text file Use this command-   html2txt -i your (input folder path) -o (output folder path)
* To extract keyphrases run the command : extract_keywords -i your (input folder path) -o (output folder path)
* You may come across an import error for Pytorch if it is not avaliable in your environment such as 
* ImportError:AutoModelForTokenClassification requires the PyTorch library but it was not found in your environment. Check out the instructions on the installation page: https://pytorch.org/get-started/locally/ and follow the ones that match your environment.Please note that you may need to restart your runtime after installation.
* Then run the command- pip install torch to nstall the missing library
* Once, keywords are extracted it will be saved as a .csv file , remove the duplicates from the files and the easy keywords and save the list of keywords in a .txt file.
* Install latest version amilib from PyPI to create the dictionary from extracted keywords
* once, installed run the command amilib --help to check for successful installation. If not installed successfully you will get a error such as ModuleNotFoundError: No module named 'sklearn'
* For this error run the command pip install scikit-learn and then again run the amilib --help to check for successful installation , if installed successfully no error will be seen and information regarding amilib will be visible on screen.
* After successfully installing amilib run the command amilib DICT --words your_wordlist_path.txt  --description wikipedia --dict output_dict_path.html --figures --operation create In this command you need to give the file name of your keyphrases in place of your_wordlist_path.txt (eg: keyphrases.txt)

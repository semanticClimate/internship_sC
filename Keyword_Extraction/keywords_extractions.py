import nltk
from nltk.tokenize import word_tokenize
import re
import os

# Define the directory where NLTK data was downloaded
nltk_data_dir = '/usr/local/nltk_data'

# Construct the path to the English stopwords file
stopwords_file_path = os.path.join(nltk_data_dir, 'corpora', 'stopwords', 'english')

# Read the stopwords directly from the file
try:
    with open(stopwords_file_path, 'r') as f:
        english_stopwords = set(f.read().splitlines())
except FileNotFoundError:
    print(f"Error: Stopwords file not found at {stopwords_file_path}")
    english_stopwords = set() # Set to empty set if file not found


def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    tokens = word_tokenize(text)
    words = [word for word in tokens if word.isalpha()]
    filtered_words = [word for word in words if word not in english_stopwords]
    return filtered_words

cleaned_words = clean_text(pdf_text)
import nltk
import os

# Define a directory for NLTK data
nltk_data_dir = '/usr/local/nltk_data'

# Remove the existing NLTK data directory if it exists
!rm -rf {nltk_data_dir}

# Create the directory if it doesn't exist
os.makedirs(nltk_data_dir, exist_ok=True)

# Add the directory to NLTK's data path
nltk.data.path.append(nltk_data_dir)

# Download the necessary NLTK data to the specified directory
nltk.download('punkt', download_dir=nltk_data_dir)
nltk.download('stopwords', download_dir=nltk_data_dir)

from keybert import KeyBERT

kw_model = KeyBERT()
keywords = kw_model.extract_keywords(cleaned_text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=200)

print("\nTop 200 Keywords/Phrases:\n")
for kw, score in keywords:
    print(kw)

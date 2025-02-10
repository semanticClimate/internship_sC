import pdfplumber
import re
from collections import Counter
import os

# Import the setup file (Make sure download_nltk.py is in the same folder)
import download_nltk

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
    return text

def preprocess_text(text):
    """Cleans and tokenizes text."""
    text = text.lower()
    words = re.findall(r"\b[a-z]{3,}\b", text)  # Extract words with at least 3 letters
    words = [word for word in words if word not in download_nltk.STOPWORDS]  # Use stopwords from nltk_setup
    return words

def create_wordlist(pdf_path, min_frequency=2, max_frequency=10, max_words = 100, save_to_file=True):
    """Creates a wordlist of words that are not too common but still relevant."""
    text = extract_text_from_pdf(pdf_path)
    words = preprocess_text(text)
    word_counts = Counter(words)

    # Keep words that appear at least `min_frequency` times but not more than `max_frequency`
    filtered_words = [word for word, count in word_counts.items() if min_frequency <= count <= max_frequency]

    new_wordlist = filtered_words[:max_words]

    if save_to_file:
        # Get the directory where `wordlist.py` is located
        folder_path = os.path.dirname(os.path.abspath(__file__))  # No extra "wordlist" folder

        # Define the output file path
        file_path = os.path.join(folder_path, "wordlist.txt")

        # Save words to the text file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(new_wordlist))

        print(f" Wordlist saved to {file_path}")

    return new_wordlist  # Returns a list of words


# Example usage
pdf_path = "IPCC_AR6_WGII_CCP7 (1).pdf"
wordlist = create_wordlist(pdf_path)
print("\n".join(wordlist))

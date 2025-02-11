import os
import pdfplumber
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import yake
import pytesseract

# Download required NLTK data
import setup_nltk


def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF using pdfplumber, falls back to OCR if needed."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
            else:
                # Fallback to OCR if no text is found
                img = page.to_image()
                text += pytesseract.image_to_string(img) + " "

    if not text.strip():
        print("[ERROR] No text extracted. Your PDF might be image-based.")

    return text.strip()


def preprocess_text(text):
    """Tokenizes text and removes stopwords, numbers, and punctuation."""
    words = word_tokenize(text.lower())
    words = [word for word in words if word.isalnum()]  # Remove punctuation
    words = [word for word in words if not word.isnumeric()]  # Remove numbers
    words = [word for word in words if word not in setup_nltk.STOPWORDS]

    cleaned_text = " ".join(words)

    if not cleaned_text.strip():
        print("[ERROR] Text was removed during preprocessing.")

    return cleaned_text


def extract_keywords(text, num_words, phrase_length):
    """Extracts keywords using YAKE! with adjustable phrase length."""
    kw_extractor = yake.KeywordExtractor(lan="en", n=phrase_length, top=max(num_words, 10))
    keywords = kw_extractor.extract_keywords(text)

    return [word for word, score in keywords]  # Extract only words


def save_word_list(word_list):
    """Saves the extracted word list to a text file inside the wordlist folder."""
    folder_path = os.path.dirname(os.path.abspath(__file__))  # No extra "wordlist" folder

    # Define the output file path
    file_path = os.path.join(folder_path, "wordlist.txt")

    # Save words to the text file
    with open(file_path, "w", encoding="utf-8") as file:
        for word in word_list:
            file.write(word + "\n")

    print(f"\n Wordlist saved to {file_path}")


def create_word_list(pdf_path, num_words, phrase_length=1):
    """
    Generates a meaningful word list from a PDF file and saves it to a specified text file.

    Parameters:
        pdf_path (str): Path to the PDF file.
        num_words (int): Number of words/phrases to extract.
        phrase_length (int): Number of words per phrase (1 = single words, 2 = bi-grams, etc.)
    """
    text = extract_text_from_pdf(pdf_path)
    print("\nExtracted Text Preview:\n", text[:500])  # Debugging: Print first 500 chars

    cleaned_text = preprocess_text(text)
    print("\nCleaned Text Preview:\n", cleaned_text[:500])  # Debugging: Print first 500 chars

    word_list = extract_keywords(cleaned_text, num_words, phrase_length)

    if not word_list:
        print("[ERROR] No keywords extracted. Try increasing `num_words`.")
    else:
        save_word_list(word_list)

    return word_list


# Example Usage
pdf_file = r"IPCC_AR6_WGII_CCP7 (1).pdf"
num_words = 200  # Number of words/phrases to extract
phrase_length = 1  # Adjust phrase length: 1 (single words), 2 (bi-grams), 3 (tri-grams), etc.


word_list = create_word_list(pdf_file, num_words, phrase_length)

print("\nHighly Relevant Words Based on PDF Content:")
print(word_list)
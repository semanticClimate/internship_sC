from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import yake
import os

# Ensure necessary downloads
nltk.download('stopwords')
nltk.download('punkt')

def extract_text_from_html(html_path):
    with open(html_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    for script in soup(["script", "style"]):
        script.extract()

    return soup.get_text(separator=' ')

def preprocess_text(text):
    words = word_tokenize(text.lower())
    words = [word for word in words if word.isalnum()]
    words = [word for word in words if not word.isnumeric()]
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word not in stop_words]
    return " ".join(words)

def clean_phrase(phrase):
    """Remove repeating words in a phrase like 'figure figure'."""
    words = phrase.lower().split()
    seen = set()
    cleaned = []
    for word in words:
        if word not in seen:
            cleaned.append(word)
            seen.add(word)
    return " ".join(cleaned)

def is_valid_phrase(phrase, stop_words, min_len=3):
    words = phrase.lower().split()
    if len(words) < 2: return False
    if all(word in stop_words for word in words): return False
    if len(phrase) < min_len: return False
    return True

def extract_keywords(text, num_words, phrase_length):
    extractor = yake.KeywordExtractor(
        lan="en", n=phrase_length, top=num_words*2, dedupLim=0.9
    )
    raw_keywords = extractor.extract_keywords(text)
    
    stop_words = set(stopwords.words("english"))
    cleaned_keywords = []
    seen = set()
    
    for phrase, score in sorted(raw_keywords, key=lambda x: x[1]):
        cleaned = clean_phrase(phrase)
        if cleaned not in seen and is_valid_phrase(cleaned, stop_words):
            seen.add(cleaned)
            cleaned_keywords.append(cleaned)
        if len(cleaned_keywords) >= num_words:
            break

    return cleaned_keywords

def save_word_list(word_list, output_path):
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_path, "w", encoding="utf-8") as f:
        for word in word_list:
            f.write(word + "\n")
    print(f"\nWord list saved to {output_path}")

def create_word_list_from_html(html_path, num_words, phrase_length=2, output_path="wordlist.txt"):
    text = extract_text_from_html(html_path)
    print("\nExtracted Text Preview:\n", text[:500])

    cleaned_text = preprocess_text(text)
    print("\nCleaned Text Preview:\n", cleaned_text[:500])

    word_list = extract_keywords(cleaned_text, num_words, phrase_length)

    if not word_list:
        print("[ERROR] No keywords extracted.")
    else:
        save_word_list(word_list, output_path)

    return word_list

# Example usage
html_file = r"html_with_ids.html"
num_words = 100
phrase_length = 2
output_path = r"output_wordlist.txt"

keywords = create_word_list_from_html(html_file, num_words, phrase_length, output_path)
print("\nHighly Relevant Cleaned Keywords:")
print(keywords)

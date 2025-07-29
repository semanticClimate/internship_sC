from bs4 import BeautifulSoup
import re

# Load HTML file
with open("IPCC_AR6_WGI_Chapter04.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Extract and clean text
text = soup.get_text(separator=" ")
text = re.sub(r"\[\d+\]", "", text)  # remove citations
text = re.sub(r"[^\w\s\-]", " ", text)  # remove punctuation
text = text.lower()

# Exclude very common English/basic science words
stopwords = set([
    'climate', 'global', 'change', 'report', 'chapter', 'earth', 'model', 'data', 'study',
    'result', 'level', 'high', 'low', 'figure', 'table', 'time', 'value', 'based',
    'system', 'surface', 'ocean', 'years', 'effect', 'area', 'work', 'space', 'mean',
    'number', 'case', 'point', 'same', 'used', 'shown', 'shown', 'first', 'new',
    'increase', 'decrease', 'include', 'e.g.', 'etc', 'however', 'although'
])

# Step 1: Extract all words ≥ 7 letters
words = re.findall(r'\b[a-z\-]{7,}\b', text)
words = [w for w in words if w not in stopwords]

# Step 2: Remove substrings (if one word is part of another, keep longest)
unique_words = sorted(set(words), key=len, reverse=True)
filtered_words = []

for word in unique_words:
    if not any(word in longer for longer in filtered_words):
        filtered_words.append(word)

# Step 3: Save outputs
with open("WG1_CH04_cleaned_keywords.txt", "w", encoding="utf-8") as f_txt:
    for word in sorted(filtered_words):
        f_txt.write(word + "\n")

with open("WG1_CH04_cleaned_keywords.csv", "w", encoding="utf-8") as f_csv:
    f_csv.write("Word\n")
    for word in sorted(filtered_words):
        f_csv.write(f"{word}\n")

print(f"✅ Extracted {len(filtered_words)} unique scientific words.")
print("📄 Saved to:")
print(" - WG1_CH04_cleaned_keywords.txt")
print(" - WG1_CH04_cleaned_keywords.csv")

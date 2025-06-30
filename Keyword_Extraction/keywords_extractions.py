from pdfminer.high_level import extract_text

input_pdf = 'IPCC_AR6_WGI_Chapter08.pdf'
output_txt = 'converted_text.txt'

# Extract plain text from PDF
text = extract_text(input_pdf)

# Save it to a file
with open(output_txt, 'w', encoding='utf-8') as f:
    f.write(text)

print("✅ PDF converted to text")

from bs4 import BeautifulSoup
from collections import Counter
import re

# Load the extracted text (treating it like HTML to simulate soup)
with open(output_txt, 'r', encoding='utf-8') as f:
    raw_text = f.read()

# You can use soup for extra cleaning (optional)
soup = BeautifulSoup(raw_text, 'html.parser')
text = soup.get_text()

# Clean text
cleaned = re.sub(r'\W+', ' ', text.lower())
words = cleaned.split()

# Remove common stopwords
stopwords = set([
    'the', 'and', 'that', 'this', 'with', 'from', 'were', 'their', 'they', 'have', 'which',
    'such', 'also', 'into', 'been', 'these', 'those', 'not', 'more', 'most', 'for', 'are',
    'was', 'its', 'but', 'can', 'will', 'one', 'has', 'had', 'may', 'each', 'than', 'all',
    'some', 'between', 'within', 'over', 'under', 'about', 'other', 'only', 'our', 'any',
    'out', 'there', 'them', 'using', 'based', 'used', 'use', 'could', 'among', 'data', 'new'
])

keywords = [word for word in words if word not in stopwords and len(word) > 3]

# Count keyword frequency
keyword_counts = Counter(keywords)

# Show top 200
print("🔑 Top 200 Keywords:")
for word, count in keyword_counts.most_common(200):
    print(f"{word}: {count}")


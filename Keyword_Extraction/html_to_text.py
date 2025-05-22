from bs4 import BeautifulSoup

# Load HTML and extract text
with open("html_with_ids.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Extract text from HTML
text = soup.get_text()

# Save to a text file
with open("Chapter4_text.txt", "w", encoding="utf-8") as output:
    output.write(text)
from bs4 import BeautifulSoup
import re

# Load your IPCC HTML file
with open("IPCC_AR6_WGI_Chapter04.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Extract all visible text
text = soup.get_text(separator=" ")

# Optional: Clean common tags like references, figure captions
text = re.sub(r"\[\d+\]", "", text)

# Define regex patterns for key climate terms
acronym_pattern = r'\b[A-Z]{3,6}\b'  # e.g., GSAT, GMST, ENSO
ssp_pattern = r'SSP\d-\d\.\d'        # e.g., SSP1-1.9
rcp_pattern = r'RCP\d\.\d'           # e.g., RCP8.5
cmip_pattern = r'CMIP\d'             # e.g., CMIP6
word_pattern = r'\b[A-Za-z-]{4,}\b'  # Longer meaningful words

# Combine all matches
matches = re.findall(f'{acronym_pattern}|{ssp_pattern}|{rcp_pattern}|{cmip_pattern}|{word_pattern}', text)

# Optional: Add custom filters for common climate keywords
keywords = set()
for word in matches:
    if word.lower() in [
        "precipitation", "warming", "feedback", "variability", "sea", "carbon", "acidification",
        "uptake", "temperature", "monsoon", "threshold", "heatwaves", "uncertainty", "projection",
        "circulation", "radiative", "forcing", "sensitivity", "climate", "pattern", "model", "scenario",
        "probabilistic", "global", "surface", "air", "response", "extremes", "pH"
    ] or word.isupper() or "SSP" in word or "RCP" in word or "CMIP" in word:
        keywords.add(word)

# Sort and write to file
with open("climate_wordlist.txt", "w", encoding="utf-8") as f:
    for word in sorted(keywords):
        f.write(word + "\n")

print(f"Extracted {len(keywords)} keywords to climate_wordlist.txt")

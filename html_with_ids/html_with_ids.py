from bs4 import BeautifulSoup
import re

import re

def generate_id(text):
    # Match hierarchical numbers like CCP7.1.2
    match = re.search(r'\bCCP(\d+(?:\.\d+)+)\b', text, re.IGNORECASE)

    if match:
        # Extract the hierarchical number (e.g., 7.1.2)
        hierarchical_number = match.group(1)
        # Replace dots with hyphens for the ID
        return f"ccp{hierarchical_number.replace('.', '-')}"
    else:
        # Fallback: Generate a sequential number (if no hierarchical number is found)
        generate_id.counter += 1
        return f"section-{generate_id.counter}"


# Initialize a counter for fallback numbering
generate_id.counter = 0

# Load the HTML file
with open("cross_chapter7.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, "lxml")

# Find all <div> elements
divs = soup.find_all("div")

# Loop through each <div> and add an ID based on its heading
for div in divs:
    # Find the first heading (h1, h2, h3, etc.) inside the <div>
    heading = div.find(["h1", "h2", "h3", "h4", "h5", "h6"])

    if heading and heading.text.strip():  # Check if heading exists and has text
        # Generate an ID from the heading text
        div_id = generate_id(heading.text.strip())

        # Assign the ID to the <div>
        div["id"] = div_id

# Save the modified HTML to a new file
with open("html_with_ids.html", "w", encoding="utf-8") as file:
    file.write(str(soup))

print("IDs added successfully! Check output.html.")
import requests
from bs4 import BeautifulSoup
import re

def fetch_html(url):
    """
    Fetches HTML content from a given url
    """
    headers = {"User-agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: Unable to fetch page (Statust Code: {response.status_code})")
        return None
    
def clean_html(html_content):
    """
    Removes unnecessary attributes and cleans the HTML
    """    
    soup = BeautifulSoup(html_content, "html.parser")

    #Remove Gatsby-related attributes
    """
    Remove unnecessary elements and attributes from the parsed HTML
    """
    # Remove <script> and <style> tags
    for tag in soup(["script", "style"]):
        tag.decompose()

    # Remove unnecessary attributes (React attributes, inline styles, classes)
    for tag in soup.find_all(True):
        attrs_to_remove = [attr for attr in tag.attrs if re.match(r"^(data-|aria-|on)", attr)]
        for attr in attrs_to_remove:
            del tag[attr]
            if 'class' in tag.attrs:
                del tag['class']
                if 'style' in tag.attrs:
                    del tag['style']
                    if 'id' in tag.attrs and not tag['id'].startswith('item-'):
                        del tag['id']

    return str(soup)


def save_html(content, filename="ccp6_processed.html"):
    """
    Saves cleaned HTML to a file.
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)
        print(f"Processed HTML saved as {filename}")


# IPCC webpage URL (replace with the specific URL you want)
ipcc_url = "https://www.ipcc.ch/report/ar6/wg2/chapter/ccp6/"

# Fetch, clean and save HTML
html_content = fetch_html(ipcc_url)
if html_content:
    cleaned_html = clean_html(html_content)
    save_html(cleaned_html)
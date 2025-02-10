from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re


def fetch_cross_chapter(url):
    """Fetch JavaScript-rendered pages using Selenium"""
    options = Options()
    options.add_argument("--headless")  # Run in background
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    html_content = driver.page_source
    driver.quit()
    return html_content

def parse_html(html_content):
    """Parse the raw HTML content into a BeautifulSoup object."""
    return BeautifulSoup(html_content, 'lxml')

def clean_html(soup):
    """Remove unnecessary elements and attributes from the parsed HTML."""
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

    # Find the main content (adjust selector if needed)
    chapter_content = soup.find("div", {"class": "chapter-content"})  # Modify selector if needed
    return chapter_content if chapter_content else soup  # Return full soup if chapter-content is not found

def add_ids(soup):
    """Assign unique IDs to each element inside the content."""
    for idx, tag in enumerate(soup.find_all(), start=1):
        tag['id'] = f"item-{idx}"
    return soup

def save_html(soup, filename):
    """Save the cleaned and processed HTML content to a file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(soup))
    print(f"Processed HTML saved as '{filename}'.")

if __name__ == "__main__":
    url = "https://www.ipcc.ch/report/ar6/wg2/chapter/ccp7/"
    html_content = fetch_cross_chapter(url)

    if html_content:
        soup = parse_html(html_content)
        cleaned_soup = clean_html(soup)
        final_soup = add_ids(cleaned_soup)
        save_html(final_soup, "ar6_crosschapter_processed.html")

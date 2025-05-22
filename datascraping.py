import requests
from bs4 import BeautifulSoup
import os
import urllib.request

# Create a directory to save images
os.makedirs('ipcc_wg2_images', exist_ok=True)

# URL of the figures page
url = 'https://www.ipcc.ch/report/ar6/wg2/figures/summary-for-policymakers'

# Headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive'
}

# Create a session to handle cookies/redirects
session = requests.Session()
session.headers.update(headers)

# Fetch the page
try:
    response = session.get(url, timeout=10)
    response.raise_for_status()  # Check for HTTP errors
except requests.exceptions.RequestException as e:
    print(f"Error fetching page: {e}")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')

# Find all image links (PNG, JPEG, JPG)
image_links = []
for img in soup.find_all('img'):
    src = img.get('src')
    if src and (src.endswith('.png') or src.endswith('.jpg') or src.endswith('.jpeg')):
        if not src.startswith('http'):
            src = 'https://www.ipcc.ch' + src
        image_links.append(src)

# Find PDF links
pdf_links = []
for a in soup.find_all('a', href=True):
    href = a['href']
    if href.endswith('.pdf'):
        if not href.startswith('http'):
            href = 'https://www.ipcc.ch' + href
        pdf_links.append(href)

# Download images
for idx, link in enumerate(image_links):
    try:
        filename = f'ipcc_wg2_images/figure_{idx+1}.png'
        response = session.get(link, stream=True, timeout=10)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f'Downloaded: {filename}')
    except requests.exceptions.RequestException as e:
        print(f'Error downloading {link}: {e}')

# Download PDFs
for idx, link in enumerate(pdf_links):
    try:
        filename = f'ipcc_wg2_images/pdf_{idx+1}.pdf'
        response = session.get(link, stream=True, timeout=10)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f'Downloaded: {filename}')
    except requests.exceptions.RequestException as e:
        print(f'Error downloading {link}: {e}')

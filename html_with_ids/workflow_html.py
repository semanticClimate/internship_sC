import requests
from bs4 import BeautifulSoup
import re
import json


def fetch_html(url):
    """Fetches HTML content from a given URL."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: Unable to fetch page (Status Code: {response.status_code})")
        return None


def clean_html(html_content):
    """Removes unnecessary attributes and cleans the HTML."""
    soup = BeautifulSoup(html_content, "html.parser")

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

    return soup


def save_html(content, filename):
    """Saves cleaned HTML to a file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(content))
    print(f"Processed HTML saved as {filename}")


def load_deletion_commands(json_file):
    """Load the JSON file containing deletion commands."""
    with open(json_file, 'r') as f:
        return json.load(f)


def remove_empty_divs(soup):
    """Remove empty <div> elements."""
    for div in soup.find_all("div"):
        if not div.text.strip() and not div.contents:
            div.decompose()
    return soup


from bs4 import BeautifulSoup


def wrap_text_with_div(html_content, deletion_commands):
    """
    Wrap specific text in a <div> and make it the parent of the <div> below it.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    for command in deletion_commands.get("wrap_text", []):
        text_to_wrap = command.get("text")
        parent_class = command.get("parent_class")

        # Find the text to wrap
        target = soup.find(string=text_to_wrap)
        if target:
            # Create a new parent <div> with the specified class
            new_div = soup.new_tag("div", **{"class": parent_class})
            new_div.string = text_to_wrap

            # Replace the text with the new <div>
            target.replace_with(new_div)

            # Find the next <div> and make it a child of the new <div>
            next_div = new_div.find_next("div")
            if next_div:
                next_div.wrap(new_div)

    return str(soup)


def unwrap_nested_divs(soup):
    """
    Unwrap nested <div> elements and keep only <div> elements that contain text, images, or heading tags.
    Works for all elements in the HTML, including <header> and <section>.
    """
    # Find all <div> elements in the entire HTML
    divs = soup.find_all("div", recursive=True)

    # Process each <div> to keep only those with text, images, or heading tags
    for div in divs:
        # Check if the <div> contains text, images, or heading tags
        if div.text.strip() or div.find(["h1", "h2", "h3", "h4", "h5", "h6", "img"]):
            # If the <div> is valid, unwrap its parent <div> if necessary
            if div.parent and div.parent.name == "div":
                # Move the valid <div> out of its parent <div>
                div.parent.unwrap()
        else:
            # Remove the <div> if it doesn't contain text, images, or heading tags
            div.decompose()

    return soup


def resize_images(soup):
    """Add a <style> tag for resizing images inside divs."""
    style_tag = soup.new_tag('style')
    style_tag.string = """
        div img {
            width: 100%;
            height: auto;
            object-fit: contain;
        }
    """
    if soup.body:
        soup.body.insert(0, style_tag)
    else:
        body_tag = soup.new_tag('body')
        soup.html.insert(1, body_tag)
        body_tag.insert(0, style_tag)
    return soup


def strip_html(html_file, deletion_commands):
    """Strip the HTML based on deletion commands."""
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Unwrap nested <div> elements and keep only those with text, images, or heading tags
    soup = unwrap_nested_divs(soup)

    for tag in deletion_commands.get("remove_tags", []):
        for element in soup.find_all(tag):
            element.decompose()

    for empty_tag_info in deletion_commands.get("remove_empty_tags", []):
        for element in soup.find_all(empty_tag_info.get("tag")):
            if not element.text.strip() and not element.contents:
                element.decompose()

    for tag in deletion_commands.get("remove_wrappers", []):
        for element in soup.find_all(tag):
            if len(element.parent.contents) > 1:
                element.unwrap()

    soup = resize_images(soup)
    soup = remove_empty_divs(soup)

    for div in soup.find_all("div"):
        div['style'] = div.get('style', '') + 'border: 2px solid red; padding: 10px;'

    return soup.prettify()


def save_stripped_html(stripped_html, output_file):
    """Save the stripped HTML to a new file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(stripped_html)


def main():
    # Paths to files
    ipcc_url = "https://www.ipcc.ch/report/ar6/wg2/chapter/ccp7/"  # IPCC webpage URL
    json_file = r'C:\Users\Dell\Documents\new_work\edit_command.json'  # Path to the JSON file with deletion commands
    processed_html_file = r'C:\Users\Dell\Documents\new_work\ccp7_processed.html'  # Path to save the cleaned HTML
    output_file = r'C:\Users\Dell\Documents\new_work\stripped_page.html'  # Path to save the stripped HTML

    # Step 1: Fetch and clean the HTML
    html_content = fetch_html(ipcc_url)
    if html_content:
        cleaned_html = clean_html(html_content)
        save_html(cleaned_html, processed_html_file)

    # Step 2: Load deletion commands and strip the HTML
    deletion_commands = load_deletion_commands(json_file)
    stripped_html = strip_html(processed_html_file, deletion_commands)

    # Step 3: Save the stripped HTML
    save_stripped_html(stripped_html, output_file)

    print(f"Stripped HTML saved to {output_file}")


if __name__ == "__main__":
    main()

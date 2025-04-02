import fitz  # PyMuPDF
import os

# Path to your PDF file
pdf_path = r"D:\newwww\PythonProject1\ClimateAcademy.pdf"  #Update this path if needed

# Directory to save the output text files
output_dir = r"D:\newwww\PythonProject1\individual_pages"  # Update this path if needed

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Open the PDF file
try:
    pdf_document = fitz.open(pdf_path)
except Exception as e:
    print(f"Error opening the PDF file: {e}")
    exit()

# Iterate through each page in the PDF
for page_num in range(len(pdf_document)):
    # Get the page
    page = pdf_document.load_page(page_num)

    # Extract text from the page
    page_text = page.get_text("text")

    # Define the output file name for the current page
    output_file = os.path.join(output_dir, f"page_{page_num + 1}.txt")

    # Save the extracted text into a separate .txt file
    with open(output_file, "w", encoding="utf-8") as text_file:
        text_file.write(page_text)

    print(f"Text from page {page_num + 1} saved to {output_file}")

print("All pages have been extracted successfully!")
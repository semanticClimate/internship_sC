import fitz  # Importing PyMuPDF

# Path to your PDF file (use a raw string to avoid escape sequence issues)
pdf_path = r"C:\Users\mebin\Downloads\ClimateAcademy.pdf"

output_text_file = "output.txt" # Path where you want to save the text file

# Open the PDF file
try:
    pdf_document = fitz.open(pdf_path)
except Exception as e:
    print(f"Error opening the PDF file: {e}")
    exit()

# Initialize an empty string to store all the text
text = ""

# Iterate through each page in the PDF
for page_num in range(len(pdf_document)):
    # Get the page
    page = pdf_document.load_page(page_num)

    # Extract text from the page
    page_text = page.get_text("text")

    # Append the text to the overall text string
    text += page_text

# Save the extracted text into a .txt file
with open(output_text_file, "w", encoding="utf-8") as text_file:
    text_file.write(text)

print(f"Text extracted and saved to {output_text_file}")
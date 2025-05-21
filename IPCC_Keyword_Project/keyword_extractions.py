
import argparse
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import os

def extract_keywords(text_file, saving_path):
    # Load model and tokenizer
    model_name = "dslim/bert-base-NER"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_name)

    # Load text
    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Set up NLP pipeline
    nlp = pipeline("ner", model=model, tokenizer=tokenizer, grouped_entities=True)

    # Run NER
    ner_results = nlp(text)

    # Extract keywords (unique words/entities)
    keywords = set()
    for entity in ner_results:
        keywords.add(entity['word'])

    # Save to file
    with open(saving_path, 'w', encoding='utf-8') as out_file:
        for word in sorted(keywords):
            out_file.write(word + '\n')

    print(f"Extracted {len(keywords)} keywords to {saving_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--text_file', type=str, required=True, help="Path to the input text file")
    parser.add_argument('--saving_path', type=str, required=True, help="Path to save the extracted keywords")
    args = parser.parse_args()
    extract_keywords(args.text_file, args.saving_path)
    

import os
import re
from collections import Counter #from typing import Counter #
import pandas as pd
from tqdm import tqdm
from argparse import ArgumentParser
from transformers import (
    TokenClassificationPipeline,
    AutoModelForTokenClassification,
    AutoTokenizer,
)
from transformers.pipelines import AggregationStrategy

# -----------------------------
# Keyphrase Extraction Pipeline
# -----------------------------
class KeyphraseExtractionPipeline(TokenClassificationPipeline):
    def __init__(self, model_name, *args, **kwargs):
        super().__init__(
            model=AutoModelForTokenClassification.from_pretrained(model_name),
            tokenizer=AutoTokenizer.from_pretrained(model_name),
            *args,
            **kwargs
        )

    def postprocess(self, *args, **kwargs):
        results = super().postprocess(
            *args,
            aggregation_strategy=AggregationStrategy.SIMPLE,
            **kwargs
        )
        return [result.get("word").strip() for result in results if result.get("word")]

# -----------------------------
# Keyword Extraction Class
# -----------------------------
class KeywordExtraction:
    def __init__(self, textfile="", saving_path=""):
        self.text = []
        self.keyphrases = []

        # Validate text file
        if textfile and os.path.isfile(textfile) and textfile.endswith(".txt"):
            self.textfile = textfile
        else:
            raise ValueError('Please provide a valid text file path ending with ".txt"')

        # Validate saving path
        if os.path.isdir(saving_path):
            self.saving_path = saving_path
        else:
            raise ValueError('Please provide a valid saving path')

    # -----------------------------
    # Read and split text file
    # -----------------------------
    def read_from_text_file(self, method="sentence"):
        with open(self.textfile, encoding="utf-8") as f:
            full_text = f.read().strip()

        if method == "sentence":
            # Split into sentences using punctuation
            self.text = re.split(r'(?<=[.!?])\s+', full_text)
        elif method == "chunk":
            # Split into word chunks of 300 words each
            words = full_text.split()
            chunk_size = 300
            self.text = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
        else:
            # Treat as one long line
            self.text = [full_text]

        print(f"Total text chunks to process: {len(self.text)}")
        print(f"First chunk preview: {self.text[0][:200]}...\n")

    # -----------------------------
    # Extract Keywords in batches
    # -----------------------------
    def extract_keywords(self, batch_size=16):
        self.read_from_text_file(method="sentence")

        model_name = "ml6team/keyphrase-extraction-kbir-inspec"
        extractor = KeyphraseExtractionPipeline(model_name=model_name)

        for i in tqdm(range(0, len(self.text), batch_size), desc="Extracting keywords"):
            batch_lines = self.text[i:i + batch_size]
            batch_keyphrases_list = extractor(batch_lines)
            for keyphrases in batch_keyphrases_list:
                self.keyphrases.extend(keyphrases)

        # Count keywords
        self.keyphrase_counts = Counter(self.keyphrases)
        self.keyphrases = list(set(self.keyphrases))

        # Top 1000 keywords
        top_keywords = [kw for kw, _ in self.keyphrase_counts.most_common(1000)]

        # Save CSV safely
        os.makedirs(self.saving_path, exist_ok=True)
        output_file = os.path.join(self.saving_path, 'top_1000_keyphrases.csv')
        df = pd.DataFrame(self.keyphrase_counts.most_common(1000), columns=["keyword", "count"])
        df.to_csv(output_file, index=False)
        print(f"\nCSV saved successfully: {output_file}")

        print(f"Total unique keywords: {len(self.keyphrases)}")
        print(f"Top 10 keywords: {self.keyphrase_counts.most_common(10)}")
        return top_keywords

    # -----------------------------
    # Main function
    # -----------------------------
    def main(self):
        return self.extract_keywords()


# -----------------------------
# Command Line Interface
# -----------------------------
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-t', '--text_file', required=True, help='Path to text file (.txt)')
    parser.add_argument('-s', '--saving_path', required=True, help='Path to save CSV output')
    args = parser.parse_args()

    extractor = KeywordExtraction(textfile=args.text_file,
                                  saving_path=args.saving_path)
    extractor.main()


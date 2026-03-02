# kshn

> [!IMPORTANT]
> **Status:** This project is in active development. CLI arguments and internal logic are subject to change as the script evolves.

`kshn` is a high-performance tool designed to build structured graphs from encyclopedia-style HTML content. By leveraging a "Wikidata-First" approach, it uses existing QIDs within your HTML to pull official, high-fidelity relationships directly from Wikidata via SPARQL, bypassing the noise of traditional text-only extraction.

## Core Features

- **Automatic Extraction**: Scans HTML to find terms, IDs, and descriptions automatically.
- **Wikidata Connections**: Uses the official Wikidata database to find real-world relationships between entities.
- **Hybrid Edge Strategy**:
  - **Official**: Verified Wikidata triples.
  - **Contextual**: In-text mentions and hyperlinks.
  - **Categorical**: Wikipedia category hierarchies (e.g., *Taxon*, *Field of Study*).
- **Proximity Analysis**: Identifies paragraph-level entity co-occurrence to weight relationship strength.
- **Premium Visualization**: Generates dark-mode, interactive HTML networks using `vis-network` for immediate exploration.
- **Interoperability**: Exports to standard `GraphML` for advanced analysis in tools like Gephi or Cytoscape.

> [!CAUTION]
> **Technical Note:**
> - `kshn` uses the Wikidata SPARQL API to build relationships. The script includes built-in delays and limits to respect API best practices and avoid overwhelming their servers.
> - **Peak Hour Errors:** You may encounter "Retrying" messages or "403 Errors" during peak traffic (typically **09:00 to 17:00 UTC**). This is due to Wikidata server congestion.
> - **No QID Fallback:** If your input file does not contain Wikidata IDs, the tool will automatically build the graph based on **term co-occurrence** (entities appearing in the same paragraph).

## Installation

1. **Clone the repository**:
   ```bash
   git clone -b gulamajdhani https://github.com/semanticClimate/internship_sC.git
   cd "internship_sC/Project Knowledge Graph/script"
   ```
   *Alternatively, you can manually download `kshn.py` and `requirements.txt` from the repository.*

2. **Install dependencies**:
   Ensure you have Python 3.8+ installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface (CLI)

Run the script on an HTML file. The output will default to `<input>_KG.html`.

```bash
# Basic run (Wikidata relationships only)
python kshn.py -i input.html

# Full enrichment (Text mentions + Categories + Co-occurrence)
python kshn.py -i input.html --all

# Export for Gephi
python kshn.py -i input.html --graphml
```

### Google Colab

The easiest way to get started is using the interactive notebook:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/semanticClimate/internship_sC/blob/gulamajdhani/Project%20Knowledge%20Graph/kshn_demo.ipynb)

It provides a guided 4-step workflow to upload, process, and download your graphs without local setup.

## Requirements

- `beautifulsoup4`
- `networkx`
- `requests`
- `SPARQLWrapper`

> [!IMPORTANT]
> **Future Roadmap**
> - **Performance Optimization**: Refactoring the SPARQL batching and local graph processing for even faster execution.
> - **spaCy Integration**: Combining spaCy's Named Entity Recognition (NER) with Wikidata SPARQL to identify entities not explicitly tagged in the HTML.
> - **Offline Mode**: A version that works without an internet connection, identifying relationships based on how terms appear together in the text (e.g., in the same paragraph) or using local Wikipedia data.
> - **LLM Integration**: Utilizing Large Language Models to extract nuanced relationships and summarize complex entity clusters within the graph.

---

# Climate Academy Project Overview

This project focuses on extracting and visualizing knowledge from the **Climate Academy Student Book** by Matthew Pye. Using automated tools and custom scripts, we have transformed the text into structured data, an interactive encyclopedia, and a comprehensive knowledge graph.

## Project Workflow

### 1. Keyword Extraction
We used **`txt2phrases`** to extract relevant keywords from the Student Book. This process identifies the most significant concepts and their frequency of occurrence, providing a baseline for identifying the core themes of the book.
- **Output:** [CAbook_keywords_with_frequency.csv](https://github.com/semanticClimate/internship_sC/blob/gulamajdhani/Climate%20Academy/CAbook_keywords_with_frequency.csv)

### 2. Encyclopedia Generation
Using **`amilib`**, an interactive **Encyclopedia** was created from the extracted keywords. This process leverages **Wikipedia** and **Wikidata** to compile detailed information about each concept, providing a structured way to explore the terminology used in the Climate Academy curriculum.
- **Output:** [CAbook_encyclopedia.html](https://github.com/semanticClimate/internship_sC/blob/gulamajdhani/Climate%20Academy/CAbook_encyclopedia.html)

### 3. Knowledge Graph Construction
The final stage involved building a **Knowledge Graph** using a custom-made Python script.
- **Process:** The script extracts concepts from the HTML encyclopedia and cross-references them with **Wikidata**.
- **Result:** This process discovers real-world factual relationships between concepts, visualizing the interconnected nature of climate science, philosophy, and history as presented in the book.
- **Output:** [CAbook_KG.html](https://github.com/semanticClimate/internship_sC/blob/gulamajdhani/Climate%20Academy/CAbook_KG.html)

---


## Internship Report
## Semantic Climate Project
## Intern: Shabnam Barbhuiya
## Period: 1st Jan- 1st June
## Supervisors: Dr Gitanjali Yadav & Dr. Peter Murray-Rust
## Project: Chapter 10 � Linking Global to Regional Climate Change (WG1, IPCC AR6)

### Introduction

The Semantic Climate project is a global initiative focused on transforming climate science reports, particularly those published by the Intergovernmental Panel on Climate Change (IPCC), into semantically rich, machine-readable formats. The aim is to enhance accessibility, comprehension, and utility of these extensive scientific documents for researchers, policy-makers, educators, and the general public. Through a combination of natural language processing (NLP), machine learning, and semantic web technologies, the project empowers users to query, summarize, and explore complex climate data more intuitively.
During my internship with Semantic Climate, I worked on IPCC Working Group 1, Chapter 10, titled "Linking Global to Regional Climate Change." This chapter plays a pivotal role in connecting large-scale climatic trends with regional and localized climate phenomena, making it highly relevant to decision-makers and stakeholders across various sectors.
My main contributions included implementing keyword extraction using transformer-based models, generating a structured climate-related dictionary, and developing a pipeline capable of summarizing and answering questions from user-provided PDFs using large language models (LLMs) and retrieval-augmented generation (RAG) techniques.


## 2. Project Overview

The main document processed was Chapter 10 from the IPCC Working Group 1 report. The intern was responsible for:
* Extracting keywords using a transformer-based model.
* Building a dictionary of climate terms relevant to the chapter.
* Developing a summarization and query-answering pipeline using transformer models and Retrieval-Augmented Generation (RAG).
These tasks aimed to improve the accessibility and navigability of dense scientific literature by transforming it into structured, searchable outputs.
3. Keyword Extraction using KeyBERT
To extract representative terms from the chapter, the KeyBERT model (available via Hugging Face) was used. KeyBERT is based on transformer embeddings and identifies the most semantically similar keyphrases from the input document.
* Tool Used: KeyBERT (all-MiniLM-L6-v2)
* Input: Cleaned full text of Chapter 10
* Output: A list of 169 unique keywords, capturing the thematic essence of the chapter.


## 4. Dictionary Generation

The 169 extracted keywords were then processed using docanalysis, an open-source CLI tool designed to build domain-specific dictionaries. Each keyword was supplemented with a description or contextual definition, allowing the output to be used as a semantic reference for researchers and machines.
* Tool Used: docanalysis
* Output Format: Dictionary in HTML/JSON format

5. Summarization and Query Pipeline (LLM + RAG)
In addition to document-specific work, I developed a general-purpose NLP pipeline capable of:
* Summarizing the contents of any PDF document.
* Answering natural language questions about the uploaded content using LLMs and RAG.
Technologies Used:
* HuggingFace transformers library
* Pretrained BART model (facebook/bart-large-cnn) for summarization
* RAG architecture with FAISS indexing for document retrieval
* Optional frontend integration using Streamlit
Pipeline Workflow:
1. PDF Input: Users can upload a PDF document.
2. Text Extraction: The PDF is converted to plain text.
3. Summarization: The BART model generates a coherent, abstract-like summary.
4. Query Handling: User questions are matched to relevant document sections using FAISS.
5. Answer Generation: Retrieved context is passed to the LLM to produce accurate, grounded responses.

Example Use Case:
* User Query: "What does the chapter say about regional model limitations?"
* System Output: "The chapter highlights that regional models often face constraints due to limited observational data, boundary condition errors, and coarse resolution, necessitating the use of statistical or dynamical downscaling methods."
This pipeline demonstrates practical, scalable use of AI in digesting and interacting with complex scientific literature.

## 6. Code Repository

All of my work during the internship is stored in the Semantic Climate GitHub repository: https://github.com/semanticClimate/internship_sC/tree/shabnam

## 7. Conclusion and Future Work
This internship provided me with hands-on experience in combining machine learning with real-world scientific data to improve accessibility and usability. I successfully completed:
* Extraction of 169 climate-relevant keywords from IPCC Chapter 10
* Generation of a structured semantic dictionary
* Development of a summarization and interactive question-answering system for scientific PDFs


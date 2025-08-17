

# Semantic Climate Internship Report

**Intern:** Moobashara Jawed
**Duration:** 1st January – 1st June
**Mentors:** Dr. Gitanjali Yadav & Dr. Peter Murray-Rust

---

## Introduction

This report documents a six-month internship with the Semantic Climate Project, an open science initiative dedicated to unlocking knowledge from climate literature.

Semantic Climate focuses on making the reports of the Intergovernmental Panel on Climate Change (IPCC) more:

* Accessible
* Semantic
* Machine-readable

The project develops open-source toolkits that extract keywords, build dictionaries and generate knowledge graphs from scientific text. This enhances the ability of researchers, policymakers and the wider community to engage with climate data.

During this internship, work was carried out on:

* IPCC Working Group I, Chapter 2: The Changing State of the Climate System
* Testing and debugging Semantic Toolkit tools
* Developing a scalable Named Entity Recognition (NER) framework for entity extraction

---

## Work on IPCC Chapter 2

The primary focus was on Working Group I (WG1), Chapter 2: The Changing State of the Climate System.

### Contributions:

* Creation of a wordlist and dictionary specific to this chapter
* Use of KeyBERT for keyword extraction
* Use of amilib for dictionary generation and refinement
* Validation of extracted terms for accuracy and relevance
* Integration of validated terms into the Semantic Climate Dictionary

**Impact:**
This work supports the construction of knowledge graphs, making IPCC content more semantic, navigable, and machine-readable for downstream applications.

---

## Contributions to Semantic Toolkit

In addition to chapter-based work, contributions were made to the testing and improvement of the Semantic Toolkit, which includes:

* docanalysis – text analysis and entity extraction
* amilib – dictionary creation and entity filtering
* ptgetpapers – bulk downloading of research papers

### Role:

* Conducted alpha testing of newly developed features
* Reported and documented bugs and errors
* Suggested improvements for tool stability and usability

These contributions helped improve the functionality and reliability of the toolkit for wider community use.

---

## Development of NER Framework

A significant outcome of this internship was the design and implementation of a custom Named Entity Recognition (NER) framework for extracting structured information from scientific literature.

### Entities Extracted:

* Countries and Geolocations
* Species
* Diseases
* Genes

### Features:

* Scalability – modular design adaptable to multiple domains
* Validation mechanisms – ensuring accuracy and minimizing false positives
* Integration-ready – can support future knowledge graph construction and enrichment of scientific repositories

**Impact:**
The framework provides a foundation for building semantic connections in both climate science and biomedical research, making it broadly applicable across disciplines.

---

## Skills and Tools Gained

The internship provided hands-on experience in:

* Natural Language Processing (NLP): spaCy, SciSpacy
* Semantic Toolkits: amilib, amidictionary, docanalysis, pygetpapers
* Software Practices: debugging, validation, GitHub workflows
* Open Science: collaborative tool development and knowledge sharing
* Climate Science Understanding: semantic representation of IPCC reports

---

## Conclusion

The internship at Semantic Climate contributed to the enrichment of IPCC literature and the strengthening of the Semantic Toolkit.

### Key Outcomes:

1. Development of a dictionary for IPCC WG1 Chapter 2 using amilib
2. Testing and debugging of Semantic Toolkit components
3. Design and implementation of a scalable NER framework for entity extraction across domains

---

## Repository

All the work done during this internship can be found in the GitHub repository:
[Semantic Climate Internship Repository – Moobashara](https://github.com/semanticClimate/internship_sC/tree/moobashara)


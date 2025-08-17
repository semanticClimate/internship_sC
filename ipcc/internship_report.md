

# Semantic Climate Internship Report


**Intern:** Moobashara Jawed
**Duration:** 1st January – 1st June
**Mentors:** Dr. Gitanjali Yadav & Dr. Peter Murray-Rust

---

## Introduction

This repository documents my six-month internship with the Semantic Climate Project, an open science initiative dedicated to unlocking knowledge from climate literature.

Semantic Climate focuses on making the reports of the Intergovernmental Panel on Climate Change (IPCC) more:

* Accessible
* Semantic
* Machine-readable

The project develops open-source toolkits that extract keywords, build dictionaries and generate knowledge graphs from scientific text. This helps researchers, policymakers and the public engage more effectively with climate data.

During my internship, I worked on:

* IPCC Working Group I, Chapter 2: The Changing State of the Climate System
* Testing and debugging Semantic Toolkit tools
* Developing a scalable Named Entity Recognition (NER) framework for entity extraction

---

## Work on IPCC Chapter 2

My primary focus was Working Group I (WG1), Chapter 2: The Changing State of the Climate System.

### Contributions:

* Created a wordlist and dictionary specific to this chapter
* Used KeyBERT for keyword extraction
* Used amilib for dictionary generation and refinement
* Validated extracted terms for accuracy and relevance
* Integrated validated terms into the Semantic Climate Dictionary

Impact:
This work supports the construction of knowledge graphs, making IPCC content more semantic, navigable and machine-readable for downstream applications.

---

## Contributions to Semantic Toolkit

I also contributed to the testing and improvement of the Semantic Toolkit, which includes:

* docanalysis – text analysis and entity extraction
* amilib – dictionary creation and entity filtering
* ptgetpapers – bulk downloading of research papers

### My role:

* Conducted alpha testing of newly developed features
* Reported and documented bugs and errors
* Suggested improvements for tool stability and usability

These contributions strengthened the toolkit, ensuring reliable use by researchers and developers.

---

## Development of NER Framework

A major achievement of my internship was designing a custom Named Entity Recognition (NER) framework for extracting structured information from scientific literature.

### Entities Extracted:

* Countries and Geolocations
* Species
* Diseases
* Genes

### Features:

* Scalability – modular design for adaptation to new domains
* Validation mechanisms – ensures accuracy and minimizes false positives
* Integration-ready – can support future knowledge graph construction and enrichment of scientific repositories

Impact:
This framework provides a foundation for building semantic connections in both climate science and biomedical research, making it versatile across disciplines.

---

## Skills and Tools Gained

During the internship, I strengthened my expertise in:

* Natural Language Processing (NLP): spaCy, SciSpacy, KeyBERT
* Semantic Toolkits: amilib, amidictionary, docanalysis, ptgetpapers
* Software Practices: debugging, validation, GitHub workflows
* Open Science: contributing to collaborative tool development
* Climate Science Understanding: deepened insights into IPCC reports and semantic representation

---

## Conclusion

This internship at Semantic Climate was a highly rewarding experience where I contributed to the open science and climate informatics community.

### Key Outcomes:

1. Built a dictionary for IPCC WG1 Chapter 2 using amilib
2. Contributed to testing and debugging of Semantic Toolkit tools
3. Developed a scalable NER framework for entity extraction across domains



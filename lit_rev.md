## AI Assisted Automated Literature Review (ALR)

**Automated Literature Review (ALR)** is searching scientific literatures for any query term from the publicly available databases and extracting information from the corpus using computational tools and techniques to reduce the time and effort required for traditional manual searches. 

### Uses of Literature Review

- Project grant writing
- Provides background information for a research problem
- Clinical Decision Support
- Identifies gaps in current knowledge.
- Defining Research Questions and Objectives


### Why need ALR?

- Large no. of publications
- Time Efficiency
- covering a broader range of studies
- review stays up to date with the latest findings
- Consistency and Reproducibility
- Cost Efficiency

### semanticClimate Toolkits for ALR 

![ALR tools](https://github.com/semanticClimate/internship_sC/blob/main/img/ALR_pic1.png)


### Workflow for ALR 

![ALR workflow](https://github.com/semanticClimate/internship_sC/blob/main/img/ALR_pic2.png)

### Steps in ALR

- **Step 1:** searching the scholarly literatures on the query term or any keywords with `pygetpapers` (text and data mining)
- **Step 2:** Creating Summary Datatables for the retrieved articles using `amilib`
- **Step 3:** Summarizing the content of the research article using `summarization` tool 
- **Step 4:** Extracting useful informations like species name, location, compounds mentioned in the literature with `Named Entity Recognition (NER)` tool
- **Step 5:** Asking questions to the PDFs with `LLMRAG` tool 


### Link to the Notebooks 

- #### [Text and data mining](https://colab.research.google.com/drive/1RumRjh0EnKcLDmXhtYvxqMKi39BX_sB1?usp=sharing)
- #### [Summarization](https://colab.research.google.com/drive/1el5Zjogk7DXqqeuBzGMqFDBGTvyWg1Pm?usp=sharing)
- #### [Named Entity Recognition](https://colab.research.google.com/drive/1oPgnTC4UrBJF-8W2t508voWEsu8_z4ac?usp=sharing)
- #### [LLMRAG](https://colab.research.google.com/drive/1RteHNh-ZROSSxja7tYRaKVCwT5wWOeVP?usp=sharing)

### About `pygetpapers`

`pygetpapers` is a tool to assess the text miners. It is a python library.

It makes the request to the Open Access libraries, analyze the hit, and download the data.

#### [Read more about the usage of pygetpapers](https://github.com/petermr/pygetpapers)

![literature search with pygetpapers](https://github.com/semanticClimate/internship_sC/blob/main/img/ALR_pic3.png)



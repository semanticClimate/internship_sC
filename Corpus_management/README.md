
**WEDNESDAY (04-06-2025)**

### Objective

Test the functionality of `pygetpapers` for downloading research articles based on a specific query.

### Initial Command

```bash
python -m pygetpapers.pygetpapers --query '"wildlife" AND "biodiversity"' --pdf --limit 5 --output downloaded_file --api openalex --output Wildlife
```

### Issue Encountered

* **Error Message:**

  ```
  pygetpapers.py: error: unrecognized arguments: AND biodiversity'
  ```
* **Cause:**
  The query string was not properly escaped. The logical operator `AND` and surrounding quotes were interpreted as separate arguments instead of a single query string.

### ✅ Solution

* Correctly escape the query string to ensure it is interpreted as one argument.
* Use backslashes to escape the internal double quotes within the query.

### ✅ Corrected Command

```bash
python -m pygetpapers.pygetpapers --query "\"wildlife\" AND \"biodiversity\"" --pdf --limit 5 --output Wildlife --api openalex
```


**WEDNESDAY (16-04-2025)**

-**Current Task**: Working on resolving the error in docanalysis

-**Current State**: Docanalysis is working on local system(windows 11), but not being able to use it in colab environment

---
# Corpus Management

## Overview  
This document outlines the responsibilities and tasks for managing the corpus and ensuring structured wordlists, dictionaries, and tables of contents (TOC) for **IPCC chapters**. The corpus is maintained using **amilib**, with tasks documented on **GitHub** for accessibility and long-term reference.

---

## Responsibilities  

### 1. **Corpus Data Management**  
- Maintain a structured record of **wordlists, dictionaries, and TOC** created for IPCC chapters.  
- Ensure completeness and correctness of **processed chapters**.  
- Track which chapters have been processed and which remain pending.  

### 2. **Code Management & Maintenance**  
- Organize and document existing **amilib** and **docanalysis** code.  
- Ensure readability and maintainability of the codebase.  
- Identify and **fix bugs** in the scripts used for corpus processing.  

### 3. **Jupyter Notebook Documentation**  
- Create **examples** of corpus processing.  
- Embed these examples in Jupyter notebooks for better accessibility.  

### 4. **Command-Line Integration**  
- Integrate new features into **amilib's command-line interface**.  
- Suggest and implement feature improvements based on project requirements.  

### 5. **Team Collaboration & Presentations**  
- Present updates on corpus management and development to the **team**.  
- Actively engage in discussions related to **amilib corpus management** on GitHub.  
- Ensure that key discussions are recorded in **ami_corpus notebooks** for **permanent reference**.  

### 6. **Video Tutorials & Documentation**  
- Record **video tutorials** explaining corpus processing and feature integrations.  
- Ensure all relevant documentation is **openly available** on GitHub for long-term access.  

---


## Contribution & Future Development  

All discussions, updates, and improvements should be **documented on GitHub** to ensure transparency and long-term accessibility. Feature requests and suggestions should be submitted through **GitHub issues** to keep track of ongoing enhancements.

This document will be regularly updated to reflect any modifications or additions to the corpus management workflow.  


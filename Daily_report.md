## Date : 16/04/2025 Wednesday

## Component 
Resolving the issues with `docanalysis` in **Google colab environment**
### **current task** : Working of `docanalysis` in **Google colab** environment
### **current status** : Not able to install `docanalysis` in colab


## Date : 04/04/2025 Wednesday

- **Task**: Tested `pygetpapers` for downloading research articles using a query.
- **Initial Command**:
  ```bash
  python -m pygetpapers.pygetpapers --query '"wildlife" AND "biodiversity"' --pdf --limit 5 --output downloaded_file --api openalex --output Wildlife

- **Output** :
```bash
pygetpapers.py: error: unrecognized arguments: AND biodiversity'
```
- **Reason** : The query string was not correctly escaped, causing the logical operator AND to be interpreted as separate arguments.

- **Solution** : 
```bash
python -m pygetpapers.pygetpapers --query "\"wildlife\" AND \"biodiversity\"" --pdf --limit 5 --output Wildlife --api openalex
```

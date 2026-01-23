#  Encyclopedia Browser: Beginner's Guide


---

## Step 1: Prepare Your Environment

It is recommended to use a virtual environment to keep your project dependencies isolated and avoid conflicts.

1.  **Open your terminal** or command prompt.
2.  **Navigate to the project directory**:
    ```bash
    cd path/to/encyclopedia-browser
    ```
3.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    ```
4.  **Activate the virtual environment**:
    - **Windows**: `.venv\Scripts\activate`
    - **Linux/macOS**: `source .venv/bin/activate`


---

## Step 2: Install Dependencies

Now, install the necessary libraries and NLP data.

```bash
# Install core dependencies
pip install streamlit whoosh nltk lxml rapidfuzz

# Download necessary NLP data for searching
python -m nltk.downloader punkt stopwords

# Install the package in editable mode
pip install -e .
```

---

## Step 3: Create Your First Encyclopedia

Before you can browse, you need content! You can generate an encyclopedia HTML file from a simple list of terms.

1.  **Create a text file** (e.g., `my_terms.txt`) with one term per line:
    ```text
    Climate Change
    Global Warming
    Sustainability
    ```
2.  **Generate the encyclopedia**:
    ```bash
    python -m Examples.create_encyclopedia_from_wordlist --wordlist my_terms.txt --output my_encyclopedia.html
    ```

> [!NOTE]
> This script fetches verified content from Wikipedia for each term and bundles it into a single, portable HTML file.

---

## Step 4: Launch the Browser

Time to see it in action! Run the browser application using the following command:

```bash
python encyclopedia/browser/run_browser.py
```

> The browser should automatically open in your default web browser at `http://localhost:8501`. If it doesn't, copy and paste the URL manually.

---

## How to Use the Browser

### 1. Load Your Content
In the sidebar on the left, click **"Upload Encyclopedia HTML File"** and select the `my_encyclopedia.html` file you just created. Then click **"Load Encyclopedia"**.

### 2. Search for Terms
Type a term in the search box. You can choose different search modes:
- **Auto (Recommended)**: Smartly tries different methods to find the best match.
- **Exact**: Finds exactly what you typed.
- **Stemmed**: Handles variations (e.g., "climate" matches "climates").
- **Fuzzy**: Finds matches even if you make a typo (e.g., "climat" matches "climate").

### 3. Browse Everything
Click the **"Browse All"** tab at the top to see a paginated list of all entries in your encyclopedia.

---

## Troubleshooting

- **"ModuleNotFoundError"**: Ensure you activated your virtual environment in **Step 1** and installed everything in **Step 2**.
- **No search results**: Try using the **Fuzzy** search mode if you aren't sure of the exact spelling.
- **Browser won't open**: Check your terminal for errors. You can run the dependency check:
  ```bash
  python encyclopedia/browser/check_dependencies.py
  ```

---

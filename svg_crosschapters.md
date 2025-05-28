# 🌍 IPCC AR6 Cross-Chapter Paper Visualizer

This project visualizes the structure of the IPCC AR6 reports with a focus on Cross-Chapter Papers (CCPs). It uses Graphviz to generate an interactive SVG diagram that:

- Shows the hierarchy of IPCC reports: IPCC → Assessment Reports → Working Groups → Chapters
- Includes links to official IPCC pages
- Parses and visualizes top-level subsection anchors (e.g., CCP1.1, CCP2.3) from the provided HTML files
- Displays the official heading of each subsection as a tooltip when hovering over the corresponding node

---

## 🔧 Setup Instructions

### 1. Install Required Tools

Make sure you have Python 3 installed. Then, run:

```bash
sudo apt-get update
sudo apt-get install -y graphviz
pip install graphviz beautifulsoup4
```

---

### 2. Prepare HTML Files

Download the official HTML files for the Cross-Chapter Papers (CCP1 to CCP7) from the IPCC AR6 WGII website and place them into a folder (e.g., `./ccp_html`).

Example files:
- `Cross-Chapter Paper 1.html`
- `Cross-Chapter Paper 2.html`
- ...
- `Cross-Chapter Paper 7.html`

---

## ▶️ How to Run

1. Save the Python script as `build_ccp_graph.py`
2. Make sure the HTML files are placed inside the expected folder (e.g., `./ccp_html`)
3. Run the script using:

```bash
python build_ccp_graph.py
```

This will:

- Parse all the Cross-Chapter Paper HTMLs
- Extract the section IDs and headings
- Build and render the full IPCC structure into an SVG file

---

## 📁 Output

- A file named `ipcc_ccp_top_sections.svg` will be created in the current directory.
- Open this file in a browser to explore the graph interactively.
- Hover over a subnode like `CCP1.2` to see the official heading (e.g., “Observed Impacts”).

---

## 📌 Notes

- Only top-level sections like `CCP1.1`, `CCP1.2`, etc. are extracted — deeper levels like `CCP1.1.1` are ignored.
- The node tooltip contains only the clean heading text (e.g., “Point of Departure”), with phrases like “Expand section” removed.
- Nodes are clickable and redirect to the official section in the IPCC website.

---

## 🪪 License

MIT License  
© 2025 Your Name

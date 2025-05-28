# 🌍 IPCC AR6 Cross-Chapter Paper Visualizer

This project visualizes the structure of the IPCC AR6 reports with a focus on Cross-Chapter Papers (CCPs). It uses Graphviz to generate an interactive SVG diagram that:

- Shows the hierarchy of IPCC reports: IPCC → Assessment Reports → Working Groups → Chapters
- Includes links to official IPCC pages
- Parses and visualizes top-level subsection anchors (e.g., CCP1.1, CCP2.3) from the provided HTML files
- Displays the official heading of each subsection as a tooltip when hovering over the corresponding node

This helps researchers, students, and policy analysts quickly explore and navigate the IPCC's extensive AR6 structure — especially the otherwise hard-to-read Cross-Chapter Papers.

---

## 🔧 Setup Instructions

### 1. Install Required Tools

Make sure you have Python 3 installed. Then, run:

```bash
sudo apt-get update
sudo apt-get install -y graphviz
pip install graphviz beautifulsoup4

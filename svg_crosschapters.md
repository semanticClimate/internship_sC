# IPCC Cross-Chapter Paper (CCP) Top-Level Graph

A small Python/Graphviz pipeline that scans your local copies of the IPCC AR6 Cross-Chapter Paper HTML files, extracts each top-level section anchor (e.g. `CCP1.1`), grabs its real heading (e.g. “Point of Departure”) as a hover-tooltip, and then renders an interactive SVG showing:

- The IPCC root node  
- Assessment Reports AR1–AR6  
- Working Groups (WG1, WG2, WG3, Synthesis Report)  
- All WG1 & WG3 chapter nodes  
- WG2 chapters + a “Cross_Chapters” parent  
- Under “Cross_Chapters,” each CCP parent (CCP1…CCP7)  
- Under each CCP, every CCPx.y sub-node with its heading as the tooltip  

---

## 📁 Repository Contents


---

## ⚙️ Prerequisites

- **Python 3.7+**  
- **Graphviz** system package (for the `dot` renderer)  
- **Google Colab** (optional, for zero-install)  
- **BeautifulSoup4** and **graphviz** Python packages  
- Local copies of the AR6 CCP HTML files in your Google Drive (or local FS)

---

## 🚀 Getting Started

### Option A: Run in Google Colab

1. **Open** `ccp_graph.ipynb` in Google Colab  
2. **Mount** your Drive when prompted  
3. **Run all cells**  
4. At the bottom you’ll see the rendered SVG inline  
5. Click any node or hover over a CCPx.y to see its heading

### Option B: Run locally

1. **Clone** this repo  
   ```bash
   git clone https://github.com/your-username/ipcc-ccp-graph.git
   cd ipcc-ccp-graph
sudo apt-get install graphviz
pip install graphviz beautifulsoup4
python scripts/build_graph.py \
    --input-dir "/path/to/your/drive/MyDrive" \
    --output svg \
    --out-name ipcc_ccp_top_sections

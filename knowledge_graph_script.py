import os
import re
import subprocess
import webbrowser
import warnings
from bs4 import BeautifulSoup
import networkx as nx
from pyvis.network import Network

# ==========================
# Step 0: Auto-install basics
# ==========================
def ensure_packages(packages):
    for pkg in packages:
        try:
            __import__(pkg)
        except ImportError:
            print(f"📦 Installing {pkg} ...")
            subprocess.check_call(["pip", "install", pkg])

ensure_packages(["beautifulsoup4", "networkx", "pyvis"])

warnings.filterwarnings("ignore")

# ==========================
# Step 1: Input / Output
# ==========================
input_file = r"C:\Users\workt\Desktop\IPCC\Encyclopedia-IPCC\ipcc_encyclopedia.html"
output_file = r"C:\Users\workt\Desktop\IPCC\kgraph\knowledge_graph_ipcc.html"
graph_html = r"C:\Users\workt\Desktop\IPCC\kgraph\kgraph.html"
graphml_path = os.path.join("output", "data", "graph", "encyclopedia_kg.graphml")

os.makedirs(os.path.dirname(graphml_path), exist_ok=True)

# ==========================
# Step 2: Clean HTML
# ==========================
print("🔎 Cleaning HTML...")

with open(input_file, "r", encoding="utf-8") as f:
    html = f.read()

# Remove citation superscripts
cleaned_html = re.sub(
    r'<sup[^>]*(cite_ref|reference)[^>]*>.*?</sup>',
    '',
    html,
    flags=re.I | re.S
)

soup = BeautifulSoup(cleaned_html, "html.parser")

entries = []
seen = set()

for i, entry in enumerate(soup.find_all("div", {"role": "ami_entry"})):
    term = entry.get("term", "").strip()
    if not term:
        continue

    desc = entry.find("p", class_="wpage_first_para")
    description = desc.get_text(strip=True) if desc else ""

    img = entry.find("img")
    img_src = img["src"] if img and img.has_attr("src") else ""

    key = (description, img_src)
    if key not in seen:
        seen.add(key)
        entries.append(entry)

# Create new clean HTML wrapper
new_soup = BeautifulSoup("""
<html>
<head>
<meta charset='utf-8'>
<title>Semantic Encyclopedia</title>
</head>
<body></body>
</html>
""", "html.parser")

wrapper = new_soup.new_tag("div", role="ami_dictionary")
new_soup.body.append(wrapper)

for entry in entries:
    wrapper.append(entry)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(str(new_soup))

print(f"✅ Cleaned file saved: {output_file}")

# ==========================
# Step 3: Extract Snippets
# ==========================
def extract_snippets(html_file):
    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    snippets = {}

    for entry in soup.find_all("div", {"role": "ami_entry"}):
        term = entry.get("term", "").strip()
        if not term:
            continue

        text = entry.get_text(" ", strip=True)
        text = re.sub(r"\s+", " ", text)

        img_tag = entry.find("img")
        img_src = img_tag["src"] if img_tag and img_tag.has_attr("src") else None

        snippets[term] = {
            "text": text[:1000],
            "image": img_src
        }

    return snippets


html_snippets = extract_snippets(output_file)

# ==========================
# Step 4: Build Knowledge Graph (NO SELF LOOPS)
# ==========================
print("🧠 Building Knowledge Graph...")

with open(output_file, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

entries = soup.find_all("div", {"role": "ami_entry"})
href_pattern = re.compile(r"/wiki/([^\"#]+)")

nodes = {}

# Extract nodes
for div in entries:
    term = div.get("term", "").strip()
    if not term:
        continue

    desc_tag = div.find("p", class_="wpage_first_para")
    desc = desc_tag.get_text(" ", strip=True) if desc_tag else ""

    img_tag = div.find("img")
    img = img_tag["src"] if img_tag and img_tag.has_attr("src") else ""

    links = []
    for a in div.find_all("a", href=True):
        match = href_pattern.search(a["href"])
        if match:
            target = match.group(1).replace("_", " ").strip()
            links.append(target)

    nodes[term] = {
        "desc": desc,
        "img": img,
        "links": links
    }

G = nx.Graph()

# Add nodes
for term, data in nodes.items():
    G.add_node(term, description=data["desc"], image=data["img"])

# Fast lookup
lookup = {t.lower(): t for t in nodes.keys()}

# Add edges safely
for src, data in nodes.items():
    for tgt in data["links"]:
        tgt_clean = tgt.lower()

        if tgt_clean in lookup:
            real_target = lookup[tgt_clean]

            if src != real_target:  # Prevent self-loop
                G.add_edge(src, real_target)

# Remove accidental self-loops
G.remove_edges_from(nx.selfloop_edges(G))


print(f"🧩 Nodes: {len(G.nodes)}")
print(f"🔗 Edges: {len(G.edges)}")

# Save GraphML
nx.write_graphml(G, graphml_path)
print(f"✅ GraphML saved: {graphml_path}")

# ==========================
# Step 5: Visualization (Legend Matched)
# ==========================

net = Network(height="100vh", width="100%", bgcolor="#000000", font_color="#FFFFFF")

for node, data in G.nodes(data=True):
    degree = len(G[node])

    # ---- Legend-based Coloring ----
    if degree >= 8:
        color = "#00FF99"      # 🟢 Highly Connected Nodes
        label_type = "Highly Connected Node"

    elif degree >= 4:
        color = "#66B2FF"      # 🔵 Main Topics
        label_type = "Main Topic"

    elif degree >= 2:
        color = "#FF9933"      # 🟠 Subfields / Categories
        label_type = "Subfield / Category"

    else:
        color = "#FF5555"      # 🔴 Related Concept
        label_type = "Related Concept"

    tooltip_text = html_snippets.get(node, {}).get("text", "")

    net.add_node(
        node,
        title=f"<b>{node}</b><br><i>{label_type}</i><br><br>{tooltip_text}",
        color=color,
        size=12 + degree * 2
    )

# Add edges
for src, tgt in G.edges():
    net.add_edge(src, tgt, color="rgba(0,255,255,0.85)", width=1.6)

net.write_html(graph_html)

print(f":earth_africa: Graph visualization saved: {graph_html}")

webbrowser.open(f"file://{os.path.abspath(graph_html)}")
import pandas as pd
import networkx as nx
from pyvis.network import Network
import webbrowser
import re

# ======================
# TEXT CLEAN
# ======================
def clean_text(x):
    if isinstance(x, str):
        x = x.strip().lower()
        x = re.sub(r'^key[\s_\-:]*', '', x)
        x = re.sub(r'^k[\s_]+', '', x)
        x = re.sub(r'^[_\-\s]+', '', x)
        x = re.sub(r'\s+', ' ', x)
    return x

# ======================
# LOAD MATRIX
# ======================
df = pd.read_csv("matrix.csv", encoding="cp1252")
df.fillna(0, inplace=True)

df.columns = df.columns.str.replace('\ufeff','')
df.columns = df.columns.str.strip().str.lower()

keyword_col = "keyword"
total_col = "total"

df[keyword_col] = df[keyword_col].apply(clean_text)
df = df.drop_duplicates(subset=keyword_col)

# ======================
# PARAMETERS
# ======================
EDGE_THRESHOLD = 15
KEYWORD_TOTAL_MIN = 10

meta_cols = [keyword_col, total_col, "n_institutions"]
institution_cols = [c for c in df.columns if c not in meta_cols]

df = df[df[total_col] >= KEYWORD_TOTAL_MIN]

# ======================
# BUILD GRAPH
# ======================
G = nx.Graph()

for _, row in df.iterrows():

    key_id = "k_" + row[keyword_col]
    key_label = clean_text(row[keyword_col])
    key_size = row[total_col]

    edge_count = 0

    for inst in institution_cols:
        val = row[inst]

        if val >= EDGE_THRESHOLD:
            edge_count += 1

            inst_id = "i_" + inst
            inst_label = clean_text(inst)

            G.add_node(inst_id, label=inst_label, kind="institution")
            G.add_node(key_id, label=key_label, kind="keyword", size_metric=key_size)

            G.add_edge(inst_id, key_id, weight=val)

    if edge_count == 0 and G.has_node(key_id):
        G.remove_node(key_id)

# ======================
# INSTITUTION SIZE
# ======================
inst_strength = {}

for u, v, d in G.edges(data=True):
    if u.startswith("i_"):
        inst_strength[u] = inst_strength.get(u, 0) + d["weight"]

for n in G.nodes():
    if n.startswith("i_"):
        G.nodes[n]["size_metric"] = inst_strength.get(n, 10)

# ======================
# VISUALIZE
# ======================
net = Network(height="860px", width="100%", bgcolor="white")
net.force_atlas_2based()

for n, d in G.nodes(data=True):

    label = clean_text(d["label"])

    # ⭐ make institution uppercase
    if d["kind"] == "institution":
        label = label.upper()

    size_val = d.get("size_metric", 30)

    if d["kind"] == "keyword":
        color = "#d97706"
        size = 10 + size_val * 0.05

        title = f"Keyword: {label} | Frequency: {int(size_val)}"
        link = f"https://en.wikipedia.org/wiki/{label.replace(' ','_')}"
        font = {"size": 17, "face": "Verdana", "bold": True}

    else:
        color = "#1e40af"
        size = 22 + size_val * 0.02

        title = f"Institution: {label}"
        link = f"https://www.google.com/search?q={label}"
        font = {"size": 18, "face": "Arial", "bold": True}

    net.add_node(
        n,
        label=label,
        size=size,
        color=color,
        title=title,
        font=font,
        onclick=f"window.open('{link}')"
    )

for u, v, d in G.edges(data=True):
    net.add_edge(
        u, v,
        width=max(1, d["weight"]/25),
        color="rgba(90,90,90,0.6)"
    )

# ======================
# HEADER
# ======================
header = """
<div style="position:fixed;left:20px;top:15px;
font-family:Arial;z-index:9999;">

<div style="font-size:22px;font-weight:bold;margin-bottom:4px;">
Knowledge Graph: Institutions × Research Keywords
</div>

<div style="font-size:14px;line-height:1.6;color:#333;">
<span style="color:#1e40af;">●</span> Blue → Institutions &nbsp;&nbsp;
<span style="color:#d97706;">●</span> Orange → Keywords &nbsp;&nbsp;
Lines → Institution researches keyword &nbsp;&nbsp;
Thicker line → Stronger association
</div>

</div>
"""

# ======================
# SAVE + INJECT HEADER
# ======================
net.write_html("knowledge_graph.html")

with open("knowledge_graph.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace("<body>", "<body>" + header)

with open("knowledge_graph.html", "w", encoding="utf-8") as f:
    f.write(html)

webbrowser.open("knowledge_graph.html")
import graphviz #The HTML version of the IPCC reports, renders them into content trees.

# Create a directed graph in Left-to-right layout.
graph = graphviz.Digraph(format='svg', graph_attr={'rankdir': 'LR'})

# Define the list of nodes (created with dynamic node creation) with their properties.
nodes = [
    {"name": "IPCC", "shape": "oval", "style": "filled", "color": "#ADD8E6", "URL": "https://www.ipcc.ch/report"},
    *[{"name": f"AR{i}", "shape": "parallelogram", "style": "filled", "color": "#90EE90"} for i in range(1, 7)],
    *[{"name": f"Wg{i}", "shape": "diamond", "style": "filled", "color": "#FFF4EO", "URL": f"https://www.ipcc.ch/report/ar6/wg{i}/"} for i in range(1, 4)],
    {"name": "SynR", "shape": "diamond", "style": "filled", "color": "#FFF4EO", "URL": "https://www.ipcc.ch/report/ar6/syr/"},
    *[{"name": f"Ch1_{i}", "shape": "cylinder", "style": "filled", "color": "#E6E6FA", "URL": f"https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-{i}/"} for i in range(1, 13)],
    {"name": "Atlas", "shape": "cylinder", "style": "filled", "color": "#E6E6FA", "URL": "https://www.ipcc.ch/report/ar6/wg1/chapter/atlas/"},
    {"name": "Chapters", "shape": "hexagon", "style": "filled", "color": "#AFEEEE"},
    {"name": "Cross_Chapters", "shape": "hexagon", "style": "filled", "color": "#AFEEEE"},
    *[{"name": f"Ch2_{i}", "shape": "cylinder", "style": "filled", "color": "#F5DEB3", "URL": f"https://www.ipcc.ch/report/ar6/wg2/chapter/chapter-{i}/"} for i in range(1, 19)],
    *[{"name": f"Ccp{i}", "shape": "cylinder", "style": "filled", "color": "#9FE2BF", "URL": f"https://www.ipcc.ch/report/ar6/wg2/chapter/ccp{i}/"} for i in range(1, 8)],
    *[{"name": f"Ch3_{i}", "shape": "cylinder", "style": "filled", "color": "#D8BFD8", "URL": f"https://www.ipcc.ch/report/ar6/wg3/chapter/chapter-{i}/"} for i in range(1, 18)]
]

# Add nodes to the graph
for node in nodes:
    graph.node(node["name"], shape=node["shape"], style=node.get("style", ""), color=node.get("color", ""), URL=node.get("URL", ""))

# Define relationships between nodes
edges = [
    ("IPCC", "AR1"), ("IPCC", "AR2"), ("IPCC", "AR3"), ("IPCC", "AR4"), ("IPCC", "AR5"), ("IPCC", "AR6"),
    ("AR6", "Wg1"), ("AR6", "Wg2"), ("AR6", "Wg3"), ("AR6", "SynR"),
    *[(f"Wg1", f"Ch1_{i}") for i in range(1, 13)], ("Wg1", "Atlas"),
    ("Wg2", "Chapters"), ("Wg2", "Cross_Chapters"),
    *[(f"Chapters", f"Ch2_{i}") for i in range(1, 19)],
    *[(f"Cross_Chapters", f"Ccp{i}") for i in range(1, 8)],
    *[(f"Wg3", f"Ch3_{i}") for i in range(1, 18)]
]

# Add edges to indicate relationships
for source, target in edges:
    graph.edge(source, target, style="dotted")

# Render the graph as an SVG file
graph.render('AR6_Vertical', view=True)  # This will save the file as 'AR6_Vertical.svg' and open it
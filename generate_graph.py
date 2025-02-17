import webbrowser
import os
from graphviz import Digraph


class GraphVizBuilder:
    """
    A modular class for creating and rendering Graphviz diagrams in SVG format.
    Includes default IPCC and AR6 WGII graphs but allows users to create custom graphs.
    """

    def __init__(self, name="CustomGraph", output_format="svg", rankdir="TB"):
        """
        Initializes a Graphviz Digraph object with default attributes.

        Args:
            name (str): Name of the graph.
            output_format (str): Output format of the graph (default is SVG).
            rankdir (str): Layout direction of the graph.
        """
        self.graph = Digraph(name, format=output_format)
        self.graph.attr(splines="curved")
        self.graph.attr(rankdir=rankdir)
        self.graph.attr("node", shape="ellipse", style="filled", color="lightgrey")
        self.node_levels = {}

    def add_node(self, node_id, label, url=None, color=None, parent = None):
        """
        Adds a node to the graph with dynamic sizing based on depth.

        Args:
            node_id (str): Unique identifier for the node.
            label (str): Display label for the node.
            url (str): (Optional) URL to associate with the node.
            color (str): (Optional) Background color for the node.
            parent (str): (Optional) Parent node ID to determine depth.
        """
        # Determine node level based on parent
        level = self.node_levels.get(parent, 0) + 1 if parent else 0
        self.node_levels[node_id] = level  # Store depth

        # Adjust size dynamically based on level
        base_font = 16
        base_width = 1.5
        base_height = 0.8
        scale_factor = 0.85  # Reduces size per level

        fontsize = max(8, base_font * (scale_factor ** level))  # Min font = 8
        width = max(0.5, base_width * (scale_factor ** level))  # Min width = 0.5
        height = max(0.3, base_height * (scale_factor ** level))  # Min height = 0.3

        attributes = {"URL": url, "target": "_blank"} if url else {}
        if color:
            attributes["color"] = color

        attributes["fontsize"] = str(int(fontsize))
        attributes["width"] = str(width)
        attributes["height"] = str(height)

        self.graph.node(node_id, label, **attributes)


    def add_edge(self, from_node, to_node, label=None, minlen=1, weight=2):
        """
        Adds a curved edge between two nodes.

        Args:
            from_node (str): Start node.
            to_node (str): End node.
            label (str): (Optional) Edge label.
            minlen (int): Edge length.
            weight (int): Edge weight for layout.
        """
        attributes = {"minlen": str(minlen), "weight": str(weight)}
        if label:
            self.graph.edge(from_node, to_node, label=label, **attributes)
        else:
            self.graph.edge(from_node, to_node, **attributes)



    def balance_graph(self):
        """
        Adds invisible edges to maintain balance in the graph.
        """
        # Example of adding invisible edges for alignment
        self.graph.edge("WG1", "WG3", style="invis", minlen="3")
        self.graph.edge("WG2", "WG1", style="invis", minlen="2")


    def render_graph(self, output_file, open_in_browser=False):
        """
        Renders the graph to a file in the 'output' folder and optionally opens it in a browser.

        Args:
            output_file (str): Name of the output file (without extension).
            open_in_browser (bool): Whether to open the file in the browser after rendering.
        """

        # Construct the full file path inside the 'output' folder
        output_dir = "output"
        filepath = os.path.join(output_dir, output_file)

        svg_path = self.graph.render(filepath, cleanup=True)
        print(f"Graph saved as {filepath}.svg")

        # If you want to open the SVG file in the browser
        html_path = "graph_viewer.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Graph Visualization</title>
    <style>
        body {{
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
            background-color: #f4f4f4;
        }}
        embed, iframe, object {{
            width: 100%;
            height: 100vh;
        }}
    </style>
</head>
<body>
    <embed src="{svg_path}" type="image/svg+xml" />
</body>
</html>""")

        if open_in_browser:
            webbrowser.open(html_path)
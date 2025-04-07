### Introduction to Graphviz
---

Graphviz is an open-source tool used for graph visualization. It helps create diagrams, flowcharts, network graphs, and hierarchical structures.

### What is Graphviz?
---

Graphviz is a software that converts text-based descriptions written in the DOT language into visually attractive graphs.

### How to Install Graphviz
---

1. Go to Graphviz Download Page, choose the Windows installer (.exe file).
2. Download and install the setup file.
3. Add Graphviz to the system’s environment variables.

## Basic Graphviz Example
--
Graphviz uses the DOT language to define graphs.

**Example: Simple Graph**
--
digraph G {
    A -> B;
    B -> C;
    A -> C;
}


**digraph G { ... }:** Defines a directed graph named G.

**A -> B;:** Creates a directed edge from node A to node B.

**A -> C;:** Another directed edge from A to C.

## What are Node and Edges?

**Nodes (or Vertices):** These are the points in the graph (e.g., A, B, C).

**Edges:** These are the lines/arrows connecting the nodes. In the example:


A -> B is an edge from node A to node B.

## Rendering the Graph
--
***Command to Render (Graphviz CLI):***

**dot -Tpng graph.dot -o graph**

**graph.dot:** The file with your DOT code.

**-Tpng:** Specifies the output format (PNG in this case).

**-o graph.png:** Output file name.

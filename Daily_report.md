# Daily Report

## May 9, 2025
- Understood the working of Test-Driven Development (TDD) in Python and how tests drive code implementation in modular libraries.

## May 15, 2025
- Learned the overall structure of IPCC reports and reviewed the HTML file organization in our repo.  
- Cloned and navigated the `amilib` GitHub repository to get acquainted with its codebase.

## May 16, 2025
- Explored the HTML cleaning workflow for WG2 chapters.  
- Applied initial cleanup scripts to WG2 Chapter 1, extracting headings and content nodes.  
- Defined Graphviz nodes in `AR6_graph.py` to map chapter and subsection IDs for visual hierarchy.

## May 17, 2025
- Investigated HTML scraping and cleaning utilities within `amilib`.  
- Ran parsing routines on WG2 Chapters 1 and 2, ensuring correct tag and metadata extraction.

## May 19, 2025
- Executed the full pytest suite across the `amilib` directory to verify test coverage.  
- Identified failing tests, discussed root causes in the team meeting, and outlined next steps for debugging.

## May 20, 2025
- Worked on extracting the Table of Contents (ToC) structure from IPCC WG2 Cross-Chapter Paper (CCP) webpages:  
  - Identified and retrieved all major section headings and their internal anchors.  
  - Parsed page content to capture section titles and corresponding links.  
  - Enabled programmatic navigation of specific report sections for downstream analysis.  
- Planned next steps to visualize this ToC structure as a graph of nodes and edges, illustrating flow and hierarchy.

## May 21–22, 2025
- Began learning Graphviz basics to visualize CCP ToC as a node-based graph.  
- Explored error-handling mechanisms in `amilib`, focusing on how different components report and manage parsing or graph-construction issues.  
- Built foundational understanding of visualization workflows and the library’s error-reporting structure.

## May 23, 2025
- Investigated and fixed a **UnicodeEncodeError** during text extraction in `amilib`:  
  - Error occurred when encoding special characters (e.g., “≥” \u2265) under the default `cp1252` codec.  
  - Analyzed traceback in `charmap_encode`, adjusted file I/O to use UTF-8 (with `errors='ignore'` or `'replace'`), and ensured all special characters are handled without failures.  
  - Improved robustness of text-extraction routines across IPCC report content.

## May 26, 2025
- Developed a Graphviz-based visualization component for IPCC WG2 Cross-Chapter Papers (CCPs):  
  - Automated creation of a hierarchical graph where each CCP is a parent node under a central “Cross_Chapters” node.  
  - Extracted each CCP’s ToC sections and added them as child nodes, each with distinct styling and a clickable URL to the source IPCC page.  
  - Enabled intuitive exploration of chapter layouts and rapid navigation between subsections.

## May 27–28, 2025
**Workflow for the Graphviz task:**
1. **Installed required tools**  
   - Installed Graphviz and BeautifulSoup for HTML parsing and graph generation in Colab.

2. **Mounted Google Drive**  
   - Connected Colab to Google Drive to access saved CCP HTML files.

3. **Imported libraries**  
   - Modules: `os`, `re` (filesystem), `BeautifulSoup` (HTML parsing), `graphviz` (graph construction), `IPython.display.SVG` (rendering).

4. **Located CCP HTML files**  
   - Searched Drive for filenames matching “Cross-Chapter Paper N” (N=1–7) with `.html` extension.  
   - Collected CCP numbers and paths into a list.

5. **Initialized the Graphviz graph**  
   - Created a `Digraph` object (SVG format).  
   - Set default font to Arial.

6. **Added overall IPCC structure (briefly)**  
   - Root “IPCC” node, linked to AR1–AR6.  
   - Under AR6, added WG1, WG2, WG3, and SYR.  
   - Populated WG1 and WG3 chapter nodes (cylinders) and connected them with dotted edges.

7. **Set up WG2 subcategories**  
   - Added “Chapters” and “Cross_Chapters” nodes (hexagons) under WG2.  
   - Connected WG2 Chapter nodes (Ch2_1 through Ch2_18) under “Chapters.”

8. **Defined helper functions for CCP processing**  
   - `extract_ccp_heading(tag, num)`: Finds the heading text for a CCP subsection (e.g., “CCP1.2”).  
   - `sanitize(heading, maxlen)`: Cleans whitespace, removes UI text, escapes quotes, and truncates long headings for tooltips.

9. **Processed each CCP**  
   For CCP 1–7:  
   - Created a parent node (e.g., “Ccp1”) styled as a cylinder with a URL to the online CCP page; connected it to “Cross_Chapters.”  
   - Parsed the CCP HTML via BeautifulSoup, locating all subsection tags with IDs matching `CCP{num}.\d+`.  
   - For each tag:  
     1. Extracted its anchor ID (e.g., “CCP1.2”).  
     2. Used `extract_ccp_heading` to get the readable heading (e.g., “Key Findings”).  
     3. Sanitized the heading to create a tooltip.  
     4. Created a child node labeled with the anchor (e.g., “CCP1_2”), assigned a URL that jumps to that section, and added the tooltip.  
     5. Connected each child node back to its CCP parent node with a dotted edge.

10. **Rendered and displayed the graph**  
    - Generated an SVG (`ipcc_ccp_top_sections.svg`) from the `Digraph`.  
    - Displayed the final visualization inline, showing the hierarchy:  
      ```  
      IPCC → AR1–AR6 → WG2 → Cross_Chapters → CCP1–CCP7 → CCP_Subsections  
      ```

## May 29–30, 2025
- **Path‐separator mismatches:** Tests expected POSIX‐style paths (e.g., `wg1/Chapter…with_ids.html`), but code returned Windows‐style backslashes. Normalized file paths with `os.path.normpath` to produce consistent POSIX-compatible strings.
- **UnicodeEncodeError failures:** Characters like “≥”, “−”, and “ė” failed under `cp1252`. Enforced UTF-8 (opening files with `encoding='utf-8'` and setting `errors='ignore'`/`'replace'`) so special characters no longer cause encoding errors.
- **“makespace” assertion issue:** One test returned `False` incorrectly. Adjusted parsing logic to correctly detect missing `<strong>` tags, ensuring that test now passes.
- **Graphviz import errors:** Tests referring to `graphviz.Digraph` and `graphviz.Graph` failed due to an incorrect or shadowed package. Reinstalled the official Python Graphviz bindings (`pip install python-graphviz`) and updated imports to restore expected attributes.
- **CLI argument mismatch:** The test for capturing errors expected an operation named `search`, but `argparse` only allowed other commands. Added `search` to the `choices` list for `--operation`, so `--operation search` now passes.

With those fixes—path normalization, UTF-8 enforcement, parsing adjustments, correct Graphviz installation, and updated CLI choices—all previously failing tests now pass successfully.

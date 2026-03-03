## extracting keyphrases from the climate_academy pdf

pip install txt2phrases.

**(vir) C:\Users\saksh\OneDrive\Desktop\semantic_nipgr\txt2phrases>txt2phrases auto -i C:\Users\saksh\OneDrive\Desktop\semantic_nipgr\txt2phrases\climate_academy\ -o results/**

-Standard folder detected.
-Found PDF: C:\Users\saksh\OneDrive\Desktop\semantic_nipgr\txt2phrases\climate_academy\ClimateAcademy_Book.pdf
-Found 1 PDFs.
-Converting 1 PDFs to TXT...
Converting PDFs:   0%|                                                             | 0/1 [00:00<?, ?it/s]Converting: C:\Users\saksh\OneDrive\Desktop\semantic_nipgr\txt2phrases\climate_academy\ClimateAcademy_Book.pdf
Converting PDFs: 100%|█████████████████████████████████████████████████████| 1/1 [00:18<00:00, 18.35s/it]
-Converted 1 PDFs to TXT.

-Running keyword extraction...
-Device set to use cpu
-Found 1 text files to process.

Extracting climate_academy.txt: 100%|██████████████████████████████████| 464/464 [48:01<00:00,  6.21s/it]
Saved: results\climate_academy_keywords.csv

Auto-pipeline complete!


## for creating encyclopedia of output csv file

-used the script https://github.com/semanticClimate/encyclopedia/blob/pmr202601/Examples/create_encyclopedia_from_phraselist.py
-on the terminal i gave the command-
**python Examples/create_encyclopedia_from_phraselist.py  --input c:\Users\saksh\OneDrive\Desktop\semantic_nipgr\txt2phrases\results\climate_academy_keywords.csv  --output encyclopedia.html --add-wikipedia --add-images --batch-size 10**

here i=input folder
o=output folder

## creating knowledge graph for the encyclopedia of climate academy book
-used the script https://github.com/semanticClimate/encyclopedia/blob/pmr202601/Examples/create_knowledge_graph.py
- i used the command
**python Examples/create_knowledge_graph.py  --input c:\Users\saksh\OneDrive\Desktop\semantic_nipgr\encyclopedia\encyclopedia.html  --output knowled
ge_graph.graphml  --format graphml  --include-wikipedia  --include-wikidata --verbose**

-Building knowledge graph...
  - Wikipedia links: True
  - Wikidata relationships: True
✓ Graph created: 873 nodes, 2703 edges
Exporting graph to temp\knowledge_graphs\encyclopedia\encyclopedia.graphml (graphml format)...
✓ Graph exported successfully to temp\knowledge_graphs\encyclopedia\encyclopedia.graphml
  Format: graphml
  Nodes: 873
  Edges: 2703

  Edge types:
    shared_value: 1639
    wikipedia_link: 652
    P527: 145
    P31: 142
    P279: 87
    P361: 31
    P2670: 7
- the output of this is encyclopedia.graphml







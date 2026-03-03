# Climate Academy Encyclopedia & Knowledge Graph Pipeline

## Project Overview

This project generates:

- An HTML Encyclopedia  
- A Knowledge Graph (GraphML format)  


from keywords extracted from the *Climate Academy* book.

#cloning the repository to utilize the scripts

git clone https://github.com/semanticClimate/encyclopedia.git
cd encyclopedia
git checkout pmr202601 
cd examples

#Making an encyclopedia of Climate Academy

command-
    !python Examples/create_encyclopedia_from_phraselist.py \
  --input /content/climate_academy_keywords.csv \
  --output /content/encyclopedia_ClimateAcademy.html \
  --add-wikipedia \
  --add-images \
  --batch-size 10

input- https://github.com/semanticClimate/internship_sC/blob/sakshi-gupta/climate%20academy/climate_academy_keywords.csv
output-https://github.com/semanticClimate/internship_sC/blob/taiba-shamim/Climate%20Academy/encyclopedia_ClimateAcademy.html

#Making a Knowledge Graph from Encyclopedia

script utilized-https://github.com/semanticClimate/encyclopedia/blob/pmr202601/Examples/create_knowledge_graph.py

command-
!python Examples/create_knowledge_graph.py --input /content/encyclopedia_ClimateAcademy.html --output /content/results/knowledge_graph_climateAcademy.graphml --format graphml --include-wikipedia --include-wikidata --verbose

input-https://github.com/semanticClimate/internship_sC/blob/taiba-shamim/Climate%20Academy/encyclopedia_ClimateAcademy.html
output-https://github.com/semanticClimate/internship_sC/blob/taiba-shamim/Climate%20Academy/Knowledge_graph_ClimateAcademy.graphml

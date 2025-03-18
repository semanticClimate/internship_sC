#The HTML version of the IPCC reports, renders them into content trees.
import graphviz
graph = graphviz.Digraph(format='svg')

#Creates The Parent Node IPCC
graph.node('IPCC', shape='oval', style="filled", color="#ADD8E6", URL="https://www.ipcc.ch/report")

#Creates Assessment Reports (AR 1-6) Nodes Using Dynamic Node Creation.
AR = [f'AR{i}' for i in range(1, 7)]
for node in AR:             #For iterating the properties of AR 1-6
    graph.node(node, shape='parallelogram', style="filled", color="#90EE90")
    graph.edge('IPCC', node, style="dotted")    #Connects edge IPCC to node i.e., AR [Assessment Reports]

#Creates Working Groups [Wg1, Wg2, Wg3] and Synthesis Report Node [SynR] Using Dynamic Node Creation
Wg = [f'Wg{i}' for i in range(1, 4)]
SynR = ['SynR']
for node in Wg + SynR:    #For Iterating the Properties and URL of Working Groups [Wg1-3] & Synthesis Report
    url = f"https://www.ipcc.ch/report/ar6/{node.lower()}/" if node != 'SynR' else "https://www.ipcc.ch/report/ar6/syr/"
    graph.node(node, shape='diamond', style="filled", color="#FFF4EO", URL=url)
    graph.edge('AR6', node, style="dotted")  #Connects edge AR6 to Working Groups & Synthesis Report

#Creates Chapters and Atlas for Working Group 1 [Wg1]
Wg1_Ch = [f'Ch1_{i}' for i in range(1, 13)] + ['Atlas']
for node in Wg1_Ch:     #For Iterating the Properties of Chapters [Ch1_1-Ch1_12] & Atlas of Working Group 1 [Wg1]
    chapter = node.split('_')[1].lower() if node != 'Atlas' else 'atlas'
    url = f"https://www.ipcc.ch/report/ar6/wg1/chapter/{'chapter-' if chapter != 'atlas' else ''}{chapter}/"
    graph.node(node, shape='cylinder', style="filled", color="#E6E6FA", URL=url)
    graph.edge('Wg1', node, style="dotted")  #Connects Edge Chapters and Atlas to Working Group 1 [Wg1]

#Creates Subcategory Nodes for Working Group 2 (Wg2) - Chapters and Cross_Chapters
SubcategoryWg2 = ['Chapters', 'Cross_Chapters']
for node in SubcategoryWg2:    #For Iterating the Properties of SubCategory of Working Group 2
    graph.node(node, shape='hexagon', style="filled", color="#AFEEEE")
    graph.edge('Wg2', node, style="dotted")   #Connects Edge Subcategory to Working Group 2 [Wg2]

#Creates Chapters for Working Group 2 [Wg2]
Wg2_Ch = [f'Ch2_{i}' for i in range(1, 19)]
for node in Wg2_Ch:     #For Iterating the Properties of Chapters [Ch2_1 - Ch2_18] of Working Group 2 [Wg2]
    chapter = node.split('_')[1]
    url = f"https://www.ipcc.ch/report/ar6/wg2/chapter/chapter-{chapter}/"
    graph.node(node, shape='cylinder', style="filled", color="#F5DEB3", URL=url)
    graph.edge('Chapters', node, style="dotted") #Connects Edge Chapters to Working Group 2 [Wg2]

#Creates Cross-Chapter for Working Group 2 [Wg2]
Wg2_Ccp = [f'Ccp{i}' for i in range(1, 8)]
for node in Wg2_Ccp:    #For Iterating the Properties of Cross_Chapters [ccp1 - ccp7] of Working Group 2 [Wg2]
    ccp = node.lower()
    url = f"https://www.ipcc.ch/report/ar6/wg2/chapter/{ccp}/"
    graph.node(node, shape='cylinder', style="filled", color="#9FE2BF", URL=url)
    graph.edge('Cross_Chapters', node, style="dotted")   #Connects Edge Cross_Chapters to Working Group 2 [Wg2]

#Creates Chapters for Working Group 3 [Wg3]
Wg3_Ch = [f'Ch3_{i}' for i in range(1, 18)]
for node in Wg3_Ch:     #For Iterating the Properties of Chapters [Ch3_1 - Ch3_17] of Working Group 3 [Wg2]
    chapter = node.split('_')[1]
    url = f"https://www.ipcc.ch/report/ar6/wg3/chapter/chapter-{chapter}/"
    graph.node(node, shape='cylinder', style="filled", color="#D8BFD8", URL=url)
    graph.edge('Wg3', node, style="dotted")     #Connects Edge Chapters to Working Group 3 [Wg3]

graph.render('layered_graph', view=True)  #Renders the Graph for Output
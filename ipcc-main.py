from generate_graph import GraphVizBuilder
if __name__ == "__main__":
    # Create an instance for the IPCC structure
    ipcc_graph = GraphVizBuilder("IPCC_Structure", rankdir="TB")
    # Creating Nodes
    ipcc_graph.add_node("IPCC", "IPCC", url="https://www.ipcc.ch/", color="lightyellow")
    ipcc_graph.add_node("WG1", "Working Group I", url="https://www.ipcc.ch/working-group/wg1/", parent= "IPCC")
    ipcc_graph.add_node("WG2", "Working Group II", url="https://www.ipcc.ch/working-group/wg2/", parent= "IPCC")
    ipcc_graph.add_node("WG3", "Working Group III", url="https://www.ipcc.ch/working-group/wg3/", parent= "IPCC")

    #Creating nodes for sub section of working group 1
    ipcc_graph.add_node("SPM1", "Summary for Policymakers",
                        url="https://www.ipcc.ch/report/ar6/wg1/chapter/summary-for-policymakers/", parent="WG1")
    ipcc_graph.add_node("TS1", "Technical Summary", url="https://www.ipcc.ch/report/ar6/wg1/chapter/technical-summary/",
                        parent="WG1")
    ipcc_graph.add_node("FR1", "Full Report", url="https://www.ipcc.ch/report/ar6/wg1/", parent="WG1")
    ipcc_graph.add_node("C1", "Chapters", url="https://www.ipcc.ch/report/ar6/wg1/",
                        color="lightyellow", parent="WG1")  # Set a different color
    ipcc_graph.add_node("CC1", "Cross Chapters", url="https://www.ipcc.ch/report/ar6/wg1/", color="lightgreen",
                        parent="WG1")

    # Adding edges of sub section of Working Group 2
    ipcc_graph.add_edge("WG1", "SPM1")
    ipcc_graph.add_edge("WG1", "TS1")
    ipcc_graph.add_edge("WG1", "FR1")
    ipcc_graph.add_edge("WG1", "C1")
    ipcc_graph.add_edge("WG1", "CC1")




    #Creating nodes for sub sections of Working Group 2
    ipcc_graph.add_node("SPM2", "Summary for Policymakers",
                     url="https://www.ipcc.ch/report/ar6/wg2/chapter/summary-for-policymakers/", parent= "WG2")
    ipcc_graph.add_node("TS2", "Technical Summary", url="https://www.ipcc.ch/report/ar6/wg2/chapter/technical-summary/", parent= "WG2")
    ipcc_graph.add_node("FR2", "Full Report", url="https://www.ipcc.ch/report/ar6/wg2/", parent= "WG2")
    ipcc_graph.add_node("C2", "Chapters", url="https://www.ipcc.ch/report/ar6/wg2/",
                     color="lightyellow", parent= "WG2")  # Set a different color
    ipcc_graph.add_node("CC2", "Cross Chapters", url="https://www.ipcc.ch/report/ar6/wg2/", color="lightgreen", parent= "WG2")


    # Adding edges of sub section of Working Group 2
    ipcc_graph.add_edge("WG2", "SPM2")
    ipcc_graph.add_edge("WG2", "TS2")
    ipcc_graph.add_edge("WG2", "FR2")
    ipcc_graph.add_edge("WG2", "C2")
    ipcc_graph.add_edge("WG2", "CC2")

    # Creating nodes for sub sections of Working Group 3
    ipcc_graph.add_node("SPM3", "Summary for Policymakers",
                        url="https://www.ipcc.ch/report/ar6/wg3/chapter/summary-for-policymakers/", parent="WG3")
    ipcc_graph.add_node("TS3", "Technical Summary", url="https://www.ipcc.ch/report/ar6/wg3/chapter/technical-summary/",
                        parent="WG3")
    ipcc_graph.add_node("FR3", "Full Report", url="https://www.ipcc.ch/report/ar6/wg3/", parent="WG3")
    ipcc_graph.add_node("C3", "Chapters", url="https://www.ipcc.ch/report/ar6/wg3/",
                        color="lightyellow", parent="WG3")  # Set a different color
    ipcc_graph.add_node("CC3", "Cross Chapters", url="https://www.ipcc.ch/report/ar6/wg3/", color="lightgreen",
                        parent="WG3")

    # Adding edges of sub section of Working Group 2
    ipcc_graph.add_edge("WG3", "SPM3")
    ipcc_graph.add_edge("WG3", "TS3")
    ipcc_graph.add_edge("WG3", "FR3")
    ipcc_graph.add_edge("WG3", "C3")
    ipcc_graph.add_edge("WG3", "CC3")

    # Adding edges
    ipcc_graph.add_edge("IPCC", "WG1")
    ipcc_graph.add_edge("IPCC", "WG2", minlen=2)
    ipcc_graph.add_edge("IPCC", "WG3")
    ipcc_graph.render_graph("ipcc_structure", open_in_browser=True)

    ipcc_graph.balance_graph()


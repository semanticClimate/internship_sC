from generate_graph import GraphVizBuilder
if __name__ == "__main__":

# Create an instance for the IPCC structure
    syr_graph = GraphVizBuilder("SYR_Report", rankdir="TB")
    # Creating Nodes
    syr_graph.add_node("Synthesis Report", "Synthesis Report", url="https://www.ipcc.ch/synthesis-report/", color="lightyellow")
    syr_graph.add_node("About", "About", url="https://www.ipcc.ch/synthesis-report/#synthesis-report-intro-1", parent= "Synthesis Reprt")
    syr_graph.add_node("Report", "Report", url="https://www.ipcc.ch/synthesis-report/#synthesis-report-text-1", color="lightgreen" ,parent= "Synthesis Reprt")
    syr_graph.add_node("Activities", "Activities", url="https://www.ipcc.ch/synthesis-report/#synthesis-report-text-2", parent= "Synthesis Reprt")

    #Creating nodes for sub section of Report
    syr_graph.add_node("First AR", "First Assesment Report",
                        url="https://www.ipcc.ch/report/ar1/syr/", parent="Report")
    syr_graph.add_node("Second AR", "Second Assesment Report", 
                       url="https://www.ipcc.ch/report/ar2/syr/", parent="Report")
    syr_graph.add_node("Third AR", "Third Assesment Report", 
                       url="https://www.ipcc.ch/report/ar3/syr/", parent="Report")
    syr_graph.add_node("Fourth AR", "Fourth Assesment", 
                       url="https://www.ipcc.ch/report/ar4/syr/", parent="Report")  # Set a different color
    syr_graph.add_node("Fifth AR", "Fifth Assesment Report", 
                       url="https://www.ipcc.ch/report/ar5/syr/", parent="Report")
    syr_graph.add_node("Sixth AR", "Sixth Assesment Report", 
                       url="https://www.ipcc.ch/report/ar6/syr/", parent="Report")
    syr_graph.add_node("SR", "Special Report", 
                       url="", color="lightgreen", parent="Report")

    # Adding edges of sub section of Report
    syr_graph.add_edge("Report", "First AR")
    syr_graph.add_edge("Report", "Second AR")
    syr_graph.add_edge("Report", "Third AR")
    syr_graph.add_edge("Report", "Fourth AR")
    syr_graph.add_edge("Report", "Fifth AR")
    syr_graph.add_edge("Report", "Sixth AR")
    syr_graph.add_edge("Report", "SR")



    #Creating nodes for sub sections of Special Report
    syr_graph.add_node("CCC", "Climate Change and Cities",
                       url="https://www.ipcc.ch/report/special-report-on-climate-change-and-cities/", parent= "Special Report")
    syr_graph.add_node("CCL", "Climate Change and Land", 
                       url="https://www.ipcc.ch/report/srccl/", parent= "Special Report")
    syr_graph.add_node("OC", "Ocean and Cryosphere", url="https://www.ipcc.ch/report/srocc/", parent= "Special Report")

    syr_graph.add_edge("SR", "CCC")
    syr_graph.add_edge("SR", "CCL")
    syr_graph.add_edge("SR", "OC")
    
    # Adding edges
    syr_graph.add_edge("Synthesis Report", "About")
    syr_graph.add_edge("Synthesis Report", "Report", minlen=2)
    syr_graph.add_edge("Synthesis Report", "Activities")
    syr_graph.render_graph("syr_report", open_in_browser=True)

    syr_graph.balance_graph()
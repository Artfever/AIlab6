"""Standalone version of the Streamlit GUI."""

import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

from searchAlgos import hospital_graph, locations, gbfs, a_star

st.set_page_config(page_title="Informed Search", page_icon="🤖", layout="wide")
st.title("Emergency Supply Robot")
st.write("Compare Greedy Best-First Search and A* on a weighted hospital graph.")

nodes = list(hospital_graph)
start = st.selectbox("Select Initial Node", nodes, index=nodes.index("Pharmacy"))
goal = st.selectbox("Select Goal Node", nodes, index=nodes.index("Emergency_Ward"))
algorithm = st.selectbox("Select Search Algorithm", ["GBFS", "A*"])

if st.button("Run Search", type="primary"):
    search = gbfs if algorithm == "GBFS" else a_star
    path, cost, expansion_order = search(start, goal)
    if path is None:
        st.error("No path was found between the selected nodes.")
    else:
        st.subheader("Search Result")
        st.write(f"**Algorithm:** {algorithm}")
        st.write(f"**Solution Path:** {' -> '.join(path)}")
        st.write(f"**Total Path Cost:** {cost:.2f}")
        st.write(f"**Expansion Order:** {' -> '.join(expansion_order)}")

        graph = nx.DiGraph()
        for node, neighbors in hospital_graph.items():
            graph.add_node(node)
            for neighbor, weight in neighbors.items():
                graph.add_edge(node, neighbor, weight=weight)

        path_edges = set(zip(path, path[1:]))
        edge_colors = ["crimson" if edge in path_edges else "#9aa0a6" for edge in graph.edges()]
        node_colors = [
            "#90ee90" if node == start else "#ff9999" if node == goal else
            "#ffd580" if node in path else "#add8e6" for node in graph.nodes()
        ]
        fig, ax = plt.subplots(figsize=(11, 6))
        nx.draw(graph, locations, ax=ax, with_labels=True, node_color=node_colors,
                node_size=2400, edge_color=edge_colors, arrows=True, arrowsize=20,
                font_weight="bold")
        nx.draw_networkx_edge_labels(graph, locations,
                                     edge_labels=nx.get_edge_attributes(graph, "weight"), ax=ax)
        ax.set_title(f"{algorithm} Solution Path")
        ax.axis("off")
        st.pyplot(fig)

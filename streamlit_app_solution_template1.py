import streamlit as st
import math
import heapq
import networkx as nx
import matplotlib.pyplot as plt

# Graph, Use Case: Emergency Supply Robot

locations = {
    "Pharmacy": (0, 0),
    "Main_Corridor": (2, 1),
    "Patient_Wing": (1, 4),
    "Nursing_Station": (4, 2),
    "Laboratory": (5, 5),
    "Emergency_Ward": (8, 6)
}

hospital_graph = {
    "Pharmacy": {
        "Main_Corridor": 2.2,
        "Patient_Wing": 4.1
    },

    "Main_Corridor": {
        "Nursing_Station": 2.2
    },

    "Patient_Wing": {
        "Laboratory": 5.0
    },

    "Nursing_Station": {
        "Laboratory": 3.2,
        "Emergency_Ward": 6.0
    },

    "Laboratory": {
        "Emergency_Ward": 3.2
    },

    "Emergency_Ward": {}
}
# Heuristic
def heuristic(current, goal):
    return math.dist(locations[current], locations[goal])

# Path reconstruction
def reconstruct_path(came_from, current):
    path = []
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    return path[::-1]

# GBFS


def gbfs(start, goal):
    frontier = [(heuristic(start, goal), start)]
    came_from = {start: None}
    visited = set()
    expansion_order = []
    while frontier:
        _, current = heapq.heappop(frontier)
        if current in visited:
            continue
        visited.add(current)
        expansion_order.append(current)
        if current == goal:
            path = reconstruct_path(came_from, current)
            cost = sum(hospital_graph[a][b] for a, b in zip(path, path[1:]))
            return path, cost, expansion_order
        for neighbor in hospital_graph[current]:
            if neighbor not in visited:
                came_from.setdefault(neighbor, current)
                heapq.heappush(frontier, (heuristic(neighbor, goal), neighbor))
    return None, None, expansion_order

# A*
def a_star(start, goal):
    frontier = [(heuristic(start, goal), start)]
    came_from = {start: None}
    g_cost = {start: 0}
    visited = set()
    expansion_order = []
    while frontier:
        _, current = heapq.heappop(frontier)
        if current in visited:
            continue
        visited.add(current)
        expansion_order.append(current)
        if current == goal:
            return reconstruct_path(came_from, current), g_cost[current], expansion_order
        for neighbor, weight in hospital_graph[current].items():
            new_cost = g_cost[current] + weight
            if new_cost < g_cost.get(neighbor, float("inf")):
                g_cost[neighbor] = new_cost
                came_from[neighbor] = current
                heapq.heappush(frontier, (new_cost + heuristic(neighbor, goal), neighbor))
    return None, None, expansion_order

##########################################
# Streamlit GUI Code

st.set_page_config(page_title="Informed Search", page_icon="🤖")

st.title("Emergency Supply Robot")
st.write("Compare Greedy Best-First Search and A* on the hospital graph.")

# define the nodes and their coordinates
nodes = list(hospital_graph.keys())

# create a selectbox for the user to choose the start and goal nodes
start = st.selectbox(
    "Select Initial Node",
    nodes,
    index=nodes.index("Pharmacy")
)

goal = st.selectbox(
    "Select Goal Node",
    nodes,
    index=nodes.index("Emergency_Ward")
)

algorithm = st.selectbox("Select Search Algorithm", ["GBFS", "A*"])


if st.button("Run Search"):

    if algorithm == "GBFS":

        path, cost, expansion_order = gbfs(start, goal)
    else:

        path, cost, expansion_order = a_star(start, goal)

    if path is None:

       st.error("No path was found.")

    else:
       
        # Display result
        st.subheader("Search Result")

        st.write(
            f"Algorithm: {algorithm}"
        )

        st.write(
            f"Solution Path: {' → '.join(path)}"
        )

        st.write(
            f"Total Path Cost: {cost:.2f}"
        )


        
        # Visualize NetworkX graph
        
        G = nx.DiGraph()

        for node, neighbors in hospital_graph.items():

            for neighbor, weight in neighbors.items():

               G.add_edge(node, neighbor, weight=weight)
        pos = locations

        fig, ax = plt.subplots(
            figsize=(10, 6)
        )

        # WRITE REMAINING NETWORKX VISUALIZATION CODE HERE

        solution_edges = set(zip(path, path[1:]))
        edge_colors = [
            "red" if edge in solution_edges else "gray"
            for edge in G.edges()
        ]
        nx.draw(
            G,
            pos,
            ax=ax,
            with_labels=True,
            node_color="lightblue",
            node_size=2200,
            edge_color=edge_colors,
            arrows=True
        )
        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels=nx.get_edge_attributes(G, "weight"),
            ax=ax
        )

        ax.set_title(
            f"{algorithm} Solution Path"
        )

        ax.axis("off")

        st.pyplot(fig)

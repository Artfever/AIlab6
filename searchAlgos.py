"""Search algorithms and data for the Streamlit GUI."""

import heapq
import math

locations = {
    "Pharmacy": (0, 0), "Main_Corridor": (2, 1), "Patient_Wing": (1, 4),
    "Nursing_Station": (4, 2), "Laboratory": (5, 5), "Emergency_Ward": (8, 6)
}

hospital_graph = {
    "Pharmacy": {"Main_Corridor": 2.2, "Patient_Wing": 4.1},
    "Main_Corridor": {"Nursing_Station": 2.2},
    "Patient_Wing": {"Laboratory": 5.0},
    "Nursing_Station": {"Laboratory": 3.2, "Emergency_Ward": 6.0},
    "Laboratory": {"Emergency_Ward": 3.2}, "Emergency_Ward": {}
}


def heuristic(current, goal):
    return math.dist(locations[current], locations[goal])


def _reconstruct_path(came_from, current):
    path = []
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    return path[::-1]


def _path_cost(path):
    return sum(hospital_graph[a][b] for a, b in zip(path, path[1:]))


def gbfs(start, goal):
    frontier = [(heuristic(start, goal), start)]
    came_from, visited, expansion_order = {start: None}, set(), []
    while frontier:
        _, current = heapq.heappop(frontier)
        if current in visited:
            continue
        visited.add(current)
        expansion_order.append(current)
        if current == goal:
            path = _reconstruct_path(came_from, current)
            return path, _path_cost(path), expansion_order
        for neighbor in hospital_graph[current]:
            if neighbor not in visited:
                came_from.setdefault(neighbor, current)
                heapq.heappush(frontier, (heuristic(neighbor, goal), neighbor))
    return None, None, expansion_order


def a_star(start, goal):
    frontier = [(heuristic(start, goal), 0.0, start)]
    came_from, g_cost, closed, expansion_order = {start: None}, {start: 0.0}, set(), []
    while frontier:
        _, current_g, current = heapq.heappop(frontier)
        if current in closed:
            continue
        closed.add(current)
        expansion_order.append(current)
        if current == goal:
            return _reconstruct_path(came_from, current), g_cost[current], expansion_order
        for neighbor, weight in hospital_graph[current].items():
            new_cost = current_g + weight
            if new_cost < g_cost.get(neighbor, float("inf")):
                g_cost[neighbor] = new_cost
                came_from[neighbor] = current
                heapq.heappush(frontier, (new_cost + heuristic(neighbor, goal), new_cost, neighbor))
    return None, None, expansion_order

from typing import Dict, List, Tuple, Union

from src.network import Network


Graph = Dict[str, List[Tuple[str, float, float]]]


def _network_to_graph(network: Network) -> Graph:
    """Convert Network into adjacency list required by Dijkstra."""
    graph: Graph = {stop.get_id(): [] for stop in network.get_all_stops()}
    for route in network.routes:
        start_id = route.get_start().get_id()
        end_id = route.get_end().get_id()
        graph.setdefault(start_id, []).append(
            (end_id, route.get_duration(), route.get_cost())
        )
        # Ensure end node exists even if it has no outgoing edges.
        graph.setdefault(end_id, [])
    return graph


def dijkstra(start: str, end: str, weight_type: str, graph_or_network: Union[Graph, Network]):
    """
    Find shortest path by time or cost.
    Supports both:
    - adjacency graph dict
    - Network object (used by Menu)
    """
    INF = float("inf")

    graph = _network_to_graph(graph_or_network) if isinstance(graph_or_network, Network) else graph_or_network
    if start not in graph or end not in graph:
        return [], INF

    # Default to cost when not "time", keeping old behavior compatible.
    use_time = weight_type == "time"

    dist = {node: INF for node in graph}
    prev = {node: None for node in graph}
    dist[start] = 0.0
    unvisited = set(graph.keys())

    while unvisited:
        current = min(unvisited, key=lambda node: dist[node])
        if dist[current] == INF:
            break
        unvisited.remove(current)

        for neighbor, duration, cost in graph[current]:
            if neighbor not in unvisited:
                continue
            edge_weight = duration if use_time else cost
            new_dist = dist[current] + edge_weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = current

    if dist[end] == INF:
        return [], INF

    path = []
    node = end
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()
    return [path, round(dist[end], 2)]
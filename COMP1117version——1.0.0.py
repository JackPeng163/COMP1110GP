import csv

def load_graph_from_csv(stops_file="stops.csv", routes_file="routes.csv"):

    stop_id_to_name = {}
    with open(stops_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            stop_id = row["id"].strip()
            name = row["name"].strip()
            stop_id_to_name[stop_id] = name

    graph = {}
    with open(routes_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            start_id = row["start_id"].strip()
            end_id = row["end_id"].strip()
            duration = float(row["duration"].strip())
            cost = float(row["cost"].strip())

            start = stop_id_to_name[start_id]
            end = stop_id_to_name[end_id]

            if start not in graph:
                graph[start] = []
            graph[start].append((end, duration, cost))

            if end not in graph:
                graph[end] = []
            graph[end].append((start, duration, cost))

    return graph

graph = load_graph_from_csv("stops.csv", "routes.csv")
const_infinity = 100000000000

def Dijkstra(start, end, weight):
    table = {}
    for i in graph:
        table.update({i: [const_infinity, None]})
    table[start][0] = 0
    processed = set()

    if weight in ["Cost", "cost"]:
        token = 2
    elif weight in ["Time", "time"]:
        token = 1
    else:
        print("Invalid weight")
        return

    while len(processed) < len(graph):
        next_current = None
        min_weight = const_infinity
        for node in graph:
            if node not in processed and table[node][0] < min_weight:
                min_weight = table[node][0]
                next_current = node

        if next_current is None:
            break
        current = next_current
        processed.add(current)

        for vertex in graph[current]:
            if (vertex[token] + table[current][0]) < table[vertex[0]][0]:
                table[vertex[0]][0] = vertex[token] + table[current][0]
                table[vertex[0]][1] = current

    path = []
    pointer = end
    if table[end][0] == const_infinity:
        print("No such path to the destination")
        return [], 0

    while table[pointer][1] is not None:
        path.append(pointer)
        pointer = table[pointer][1]
    path.append(pointer)
    path.reverse()

    return path, round(table[end][0], 2)

if __name__ == "__main__":
    print("=== Public Transport Route Planner ===")
    print("Available stations:", ", ".join(graph.keys()))
    print("-" * 50)

    while True:
        start = input("Enter your starting station: ").strip()
        if start in graph:
            break
        print(f"Error: Station '{start}' not found. Please enter a valid station from the list above.\n")

    while True:
        destination = input("Enter your destination station: ").strip()
        if destination in graph:
            break
        print(f"Error: Station '{destination}' not found. Please enter a valid station from the list above.\n")

    time_path, time_total = Dijkstra(start, destination, "time")
    cost_path, cost_total = Dijkstra(start, destination, "cost")

    print("\n" + "=" * 60)
    print("📊 Fastest Route (Minimum Time):")
    if time_path:
        print(f"Route: {' → '.join(time_path)}")
        print(f"Total Travel Time: {time_total} minutes")
    else:
        print("No valid route found between these stations.")

    print("\n💰 Cheapest Route (Minimum Cost):")
    if cost_path:
        print(f"Route: {' → '.join(cost_path)}")
        print(f"Total Cost: {cost_total}")
    else:
        print("No valid route found between these stations.")
    print("=" * 60)
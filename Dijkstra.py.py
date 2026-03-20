# 10 vertex：Central、Mong Kok、Causeway Bay、Quarry Bay、Tsim Sha Tsui、
# Admiralty、Wan Chai、North Point、Jordan、Yau Ma Tei
graph = {
    "Central": [("Mong Kok", 15, 9.8), ("Admiralty", 3, 2.5)],
    "Mong Kok": [("Central", 15, 9.8), ("Tsim Sha Tsui", 5, 3.0), ("Yau Ma Tei", 2, 1.8)],
    "Causeway Bay": [("Admiralty", 6, 4.0), ("Wan Chai", 3, 2.2)],
    "Quarry Bay": [("North Point", 4, 2.0), ("Wan Chai", 10, 5.0)],
    "Tsim Sha Tsui": [("Mong Kok", 5, 3.0), ("Jordan", 3, 1.5)],
    "Admiralty": [("Central", 3, 2.5), ("Causeway Bay", 6, 4.0)],
    "Wan Chai": [("Causeway Bay", 3, 2.2), ("Quarry Bay", 10, 5.0)],
    "North Point": [("Quarry Bay", 4, 2.0)],
    "Jordan": [("Tsim Sha Tsui", 3, 1.5), ("Yau Ma Tei", 4, 2.5)],
    "Yau Ma Tei": [("Mong Kok", 2, 1.8), ("Jordan", 4, 2.5)]
}

const_infinity = 100000000000

def Dijkstra(start, end, weight):
    table = {}
    for i in graph:
        table.update({i:[const_infinity, None]})
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
        
        if next_current == None:
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
    while table[pointer][1] != None:
        path.append(pointer)
        pointer = table[pointer][1]

    path.append(pointer)
    path.reverse()

    return path, round(table[end][0], 2)


print(Dijkstra("Central", "North Point", "time"))  

print(Dijkstra("Central", "North Point", "cost"))
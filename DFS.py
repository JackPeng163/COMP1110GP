graph = {
    # 中环：连接旺角（荃湾线）、金钟（港岛线）
    "Central": [("Mong Kok", 15, 9.8, "荃湾线"), ("Admiralty", 3, 2.5, "港岛线")],
    # 旺角：连接中环、尖沙咀（荃湾线）、油麻地（观塘线）
    "Mong Kok": [("Central", 15, 9.8, "荃湾线"), ("Tsim Sha Tsui", 5, 3.0, "荃湾线"), ("Yau Ma Tei", 2, 1.8, "观塘线")],
    # 铜锣湾：连接金钟（港岛线）、湾仔（港岛线）
    "Causeway Bay": [("Admiralty", 6, 4.0, "港岛线"), ("Wan Chai", 3, 2.2, "港岛线")],
    # 鲗鱼涌：连接北角（港岛线）、湾仔（港岛线）
    "Quarry Bay": [("North Point", 4, 2.0, "港岛线"), ("Wan Chai", 10, 5.0, "港岛线")],
    # 尖沙咀：连接旺角、佐敦（荃湾线）
    "Tsim Sha Tsui": [("Mong Kok", 5, 3.0, "荃湾线"), ("Jordan", 3, 1.5, "荃湾线")],
    # 金钟：连接中环、铜锣湾（港岛线）
    "Admiralty": [("Central", 3, 2.5, "港岛线"), ("Causeway Bay", 6, 4.0, "港岛线")],
    # 湾仔：连接铜锣湾、鲗鱼涌（港岛线）
    "Wan Chai": [("Causeway Bay", 3, 2.2, "港岛线"), ("Quarry Bay", 10, 5.0, "港岛线")],
    # 北角：连接鲗鱼涌（港岛线）
    "North Point": [("Quarry Bay", 4, 2.0, "港岛线")],
    # 佐敦：连接尖沙咀（荃湾线）、油麻地（观塘线）
    "Jordan": [("Tsim Sha Tsui", 3, 1.5, "荃湾线"), ("Yau Ma Tei", 4, 2.5, "观塘线")],
    # 油麻地：连接旺角、佐敦（观塘线）
    "Yau Ma Tei": [("Mong Kok", 2, 1.8, "观塘线"), ("Jordan", 4, 2.5, "观塘线")]
}

def dfs(start, end):
    visited = set()
    path = []

    def _dfs(current):

        if current == end:
            path.append(current)
            return True
        
        if current not in graph or current in visited:
            return False
        
        path.append(current)
        visited.add(current)

        for vertex in graph[current]:
            neighbor = vertex[0]
            if _dfs(neighbor):
                return True
        
        path.pop()
        visited.remove(current)
        return False
    
    _dfs(start)
    return path

p = dfs("Central", "North Point")
print(p)

import heapq

# ----------------------
# Campus Graph
# ----------------------
campus_graph = {
    "Library": {"Engineering": 2, "CS Building": 4},
    "Engineering": {"Library": 2, "Gym": 1, "Business": 5},
    "CS Building": {"Library": 4, "Gym": 3},
    "Gym": {"CS Building": 3, "Engineering": 1, "Business": 2},
    "Business": {"Engineering": 5, "Gym": 2}
}
building_names = list(campus_graph.keys())

building_names = list(campus_graph.keys())

# ----------------------
# Dijkstra's Algorithm
# ----------------------
def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0
    pq = [(0, start)]

    while pq:
        current_dist, current_node = heapq.heappop(pq)
        for neighbor, weight in graph[current_node].items():
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
    return distances, previous

def get_path(previous, end):
    path = []
    while end:
        path.append(end)
        end = previous[end]
    return path[::-1]

# ----------------------
# KMP Search Algorithm
# ----------------------
def build_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps
        
def kmp_search(text, pattern):
    lps = build_lps(pattern)
    i = j = 0
    results = []
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            results.append(i - j)
            j = lps[j - 1]
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return results

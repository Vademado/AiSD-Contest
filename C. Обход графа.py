from sys import stdin, setrecursionlimit

setrecursionlimit(10 ** 7)


class Graph:
    def __init__(self, graph_type: str):
        self.adjacency_dictionary = dict()
        self.oriented = True if graph_type == 'd' else False

    def add_edge(self, starting_vertex: str, ending_vertex: str):
        self.adjacency_dictionary.setdefault(starting_vertex, []).append(ending_vertex)
        if not self.oriented:
            self.adjacency_dictionary.setdefault(ending_vertex, []).append(starting_vertex)

    def dfs(self, starting_vertex: str, path: list, visited: set):
        path.append(starting_vertex)
        visited.add(starting_vertex)
        for v in sorted(self.adjacency_dictionary.setdefault(starting_vertex, [])):
            if v not in visited:
                self.dfs(v, path, visited)
        return path

    def bfs(self, starting_vertex: str):
        path = list()
        visited = set()
        q = [starting_vertex]
        while q:
            vertex = q.pop(0)
            path.append(vertex)
            visited.add(vertex)
            for v in sorted(self.adjacency_dictionary.setdefault(vertex, [])):
                if v not in visited and v not in q:
                    q.append(v)
        return path


graph_type, start_vertex, search_type = stdin.readline().split()
graph = Graph(graph_type)
for line in stdin.readlines():
    if len(line.split()) == 2:
        starting_vertex, ending_vertex = line.split()
        graph.add_edge(starting_vertex, ending_vertex)
if search_type == 'd':
    for v in graph.dfs(start_vertex, [], set()): print(v)
else:
    for v in graph.bfs(start_vertex): print(v)

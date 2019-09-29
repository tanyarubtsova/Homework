from collections import deque


class Graph:
    def __init__(self):
        self.g = []
        self.n = -1

    def add_edge(self, b, e):
        while (self.n < b) or (self.n < e):
            self.g.append([])
            self.n += 1
        self.g[b].append(e)
        self.g[e].append(b)
        self.visited = []

    def dfs1(self, v):
        if v not in self.visited:
            print(v)
            self.visited.append(v)
            for i in self.g[v]:
                self.dfs1(i)

    def dfs(self, v):
        dfs1(v)
        self.visited = []

    def bfs(self, v):
        dist = [0] * (self.n + 1)
        used = [False] * (self.n + 1)
        q = deque([v])
        used[v] = True
        while q:
            u = q.popleft()
            print(u)
            for v in self.g[u]:
                if not used[v]:
                    dist[v] = dist[u] + 1
                    used[v] = True
                    q.append(v)

    def print_graph(self):
        print(self.g)
'''
g = Graph()
for i in range (5):
    b = int(input())
    e = int(input())
    g.add_edge(b, e)
g.print_graph()
g.dfs(0)
g.bfs(0)
'''
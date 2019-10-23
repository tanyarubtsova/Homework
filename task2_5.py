'''task 2 program 5'''


class Graph:
    def __init__(self):
        self.graph = []
        self.count_of_vertexes = -1

    def add_edge(self, begin, end, weight):
        while(self.count_of_vertexes < begin) or (self.count_of_vertexes < end):
            self.graph.append([])
            self.count_of_vertexes += 1
        self.graph[begin].append((end, weight))
        self.graph[end].append((begin, weight))

    def Dijkstra(self, start, end):
        INF = 1000000000000000
        dist = [INF] * (self.count_of_vertexes + 1)
        dist[start] = 0
        prnt = [0] * (self.count_of_vertexes + 1)
        used = [False] * (self.count_of_vertexes + 1)
        for i in range(self.count_of_vertexes + 1):
            v = -1
            for j in range (self.count_of_vertexes + 1):
                if (used[j] == False) and ((v == -1) or (dist[j] < dist[v])):
                    v = j
            if (dist[v] == INF):
                break
            used[v] = True
            for j in range(len(self.graph[v])):
                t = self.graph[v][j][0]
                l = self.graph[v][j][1]
                if (dist[v] + l < dist[t]):
                    dist[t] = dist[v] + l
                    prnt[t] = v
        #print(*dist)
        #print(dist[end])
        #print(prnt)
        path = []
        v = end
        while v != start:
            path.append(v)
            v = prnt[v]
        path.append(start)
        path.reverse()
        print(*path)

    def find_path(self, start, end):
        self.Dijkstra(start, end)

    def print_graph(self):
        print(self.graph)

g = Graph()
while 1:
    s = input().split()
    if len(s) != 2:
        b, e, w = [int(i) for i in s]
        g.add_edge(b, e, w)
    else:
        nodeStart, nodeEnd = int(s[0]), int(s[1])
        break
#g.print_graph()
#g.Dijkstra(0)
g.find_path(nodeStart, nodeEnd)

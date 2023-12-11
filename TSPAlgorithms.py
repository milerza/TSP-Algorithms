import heapq
import networkx as nx
import math
import time
import matplotlib.pyplot as plt


def eliminate_repetitions(path):
    list_without_rep = []
    nodes_set = set()

    for element in path:
        if element not in nodes_set:
            list_without_rep.append(element)
            nodes_set.add(element)
    list_without_rep.append(list_without_rep[0])

    return list_without_rep


def path_edges_to_nodes(edges):
    path = []
    for edge in edges:
        path.append(edge[0])
    path.append(path[0])
    return path


class TSP:
    def __init__(self, graph: nx.Graph):
        self.graph = graph

    def calculate_weight_circuit(self, circuit):
        total_weight = 0
        n = len(circuit)
        for i in range(n - 1):
            total_weight += self.graph[circuit[i]][circuit[i + 1]]['weight']

        return total_weight

    def twice_around_the_three(self):
        mst = nx.minimum_spanning_tree(self.graph)
        ordered_nodes = list(nx.dfs_preorder_nodes(mst))
        ordered_nodes.append(ordered_nodes[0])
        total_weight = self.calculate_weight_circuit(ordered_nodes)
        return ordered_nodes, total_weight

    def christofides_algorithm(self):
        mst = nx.minimum_spanning_tree(self.graph)

        G = self.graph.copy()
        G.remove_nodes_from([i for i, level in mst.degree if not level % 2 == 1])

        path = nx.MultiGraph()

        path.add_edges_from(mst.edges)

        edges = nx.min_weight_matching(G)
        path.add_edges_from(edges)
        circuit = nx.eulerian_circuit(path)

        sol = path_edges_to_nodes(circuit)
        sol = eliminate_repetitions(sol)

        total_weight = self.calculate_weight_circuit(sol)

        return sol, total_weight

    def branch_and_bound(self):
        def bound(path, G):
            ub = 0
            linked_nodes = set(path)

            for i in range(len(path) - 1):
                current_node = path[i]
                available_edges = [G[current_node][neighbor]['weight'] for neighbor in G.neighbors(current_node)]
                available_edges.sort()
                min_edge1_weight = available_edges[0]

                next_node = path[i + 1]
                min_edge2_weight = G[current_node][next_node]['weight']

                ub += (min_edge1_weight + min_edge2_weight) / 2

            for node in G.nodes:
                if node not in linked_nodes:
                    available_edges = [G[node][neighbor]['weight'] for neighbor in G.neighbors(node)]
                    available_edges.sort()
                    min_edge1_weight = available_edges[0]
                    min_edge2_weight = available_edges[1]
                    ub += (min_edge1_weight + min_edge2_weight) / 2

            return ub

        n = self.graph.number_of_nodes()

        # upper bound, level, cost, path
        root = (bound([1], self.graph), 1, 0, [1])

        queue = []
        heapq.heappush(queue, root)
        best = math.inf
        sol = []

        start_time = time.time()
        while queue or (time.time() - start_time <= 90):
            node = heapq.heappop(queue)
            if node[1] > n:
                if best > node[2]:
                    best = node[2]
                    sol = node[3]

            elif node[0] < best:
                s = node[3]
                if node[1] < n:
                    for k in range(1, n + 1):
                        if k not in node[3]:
                            bs = bound(s + [k], self.graph)
                            if self.graph.has_edge(s[-1], k) and bs < best:
                                heapq.heappush(queue,
                                               (bs, node[1] + 1, node[2] + self.graph[s[-1]][k]['weight'], s + [k]))
                elif self.graph.has_edge(s[-1], 1) and bound(s + [1], self.graph) < best and all(
                        i in node[3] for i in range(2, n + 1)):
                    heapq.heappush(queue, (
                        bound(s + [1], self.graph), node[1] + 1, node[2] + self.graph[s[-1]][1]['weight'], s + [1]))

        total_weight = self.calculate_weight_circuit(sol)

        return sol, total_weight

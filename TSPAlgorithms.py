import networkx as nx


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

    def twice_around_the_three(self):
        mst = nx.minimum_spanning_tree(self.graph)
        ordered_nodes = list(nx.dfs_preorder_nodes(mst, source=0))
        ordered_nodes = eliminate_repetitions(ordered_nodes)
        return ordered_nodes

    def christofides_algorithm(self):
        mst = nx.minimum_spanning_tree(self.graph)
        degree_nodes = mst.degree()
        s = []
        for node in degree_nodes:
            if node[1] % 2 == 1:
                s.append(node[0])

        odd_subgraph = mst.subgraph(s)
        m = nx.min_weight_matching(odd_subgraph)
        t = mst.add_weighted_edges_from(nx.edges(m))
        path = nx.eulerian_circuit(t, source=0)
        path = path_edges_to_nodes(path)
        path = eliminate_repetitions(path)

        return path

    def branch_and_bound(self):
        return



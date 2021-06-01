from collections import defaultdict


class Edge:
    def __init__(self, from_stop_id, to_stop_id, travel_time, trip_id):
        self.trip_id = trip_id
        self.travel_time = travel_time
        self.to_stop_id = to_stop_id
        self.from_stop_id = from_stop_id
        self.weight = travel_time


class Node:
    def __init__(self, stop_id):
        self.stop_id = stop_id


class AdjNode:
    def __init__(self, stop_id, weight):
        self.stop_id = stop_id
        self.weight = weight


class Graph2:

    def __init__(self, nodes):
        self.edges = []
        self.distances = {}
        # self.adjacency_list = [[node.stop_id, []] for node in nodes]
        self.adjacency_list = defaultdict(list)
        self.nodes = nodes

    def connect_dir(self, node1, node2, trip_id, weight=1):
        self.adjacency_list[node1].append((node2, weight, trip_id))

    def connect(self, node1, node2, trip_id, weight=1):
        self.connect_dir(node1, node2, weight, trip_id)
        self.connect_dir(node2, node1, weight, trip_id)

    def connections(self, node):
        return self.adjacency_list[node]

    # def add_node(self, stop_id):
    #     self.nodes.add(stop_id)
    #
    def add_node(self, node):
        self.nodes.append(node)
        node.index = len(self.nodes) - 1

    def add_edge(self, from_stop_id, to_stop_id,  travel_time, trip_id):
        edge = Edge(from_stop_id, to_stop_id,  travel_time, trip_id)
        self.edges.append(edge)
    #
    # def build_adj(self):
    #     for i in self.nodes:
    #         self.adjacency_list[i] = []
    #     for e in self.edges:
    #         adj_node = AdjNode(e.to_stop_id, e.travel_time)
    #         self.adjacency_list[e.from_stop_id].append(adj_node)


def dijkstra2(graph, from_stop_id):

    visited = {from_stop_id: 0}
    path = {}
    time = {from_stop_id: 0}
    nodes = set(graph.nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node

        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge in graph.edges[min_node]:
            weight = current_weight + graph.distances[(min_node, edge)]
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    return path


def penalty(current, adjacent):
    intersected_lines = []
    penaltyf = 0
    for l in current:
        if l in adjacent:
            intersected_lines.append(l)
    if len(intersected_lines) == 0:
        penaltyf = 3
        intersected_lines.append(adjacent)

    return penaltyf, intersected_lines
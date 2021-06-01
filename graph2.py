

class Edge:
    def __init__(self, from_stop_id, to_stop_id, departure_time, travel_time, trip_id):
        self.departure_time = departure_time
        self.from_stop_id = from_stop_id
        self.to_stop_id = to_stop_id
        self.travel_time = travel_time
        self.trip_id = trip_id
        self.weight = travel_time


class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = dict()
        self.weight = {}
        # self.adjacency_list = [[None] for _ in range(N)]

    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, from_stop_id, to_stop_id, departure_time, travel_time, trip_id):
        edge = Edge(from_stop_id, to_stop_id, departure_time, travel_time, trip_id)
        if from_stop_id in self.edges:
            from_stop_id_edges = self.edges[from_stop_id]
        else:
            self.edges[from_stop_id] = dict()
            from_stop_id_edges = self.edges[from_stop_id]
        from_stop_id_edges[to_stop_id] = edge


def min_travel_time(q, travel_time):
    """
    Returns the node with the smallest distance in q.
    """
    min_node = None
    for node in q:
        if min_node is None:
            min_node = node
        elif travel_time[node] < travel_time[min_node]:
            min_node = node

    return min_node


def dijkstra(graph, source):
    all_stops = set()
    travel_time = {}
    visited_stops = {}
    trip_ids = {}
    departure_times = {}

    for stop in graph.nodes:
        travel_time[stop] = float('inf')
        visited_stops[stop] = float('inf')
        all_stops.add(stop)

    # distance from source to source
    travel_time[source] = 0

    while all_stops:
        # node with the least distance selected first
        curr_stop = min_travel_time(all_stops, travel_time)

        all_stops.remove(curr_stop)

        if curr_stop in graph.edges:
            for _, v in graph.edges[curr_stop].items():
                if v.trip_id not in trip_ids:
                    v.weight += 5
                alt = travel_time[curr_stop] + v.travel_time + v.weight
                if alt < travel_time[v.to_stop_id]:
                    # a shorter path to v has been found
                    travel_time[v.to_stop_id] = alt - v.weight
                    visited_stops[v.to_stop_id] = curr_stop#, v.trip_id
                    trip_ids[v.to_stop_id] = v.trip_id
                    departure_times[v.to_stop_id] = v.departure_time
                else:
                    trip_ids[v.to_stop_id] = v.trip_id
                    departure_times[v.to_stop_id] = v.departure_time

    return travel_time, visited_stops


def to_array(prev, from_node, dist):
    """Creates an ordered list of labels as a route."""
    previous_node = prev[from_node]
    previous_travel_time = dist[from_node]
    route = [from_node]
    times = [previous_travel_time]
    while previous_node != float('inf'):
        route.append(previous_node)
        times.append(previous_travel_time)
        temp = previous_node
        previous_node = prev[temp]
        previous_travel_time = dist[temp]

    route.reverse()
    times.reverse()
    return route, times



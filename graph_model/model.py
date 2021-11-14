import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, name):
        self.name = name
        self.destinations = []
        self.start = False

    def add_destination(self, destination, weight):
        self.destinations.append([destination, weight])

    def set_start(self):
        self.start = True

class Edge:
    def __init__(self, start, end, weight, directional):
        self.start = start
        self.end = end
        self.weight = weight
        self.directional = directional
        self.connect_nodes()

    def __repr__(self):
        return [self.start, self.end, self.weight]

    def connect_nodes(self):
        self.start.add_destination(self.end, self.weight)
        if not self.directional:
            self.end.add_destination(self.start, self.weight)

class Graph:
    def __init__(self, data):
        self.nodes = []
        self.edges = []
        self.build_from_data(data)

    def get_node_names(self):
        return [n.name for n in self.nodes]

    def add_node(self, name):
        node = Node(name)
        self.nodes.append(node)

    def get_node_by_name(self, name):
        if name in self.get_node_names():
            return [n for n in self.nodes if n.name==name][0]
        else:
            raise ValueError(f'No node named {name}.')

    def add_edge(self, start, end, weight, directional):
        start = self.get_node_by_name(start)
        end = self.get_node_by_name(end)
        self.edges.append(Edge(start, end , weight, directional))

    # input connection as list of [start_node_name, end_node_name, weight, True if connection is one-directional]
    def add_connection(self, connection):
        start = connection[0]
        end = connection[1]
        weight = connection[2]
        if len(connection) > 3:
            directional = connection[3]
        else:
            directional = False
        if start not in self.get_node_names():
            self.add_node(start)
        if end not in self.get_node_names():
            self.add_node(end)
        self.add_edge(start, end, weight, directional)

    # build graph from a list of connections
    def build_from_data(self, data):
        for row in data:
            self.add_connection(row)

    def set_starting_point(self, start):
        node = self.get_node_by_name(start)
        node.set_start()

    def draw(self, save=''):
        G = nx.DiGraph()

        directed_edges = []
        for node in self.nodes:
            for d in node.destinations:
                directed_edges.append([node.name, d[0].name, d[1]])

        for edge in directed_edges:
            G.add_edges_from([(edge[0], edge[1])], weight=edge[2])

        edge_labels = dict(
            [((u, v,), d['weight']) for u, v, d in G.edges(data=True)]
        )

        v = ['red' if i.start else 'blue' for i in self.nodes]

        pos = nx.spring_layout(G)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        nx.draw(G, pos, node_color=v, node_size=10000/len(v), with_labels=True)
        if save:
            plt.savefig('./'+save)
        else:
            plt.show()

if __name__ == '__main__':
    data = [
        ['A', 'B', 2],
        ['A', 'C', 3, True],
        ['B', 'C', 1]
    ]
    graph = Graph(data)
    graph.set_starting_point('A')
    graph.draw()

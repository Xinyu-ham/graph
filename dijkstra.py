from graph_model.model import Graph, Node, Edge
import numpy as np

# Dijkstra algorithm for POSITIVELY weighted edges only
class Route:
    def __init__(self, destination, cost, last_route=None, starting_point=None):
        if not last_route:
            if destination == starting_point:
                self.path = [starting_point.name]
            else:
                self.path = [starting_point.name, destination.name]
            self.cost = 0
        else:
            if type(last_route) != Route:
                raise TypeError('Please input a Route object')
            self.path = last_route.path + [destination.name,]
            self.cost = int(last_route.cost) + int(cost)
        self.destination = destination


class DijkstraSolver:
    def __init__(self, graph):
        self.graph = graph

    def solve(self):
        nodes = self.graph.nodes
        try:
            start_nodes = [n for n in nodes if n.start]
            if len(start_nodes) > 1:
                print('More than one starting node.')
                return None
            else:
                start_node = start_nodes[0]
        except IndexError as e:
            print('Starting node is not set.')

        cost_map = {n:np.inf for n in nodes}
        cost_map[start_node] = 0
        path_map = {n: None for n in nodes}
        path_map[start_node] = Route(start_node, 0, starting_point=start_node)

        evaluated_nodes = []
        def evaluate_node(node, cost_map, path_map):
            d_list = []
            for destination in node.destinations:
                d = destination[0]
                d_list.append(d)
                cost = destination[1]
                # print(d.name, cost, path_map[node].path, path_map[node].cost)
                route = Route(d, cost, last_route=path_map[node])
                if route.cost < cost_map[d]:
                    cost_map[d] = route.cost
                    path_map[d] = route
            return d_list, cost_map, path_map

        to_do, cost_map, path_map = evaluate_node(start_node, cost_map, path_map)
        evaluated_nodes.append(start_node)

        for node in to_do:
            if node not in evaluated_nodes:
                d_list, cost_map, path_map = evaluate_node(node, cost_map, path_map)
                evaluated_nodes.append(node)
                to_do += d_list
        return {n.name:{
                            'cost':cost_map[n],
                            'shortest_path':path_map[n].path
                        } for n in cost_map}





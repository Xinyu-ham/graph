from graph_model.model import Graph
from dijkstra import DijkstraSolver
import pandas as pd

data = [
    ['A', 'B', '2'],
    ['A', 'C', '3'],
    ['B', 'D', '4'],
    ['C', 'D', '1'],
    ['B', 'E', '3'],
    ['C', 'F', '2'],
    ['D', 'G', '1'],
    ['E', 'G', '3'],
    ['E', 'F', '2'],
    ['F', 'H', '3'],
    ['D', 'H', '4'],
]

graph = Graph(data)
graph.set_starting_point('A')
graph.draw('example.png')

ds = DijkstraSolver(graph)
df = ds.solve()
df = pd.DataFrame(df).transpose()
print(df)
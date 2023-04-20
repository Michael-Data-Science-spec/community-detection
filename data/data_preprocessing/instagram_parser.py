import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

edges = [(1, 2, {"weight": 1}), (2, 3, {"weight": 10})]
nodes = [(1, {"color":"green"}), (3, {"color":"red"}), (2, {"color":"blue"})]
cmap = plt.cm.get_cmap('viridis')  # You can choose any colormap you like

node_labels = np.array([1, 2, 2])

# Normalize the node labels to be between 0 and 1
norm = plt.Normalize(vmin=node_labels.min(), vmax=node_labels.max())
node_colors = cmap(norm(node_labels))
color_map = node_colors

G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)
nx.draw_networkx(G, node_color = color_map)
plt.show()


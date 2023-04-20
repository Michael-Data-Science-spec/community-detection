import networkx as nx
import matplotlib.pyplot as plt

# create an example graph with 6 nodes and 5 edges
G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4, 5, 6])
G.add_edges_from([(1,2), (2,3), (3,4), (4,5), (5,6)])

# assign community labels to each node
communities = {
    1: 0,
    2: 0,
    3: 1,
    4: 1,
    5: 2,
    6: 2
}

# assign custom positions to each node based on community membership
positions = {}
for node, community in communities.items():
    if community == 0:
        positions[node] = [0, community]
    elif community == 1:
        positions[node] = [1, community]
    else:
        positions[node] = [2, community]

# calculate the layout using spring_layout
pos = nx.spring_layout(G, pos=positions)

# draw the graph
nx.draw(G, pos=pos, with_labels=True)
plt.show()
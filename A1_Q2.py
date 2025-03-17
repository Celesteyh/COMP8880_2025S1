import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# -------------------Q2.1-------------------
print('-------------------Q2.1-------------------')
# load files
def load_nodes(file_path):
    nodes = []
    with open(file_path, 'r') as f:
        for line in f:
            node = int(line.strip().split('|')[1])
            nodes.append(node)
    return nodes


def load_edges(file_path):
    edges = []
    with open(file_path, 'r') as f:
        for line in f:
            edge = line.strip().split()
            edges.append((int(edge[0]), int(edge[1])))
    return edges


node_path = '.\\global-cities.dat'
edge_path = '.\\global-net.dat'
nodes = load_nodes(node_path)
edges = load_edges(edge_path)

network = nx.Graph()
network.add_nodes_from(nodes)
network.add_edges_from(edges)
print(f'There are {network.number_of_nodes()} nodes in the network')
print(f'There are {network.number_of_edges()} edges in the network')

# -------------------Q2.2-------------------
print('-------------------Q2.2-------------------')
# connected components
components = [network.subgraph(c).copy() for c in nx.connected_components(network)]
print(f'There are {len(components)} connected components in the network')
G = sorted(components, key=len, reverse=True)[0]
print(f'The largest connected component has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges')

# -------------------Q2.3-------------------
print('-------------------Q2.3-------------------')
# map node id to node name
map_id_name = {}
with open(node_path, 'r') as f:
    for line in f:
        node = line.strip().split('|')
        map_id_name[int(node[1])] = node[2]
# top 10 nodes with highest degree in G
top10_nodes = sorted(G.degree, key=lambda x: x[1], reverse=True)[:10]
top10_nodes = [(map_id_name[node[0]], node[1]) for node in top10_nodes]
print(f'Top 10 nodes with highest degree and the number of nodes they are connected to in G:{top10_nodes}')

# -------------------Q2.4-------------------
print('-------------------Q2.4-------------------')
# degree distribution
def plot_degree(graph, title, log_scale=False):
    # get a list of degree counts where the index is the degree and the value is the frequency
    degree_freq = nx.degree_histogram(graph)
    # filter out the 0 degree nodes
    filtered_n_nodes = sum(degree_freq[1:])
    degrees = []
    freqs = []
    for degree, count in enumerate(degree_freq):
        if degree != 0 and count != 0:
            degrees.append(degree)
            freqs.append(count / filtered_n_nodes)

    # plot
    fig, ax = plt.subplots()
    plt.scatter(degrees, freqs, alpha=0.8, s=20, edgecolors='darkblue')
    plt.xlabel("Degree")
    plt.ylabel("Fraction of Nodes")
    # restrict the x-axis
    min_degree, max_degree = min(degrees), max(degrees)
    plt.xlim(min_degree, max_degree)
    plt.title("Degree Distribution of " + title)
    if log_scale:
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Degree (log base 10)")
        plt.ylabel("Fraction of Nodes (log base 10)")
        ax.xaxis.set_major_formatter(ScalarFormatter())
        ax.yaxis.set_major_formatter(ScalarFormatter())
        plt.title("Degree Distribution of " + title + " (log-log scale)")
    plt.show()


plot_degree(G, "G", False)
plot_degree(G, "G", True)

# -------------------Q2.5-------------------
print('-------------------Q2.5-------------------')
# diameter of G
diameter = nx.diameter(G)
print(f'The diameter of G is {diameter}')
# get the set of nodes with eccentricity equal to the diameter
node_pairs = nx.periphery(G)
# print(node_pairs)  # [477, 3414]
# since it only contains 2 nodes, the shortest path between them is the diameter, and they are what we need
print(f'The airports/cities that have a longest shortest path between them are {map_id_name[node_pairs[0]]} and {map_id_name[node_pairs[1]]}')

# -------------------Q2.6-------------------
print('-------------------Q2.6-------------------')
# map node name to node id
map_name_id = {v: k for k, v in map_id_name.items()}
print(f'The id of Canberra is {map_name_id["Canberra"]}')  # 501
print(f'The id of Cape Town is {map_name_id["Cape Town"]}')  # 635
# shortest path between Canberra and Cape Town
shortest_path = nx.shortest_path(network, source=501, target=635)
# map node id to node name
shortest_path = [map_id_name[node] for node in shortest_path]
print(f'The shortest path between Canberra and Cape Town goes through the following airports/cities: {shortest_path[1:-1]}')

# -------------------Q2.7-------------------
print('-------------------Q2.7-------------------')
betweenness = nx.betweenness_centrality(G)
top10_betweenness_tuple = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:10]
top10_betweenness = [(map_id_name[node[0]], node[1]) for node in top10_betweenness_tuple]
print(f'Top 10 airports/cities with highest betweenness centrality in G: {top10_betweenness}')

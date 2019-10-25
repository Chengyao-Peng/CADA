import pandas as pd
import networkx as nx
from node2vec import Node2Vec

input_dir = '/home/peng/PycharmProjects/featurematch/data/processed/omim.triples'
df = pd.read_csv(input_dir, sep='\t', header=None).loc[:, [0, 2]]
edges = df.values.tolist()

tuple_edges = []
for edge in edges:
    tuple_edge = tuple(edge)
    tuple_edges.append(tuple_edge)


G = nx.Graph()
G.add_edges_from(tuple_edges)
print('Number of nodes:' + str(G.number_of_nodes()))
print('Number of edges:' + str(G.number_of_edges()))
print('All connected:' + str(nx.is_connected(G)))

node2vec = Node2Vec(G, dimensions=100, walk_length=30, num_walks=10, workers=1)
model = node2vec.fit(window=10, min_count=1, batch_words=4)
model.wv.save_word2vec_format('/home/peng/PycharmProjects/featurematch/result/omim/omim.embeddings')
model.save('/home/peng/PycharmProjects/featurematch/result/omim/omim.model')
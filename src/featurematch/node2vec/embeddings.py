import os
import pandas as pd
import networkx as nx
from node2vec import Node2Vec
from typing import List, Optional
from ..paths import DATA_DIRECTORY, MODEL_DIRECTORY

######mapping before do it!!!!!!!!!!!!

def embeddings(
        *,
        dimensions: int,
        walk_length: int,
        p: int,
        q: int,
        num_walks: int,
        with_patients: bool,
        window: int,
        output_directory: str,
        ):
    if with_patients:
        indir = os.path.join(DATA_DIRECTORY, 'processed', 'final', 'with_patients', 'with_patients_mapped.triples')
        embedding_outdir = os.path.join(output_directory, 'with_patients', 'with_patients.embeddings')
        model_outdir = os.path.join(output_directory, 'with_patients', 'with_patients.model')
    else:
        indir = os.path.join(DATA_DIRECTORY, 'processed', 'final', 'without_patients', 'without_patients_mapped.triples')
        embedding_outdir = os.path.join(output_directory, 'without_patients', 'without_patients.embeddings')
        model_outdir = os.path.join(output_directory, 'without_patients', 'without_patients.model')

    # Generate graph
    df = pd.read_csv(indir, sep='\t', header=None)
    df = df.loc[:, [0, 2]]
    edges = df.values.tolist()

    tuple_edges = []
    for edge in edges:
        tuple_edge = tuple(edge)
        tuple_edges.append(tuple_edge)

    G = nx.Graph()
    G.add_edges_from(tuple_edges)
    Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
    G0 = G.subgraph(Gcc[0])

    print('Graph generated!')
    print('Number of nodes:' + str(G.number_of_nodes()))
    print('Number of edges:' + str(G.number_of_edges()))
    print('All connected:' + str(nx.is_connected(G)))
    print('Number of connected components:' + str(nx.number_connected_components(G)))
    print()
    print('Largest component subgraph generated!')
    print('Number of nodes:' + str(G0.number_of_nodes()))
    print('Number of edges:' + str(G0.number_of_edges()))
    print('All connected:' + str(nx.is_connected(G0)))
    print('Number of connected components:' + str(nx.number_connected_components(G0)))

    node2vec = Node2Vec(G0, dimensions=dimensions, walk_length=walk_length, num_walks=num_walks, workers=1, p=p, q=q)
    model = node2vec.fit(window=window, min_count=1, batch_words=4)
    model.wv.save_word2vec_format(embedding_outdir)
    model.save(model_outdir)

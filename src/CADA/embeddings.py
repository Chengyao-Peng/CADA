#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
import networkx as nx
from node2vec import Node2Vec
from featurematch.paths import DATA_DIRECTORY, MODEL_DIRECTORY
from featurematch.split import split
from featurematch.triples_patients import triples_patients
from featurematch.triples_hierarchical_hpo import triples_hierarchical_hpo
from featurematch.triples_disease_hpo import triples_disease_hpo


def embeddings(
        *,
        hpoteam: bool,
        with_patients: bool,
        train_size: int,
        dimensions: int,
        walk_length: int,
        p: int,
        q: int,
        num_walks: int,
        window: int,
        output_directory: str,
        ):

    triples = []
    # get triples of hpo-hpo 'is_a' relationships
    hpo_triples = triples_hierarchical_hpo()
    triples += hpo_triples
    # get triples of disease-hpo 'is_feature_of_disease' relationships
    disease_hpo_triples = triples_disease_hpo(hpoteam)
    triples += disease_hpo_triples

    if with_patients:
        output_directory = os.path.join(MODEL_DIRECTORY, output_directory)
        embedding_outdir = os.path.join(output_directory, 'with_patients.embeddings')
        model_outdir = os.path.join(output_directory, 'with_patients.model')
        # get triples of patients 'has_feature' and 'has disease' relationships
        train_size = train_size
        train, test = split(train_size, output_directory)
        patients_triples = triples_patients(train)
        triples += patients_triples

    else:
        output_directory = os.path.join(MODEL_DIRECTORY, output_directory)
        embedding_outdir = os.path.join(output_directory, 'without_patients.embeddings')
        model_outdir = os.path.join(output_directory, 'without_patients.model')

    # Generate graph
    edges = []
    for triple in triples:
        triple.pop(1)
        triple = tuple(triple)
        edges.append(triple)
    G = nx.Graph()
    G.add_edges_from(edges)
    #
    #
    # Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
    # G0 = G.subgraph(Gcc[0])
    #
    # print('Graph generated!')
    # print('Number of nodes:' + str(G.number_of_nodes()))
    # print('Number of edges:' + str(G.number_of_edges()))
    # print('All connected:' + str(nx.is_connected(G)))
    # print('Number of connected components:' + str(nx.number_connected_components(G)))
    # print()
    # print('Largest component subgraph generated!')
    # print('Number of nodes:' + str(G0.number_of_nodes()))
    # print('Number of edges:' + str(G0.number_of_edges()))
    # print('All connected:' + str(nx.is_connected(G0)))
    # print('Number of connected components:' + str(nx.number_connected_components(G0)))
    #
    # node2vec = Node2Vec(G0, dimensions=dimensions, walk_length=walk_length, num_walks=num_walks, workers=1, p=p, q=q)
    # model = node2vec.fit(window=window, min_count=1, batch_words=4)
    # model.wv.save_word2vec_format(embedding_outdir)
    # model.save(model_outdir)
    #

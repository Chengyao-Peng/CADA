#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
import pandas as pd
import networkx as nx
from node2vec import Node2Vec
from CADA.paths import MODEL_DIRECTORY
from CADA.split import split
from CADA.triples_patients import triples_patients
from CADA.triples_hierarchical_hpo import triples_hierarchical_hpo
from CADA.triples_disease_hpo  import triples_disease_hpo
from CADA.triples_gene_hpo import triples_gene_hpo
from CADA.triples_disease_gene import triples_disease_gene

logger = logging.getLogger(__name__)

def embeddings(
        *,
        disease_hpoteam = bool,
        gene_frequent: bool,
        with_patients: bool,
        dimensions: int,
        walk_length: int,
        p: int,
        q: int,
        num_walks: int,
        window: int,
        output_directory: str,
        ):
    """
    :param prioritization:
    :param disease_hpoteam:
    :param gene_frequent:
    :param with_patients:
    :param dimensions:
    :param walk_length:
    :param p:
    :param q:
    :param num_walks:
    :param window:
    :param output_directory:
    :return:
    """

    triples = []
    # get triples of hpo-hpo 'is_a' relationships
    logger.info(f'Adding hpo hierarchical relationships')

    hpo_triples = triples_hierarchical_hpo()
    triples += hpo_triples

    # get triples of disease-hpo 'is_feature_of_disease' relationships
    logger.info(f'Adding disease-hpo relationships')
    disease_hpo_triples = triples_disease_hpo(disease_hpoteam)
    triples += disease_hpo_triples
    # get triples of gene-hpo 'is_feature_of_gene' relationships
    logger.info(f'Adding gene-hpo relationships.')
    gene_hpo_triples = triples_gene_hpo(gene_frequent)
    triples += gene_hpo_triples
    # get triples of disease-gene 'mutation_contributes_to_disease' relationships
    logger.info(f'Adding disease-gene relationships')
    disease_gene_triples = triples_disease_gene()
    triples += disease_gene_triples

    if with_patients:
        output_directory = os.path.join(MODEL_DIRECTORY, output_directory)
        embedding_outdir = os.path.join(output_directory, 'with_patients.embeddings')
        model_outdir = os.path.join(output_directory, 'with_patients.model')
        # get triples of patients 'has_feature' and 'has disease' relationships
        train = split(output_directory)
        train_patients_triples = triples_patients(train)
        triples += train_patients_triples
        logger.info(f'Patients and their features and diseases relationships added')

    else:
        output_directory = os.path.join(MODEL_DIRECTORY, output_directory)
        embedding_outdir = os.path.join(output_directory, 'without_patients.embeddings')
        model_outdir = os.path.join(output_directory, 'without_patients.model')

    # Save triples
    all_triples_tsv = os.path.join(MODEL_DIRECTORY, output_directory, 'all.triples')
    all_triples = pd.DataFrame(triples)
    all_triples.to_csv(all_triples_tsv, header=None, index=False, sep='\t')

    # Generate graph
    edges = []
    for triple in triples:
        triple.pop(1)
        triple = tuple(triple)
        edges.append(triple)
    G = nx.Graph()
    G.add_node('HP:0000001')
    G.add_edges_from(edges)
    logger.info(f'Number of nodes: {G.number_of_nodes()}')
    logger.info(f'Number of edges: {G.number_of_edges()}')

    Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
    G0 = G.subgraph(Gcc[0])

    # node2vec = Node2Vec(G0, dimensions=dimensions, walk_length=walk_length, num_walks=num_walks, workers=1, p=p, q=q)
    # model = node2vec.fit(window=window, min_count=1, batch_words=4)
    # model.wv.save_word2vec_format(embedding_outdir)
    # model.save(model_outdir)
    #

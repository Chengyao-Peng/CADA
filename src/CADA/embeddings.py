#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
import csv
import pandas as pd
import networkx as nx
from node2vec import Node2Vec
from CADA.paths import DATA_DIRECTORY, MODEL_DIRECTORY
from CADA.split import split
from CADA.triples_patients import triples_patients
from CADA.triples_hierarchical_hpo import triples_hierarchical_hpo
from CADA.triples_disease_hpo import triples_disease_hpo

logger = logging.getLogger(__name__)

def embeddings(
        *,
        # prioritization: str,
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


    # get triples of hpo-hpo 'is_a' relationships
    triples = []
    hpo_triples = triples_hierarchical_hpo()
    triples += hpo_triples
    logger.info(f'Hpo hierarchical relationships added')
    # get triples of disease-hpo 'is_feature_of_disease' relationships
    disease_hpo_triples = triples_disease_hpo(hpoteam)
    triples += disease_hpo_triples
    logger.info(f'Disease-hpo relationships added')


    if with_patients:
        output_directory = os.path.join(MODEL_DIRECTORY, output_directory)
        embedding_outdir = os.path.join(output_directory, 'with_patients.embeddings')
        model_outdir = os.path.join(output_directory, 'with_patients.model')
        # get triples of patients 'has_feature' and 'has disease' relationships
        train_size = train_size
        train, test = split(train_size, output_directory)
        patients_triples = triples_patients(train)
        triples += patients_triples
        logger.info(f'Patients and their features and diseases relationships added')

    else:
        output_directory = os.path.join(MODEL_DIRECTORY, output_directory)
        embedding_outdir = os.path.join(output_directory, 'without_patients.embeddings')
        model_outdir = os.path.join(output_directory, 'without_patients.model')

    # Save triples
    triples_file = os.path.join(MODEL_DIRECTORY, output_directory, 'all.triples')
    with open(triples_file, 'w', newline='') as outputfile:
        tsv_output = csv.writer(outputfile, delimiter='\t')
        tsv_output.writerow(triples)

    # Generate graph
    edges = []
    for triple in triples:
        triple.pop(1)
        triple = tuple(triple)
        edges.append(triple)
    G = nx.Graph()
    G.add_edges_from(edges)
    logger.info(f'Number of nodes: {G.number_of_nodes()}')
    logger.info(f'Number of edges: {G.number_of_edges()}')
    
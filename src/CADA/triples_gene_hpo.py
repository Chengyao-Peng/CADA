#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from CADA.paths import DATA_DIRECTORY
import pandas as pd


def triples_gene_hpo(frequent):
    predicate = 'is_feature_of_mutation'
    triples = []
    if frequent:
        in_file = os.path.join(DATA_DIRECTORY, 'raw', 'hpo', 'gene-hpo', 'ALL_SOURCES_FREQUENT_FEATURES_genes_to_phenotype.txt')
        out_file = os.path.join(DATA_DIRECTORY, 'processed', 'hpo', 'gene-hpo', 'genes_hpos_frequent.triples')
    else:
        in_file = os.path.join(DATA_DIRECTORY, 'raw', 'hpo', 'gene-hpo', 'ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt')
        out_file = os.path.join(DATA_DIRECTORY, 'processed', 'hpo', 'gene-hpo', 'genes_hpos.triples')
        gene_list = os.path.join(DATA_DIRECTORY, 'processed', 'hpo', 'gene-hpo', 'genes.list')

    with open(gene_list, 'w') as genefile:
        df = pd.read_csv(in_file, skiprows=1, header=None, sep='\t').applymap(str)
        for row in df.values.tolist():
            gene = row[0].strip()
            genefile.write(gene + '\n')

    with open(out_file, 'w') as outfile:
        df = pd.read_csv(in_file, skiprows=1, header=None, sep ='\t').applymap(str)
        df.iloc[:, 0] = 'Entrez:' + df.iloc[:, 0]
        for row in df.values.tolist():
            gene = row[0].strip()
            feature = row[3].strip()
            outfile.write(feature + '\t' + predicate + '\t' + gene + '\n')
            triples.append([feature, predicate, gene])

    return triples
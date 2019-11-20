#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from ....paths import DATA_DIRECTORY
import pandas as pd


def gene_hpo(frequent: False):
    predicate = 'is_feature_of_mutation'
    if frequent:
        input_file = os.path.join(DATA_DIRECTORY, 'raw', 'hpo', 'gene-hpo', 'ALL_SOURCES_FREQUENT_FEATURES_genes_to_phenotype.txt')
        output_file = os.path.join(DATA_DIRECTORY, 'processed', 'hpo', 'gene-hpo', 'genes_hpos_frequent.triples')
    else:
        input_file = os.path.join(DATA_DIRECTORY, 'raw', 'hpo', 'gene-hpo', 'ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt')
        output_file = os.path.join(DATA_DIRECTORY, 'processed', 'hpo', 'disease-hpo', 'genes_hpos.triples')

    df = pd.read_csv(input_file, skiprows=1, sep ='\t').applymap(str)

    with open(output_file, 'w') as outfile:
        for row in df.values.tolist():
            gene = "Entrez:" + row[0].strip()
            feature = row[3].strip()
            outfile.write(feature + '\t' + predicate[0] + '\t' + gene + '\n')
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from CADA.paths import DATA_DIRECTORY
import pandas as pd

def triples_gene_hpo():
    predicate = 'is_feature_of_mutation'
    triples = []
    in_file = os.path.join(DATA_DIRECTORY, 'raw', 'hpo', 'gene-hpo', 'genes_to_phenotype.txt')
    out_file = os.path.join(DATA_DIRECTORY, 'processed', 'hpo', 'gene-hpo', 'genes_hpos.triples')
    with open(in_file, 'r') as infile:
        with open(out_file, 'w') as outfile:
            df = pd.read_csv(infile, skiprows=1, header=None, sep ='\t').applymap(str)
            df.iloc[:, 0] = 'Entrez:' + df.iloc[:, 0]
            for row in df.values.tolist():
                gene = row[0].strip()
                feature = row[2].strip()
                outfile.write(feature + '\t' + predicate + '\t' + gene + '\n')
                triples.append([feature, predicate, gene])

    return triples
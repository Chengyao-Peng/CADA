#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from CADA.paths import DATA_DIRECTORY
import pandas as pd


def triples_disease_hpo(hpoteam):
    predicate = 'is_feature_of_disease'
    triples = []
    if hpoteam:
        in_file = os.path.join(DATA_DIRECTORY, 'raw', 'hpo', 'disease-hpo', 'phenotype_annotation_hpoteam.tab')
        out_file = os.path.join(DATA_DIRECTORY, 'processed', 'hpo', 'disease-hpo', 'disease-hpo_hpoteam.triples')
    else:
        in_file = os.path.join(DATA_DIRECTORY, 'raw', 'hpo', 'disease-hpo', 'phenotype_annotation.tab')
        out_file = os.path.join(DATA_DIRECTORY, 'processed', 'hpo', 'disease-hpo', 'diseases-hpo.triples')

    with open(out_file, 'w') as outfile:
        df = pd.read_csv(in_file, sep ='\t', header=None).applymap(str)
        # only retain annotations from 'OMIM'
        df = df.loc[df.iloc[:, 0] == 'OMIM']
        df.iloc[:, 1] = 'OMIM:' + df.iloc[:, 1]
        for row in df.values.tolist():
            disease = row[1].strip()
            feature = row[4].strip()
            outfile.write(feature + '\t' + predicate + '\t' + disease + '\n')
            triples.append([feature, predicate, disease])

    return triples
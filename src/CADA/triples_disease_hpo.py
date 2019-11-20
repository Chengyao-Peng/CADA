#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from featurematch.paths import DATA_DIRECTORY
import pandas as pd


def triples_disease_hpo(hpoteam: False):
    predicate = 'is_feature_of_disease'
    triples = []
    if hpoteam:
        input_file = os.path.join(DATA_DIRECTORY, 'raw', 'hpo', 'disease-hpo', 'phenotype_annotation_hpoteam.tab')
    else:
        input_file = os.path.join(DATA_DIRECTORY, 'raw', 'hpo', 'disease-hpo', 'phenotype_annotation.tab')

    df = pd.read_csv(input_file, sep ='\t', header=None).applymap(str)
    print(df.columns[0])

    # df = df[df.columns[0] == 'OMIM']
    # df.columns[1] = 'OMIM:' + df.columns[1]
    # # df.iloc[248:100369, [1]] = 'OMIM:' + df.iloc[248:100369, [1]]
    # # df.iloc[100369:, [1]] = 'ORPHA:' + df.iloc[100369:, [1]]
    # for row in df.values.tolist():
    #     disease = row[1].strip()
    #     feature = row[4].strip()
    #     triples.append([feature, predicate, disease])
    #
    # return triples
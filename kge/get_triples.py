#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

f = open("/home/peng/PycharmProjects/feature_match/result/triples.tsv", "w")

items = ['Case_ID', 'Gene', 'HPO_Features']
predicates = ['has_disorder', 'has_feature', 'is_feature_of']

df = pd.read_excel("/home/peng/PycharmProjects/feature_match/data/SupplementaryTable_PEDIA/SupplementaryTable1_03092019.xlsx")
df = df.head(679)
df_filtered = df.filter(items=['Case ID', 'Gene', 'HPO Features'])
df_filtered.columns = df_filtered.columns.str.replace(' ', '_')

for row in df_filtered.itertuples(index=False):
    features = getattr(row, items[2]).split(", ")
    case = str(getattr(row, items[0]))
    gene = getattr(row, items[1])
    f.write(case+'\t'+predicates[0]+'\t'+gene+'\n')
    for feature in features:
        feature = "_".join(feature.split())
        f.write(case+'\t'+predicates[1]+'\t'+feature+'\n')
        f.write(feature+'\t'+predicates[2]+'\t'+gene+'\n')

f.close()
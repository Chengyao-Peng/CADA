#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd

#items = ['Case_ID', 'Gene', 'HPO_Features']
items = ['Case_ID', 'Gene', 'HPO']
predicates = ['has_disorder', 'has_feature', 'is_feature_of']

df = pd.read_excel("../../data/raw/supplementary_table_PEDIA/SupplementaryTable1_03092019.xlsx")
df = df.head(679)

#df_filtered = df.filter(items=['Case ID', 'Gene', 'HPO Features'])
df_filtered = df.filter(items=['Case ID', 'Gene', 'HPO'])
df_filtered.columns = df_filtered.columns.str.replace(' ', '_')

with open("../../data/processed/supplementary_table_PEDIA/triples_PEDIA.tsv", "w") as f:
    for row in df_filtered.itertuples(index=False):
        features = getattr(row, items[2]).split(", ")
        case = str(getattr(row, items[0]))
        gene = getattr(row, items[1])
        f.write(case+'\t'+predicates[0]+'\t'+gene+'\n')
        for feature in features:
            feature = "_".join(feature.split())
            f.write(case+'\t'+predicates[1]+'\t'+feature+'\n')
            f.write(feature+'\t'+predicates[2]+'\t'+gene+'\n')




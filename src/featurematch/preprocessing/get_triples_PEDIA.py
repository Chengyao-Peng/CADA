#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd

#items = ['Case_ID', 'Gene', 'HPO_Features']
items = ['Case_ID', 'Gene', 'HPO', 'Diagnosis']
predicates = ['has_mutation', 'has_feature', 'is_feature_of_mutation', 'has_disease', 'is_feature_of_disease']

df = pd.read_excel("../../data/raw/supplementary_table_PEDIA/SupplementaryTable1_03092019.xlsx")
df = df.head(679)

#df_filtered = df.filter(items=['Case ID', 'Gene', 'HPO Features'])
df_filtered = df.filter(items=['Case ID', 'Gene', 'HPO', 'Diagnosis'])
df_filtered.columns = df_filtered.columns.str.replace(' ', '_')

with open("../../data/processed/supplementary_table_PEDIA/triples_PEDIA.tsv", "w") as f:
    for row in df_filtered.itertuples(index=False):
        patient = str(getattr(row, items[0]))
        gene = getattr(row, items[1])
        features = getattr(row, items[2]).split(", ")
        disease = getattr(row, items[3]).split(";")[0]

        f.write(patient + '\t' + predicates[0] + '\t' + gene + '\n')
        f.write(patient + '\t' + predicates[3] + '\t' + disease + '\n')
        for feature in features:
            f.write(patient + '\t' + predicates[1] + '\t' + feature + '\n')
            f.write(feature + '\t' + predicates[2] + '\t'+ gene + '\n')
            f.write(feature + '\t' + predicates[4] + '\t' + disease + '\n')




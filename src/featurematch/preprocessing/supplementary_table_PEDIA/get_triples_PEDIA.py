#!/usr/bin/env python3
# -*- coding: utf-8 -*-

predicates = ['has_mutation', 'has_feature', 'is_feature_of_mutation', 'has_disease', 'is_feature_of_disease']

with open("../../../../data/raw/supplementary_table_PEDIA/pedia.tsv") as infile:
    with open("../../../../data/processed/supplementary_table_PEDIA/pedia.triples", "w") as outfile:
        content = infile.read().splitlines()
        content = [x.split('\t') for x in content]
        for line in content:
            disease = line[0].strip()
            case = 'Patient:' + line[4].strip()
            gene = 'Entrez:' + line[5].strip()
            features = line[14].split(', ')
            for feature in features:
                outfile.write(case + '\t' + predicates[1] + '\t' + feature + '\n')
                outfile.write(feature + '\t' + predicates[2] + '\t' + gene + '\n')
                outfile.write(feature + '\t' + predicates[4] + '\t' + disease + '\n')
            outfile.write(disease + '\t' + predicates[0] + '\t' + gene + '\n')
            outfile.write(case + '\t' + predicates[3] + '\t' + disease + '\n')

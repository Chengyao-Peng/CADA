#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from CADA.paths import DATA_DIRECTORY
import pickle

with open(os.path.join(DATA_DIRECTORY, 'processed', 'ids', 'hpo_old_new.dict'), 'rb') as handle:
    hpo_dict = pickle.load(handle)

def triples_patients(gene, disease, patients):
    out_file = os.path.join(DATA_DIRECTORY, 'processed', 'patients', 'patients.triples')
    predicates = ['has_feature', 'has_disease', 'has_mutation']
    triples = []
    with open(out_file, 'w') as outfile:
        for patient in patients:
            patient_id = patient[0]
            disease = patient[1]
            if disease:
                outfile.write(patient_id + '\t' + predicates[1] + '\t' + disease + '\n')
                triples.append([patient_id, predicates[1], disease])
            features = patient[3].split(',')
            for feature in features:
                outfile.write(patient_id + '\t' + predicates[0] + '\t' + hpo_dict.get(feature, feature) + '\n')
                triples.append([patient_id, predicates[0], hpo_dict.get(feature, feature)])
            if gene:
                gene = patient[2]
                if gene != 'unknown':
                    outfile.write(patient_id + '\t' + predicates[2] + '\t' + gene + '\n')
                    triples.append([patient_id, predicates[2], gene])

    return triples
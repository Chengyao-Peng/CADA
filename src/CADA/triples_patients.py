#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def triples_patients(patients):
    predicates = ['has_feature', 'has_disease']
    triples = []
    for patient in patients:
        patient_id = patient[0]
        disease = patient[1]
        features = patient[2].split(',')
        for feature in features:
            triples.append([patient_id, predicates[0], feature])
        triples.append([patient_id, predicates[1], disease])

        return triples
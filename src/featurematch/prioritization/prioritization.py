from scipy import spatial
import numpy as np
from gensim.models import Word2Vec


evaluation_patients = '/home/peng/PycharmProjects/featurematch/data/processed/patients/reform/patients_evaluation.tsv'
training_patients = '/home/peng/PycharmProjects/featurematch/data/processed/patients/reform/patients.tsv'
model = Word2Vec.load('../../../model/with_patients/with_patients.model')

with open(evaluation_patients, 'r') as e_file:
    content = e_file.read().splitlines()
    content = [x.split('\t') for x in content]
    for line in content:
        patient_id = line[0]
        disease = line[1]
        features = line[2].split(',')
        gene = line[3]
        if line[4].split(',') == ['unknown']:
            absent_features = []
        else:
            absent_features = line[4].split(',')

        similar_nodes = model.most_similar(positive=features, negative=absent_features, topn=100)
        similar_nodes_features_filters = []
        for node in similar_nodes:
            if node[0].startswith('Patient'):
                similar_nodes_features_filters.append(node[0])
            elif node[0].startwith('Entrez'):
                similar_nodes_features_filters.append(node[0])
            elif node[0].startwith('MONDO'):
                similar_nodes_features_filters.append(node[0])





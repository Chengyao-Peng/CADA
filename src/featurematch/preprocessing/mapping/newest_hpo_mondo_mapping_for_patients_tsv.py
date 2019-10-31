import pandas as pd
import pronto
#change old hpo id to newest version

old_new_hpo = {}
hpo = pronto.Ontology('../../../../data/raw/hpo/hpo_hierarchical_information/hp.obo')

for term in hpo:
    # get term id as key
    id = term.id
    # get the alt_ids and store them into dict
    if 'alt_id' in term.other:
        alt_ids = (term.other['alt_id'])
        for alt_id in alt_ids:
            old_new_hpo[alt_id] = id


df_mondo_omim = pd.read_csv('../../../../data/raw/mapping/all-mondo-disease-terms.tsv', sep='\t', header=0)[['MONDO', 'OMIM']].dropna()
dict_omim_mondo = dict(zip(df_mondo_omim.OMIM, df_mondo_omim.MONDO))

with open('../../../../data/processed/patients/reform/training/training.tsv', 'r') as infile:
    with open ('../../../../data/processed/patients/reform/training/training_mapping.tsv', 'w') as outfile:
        content = infile.read().splitlines()
        content = [x.split('\t') for x in content]
        for line in content:
            patient_id = line[0]
            disease = line[1]
            if disease in dict_omim_mondo:
                disease = dict_omim_mondo[disease]
            features = line[2].split(',')
            features = ','.join([old_new_hpo.get(feature, feature) for feature in features])
            gene = line[3]
            absent_features = line[4].split(',')
            if absent_features != ['unknown']:
                absent_features = ','.join([old_new_hpo.get(feature, feature) for feature in absent_features])
            else:
                absent_features = 'unknown'
            outfile.write(patient_id + '\t' + disease + '\t' + features + '\t' + gene + '\t' + absent_features + '\n')


with open('../../../../data/processed/patients/reform/evaluation/evaluation_pedia.tsv', 'r') as infile:
    with open ('../../../../data/processed/patients/reform/evaluation/evaluation_pedia_mapped.tsv', 'w') as outfile:
        content = infile.read().splitlines()
        content = [x.split('\t') for x in content]
        for line in content:
            patient_id = line[0]
            disease = line[1]
            if disease in dict_omim_mondo:
                disease = dict_omim_mondo[disease]
            features = line[2].split(',')
            features = ','.join([old_new_hpo.get(feature, feature) for feature in features])
            gene = line[3]
            absent_features = line[4].split(',')
            if absent_features != ['unknown']:
                absent_features = ','.join([old_new_hpo.get(feature, feature) for feature in absent_features])
            else:
                absent_features = 'unknown'
            if disease.startswith('MONDO:'):
                outfile.write(patient_id + '\t' + disease + '\t' + features + '\t' + gene + '\t' + absent_features + '\n')




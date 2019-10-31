import pandas as pd

predicates = ['has_feature', 'has_disease', 'is_feature_of_disease']

with open('../../../../data/raw/f2g/tucases_patient_disease_feature.tsv') as infile:
    with open("../../../../data/processed/f2g/tucases.triples", "w") as outfile:
        content = infile.read().splitlines()
        content = [x.split('\t') for x in content]
        for line in content:
            disease = 'OMIM:' + line[2].strip()
            case = 'Patient:' + line[0].strip()
            features = line[4].split(',')
            if features != ['']:
                for feature in features:
                    outfile.write(case + '\t' + predicates[0] + '\t' + feature + '\n')
                    outfile.write(feature + '\t' + predicates[2] + '\t' + disease + '\n')
                outfile.write(case + '\t' + predicates[1] + '\t' + disease + '\n')

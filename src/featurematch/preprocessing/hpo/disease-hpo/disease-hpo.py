import pandas as pd

predicate = ['is_feature_of_disease']

input = '../../../../../data/raw/hpo/disease-hpo/phenotype_annotation_all_mapped_omim.tab'

output = '../../../../../data/processed/hpo/disease-hpo/diseases_hpos_omim_mapped.triples'
df= pd.read_csv(input, sep ='\t', header=None).applymap(str)
diseases= []

with open(output, 'w') as outfile:
    for row in df.values.tolist():
        disease = row[1].strip()
        feature = row[4].strip()
        outfile.write(feature + '\t' + predicate[0] + '\t' + disease + '\n')
        if disease not in diseases:
            diseases.append(disease)
    print(len(diseases))
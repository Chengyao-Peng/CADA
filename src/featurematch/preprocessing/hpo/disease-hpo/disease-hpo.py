import pandas as pd

predicate = ['is_feature_of_disease']

input = '../../../../../data/raw/hpo/disease-hpo/phenotype_annotation.tab'

output = '../../../../../data/processed/hpo/disease-hpo/diseases_hpos.triples'
df= pd.read_csv(input, sep ='\t', header=None).applymap(str)
df.iloc[249:100121, [1]] = 'OMIM:' + df.iloc[:100121, [1]]
df.iloc[100121:, [1]] = 'ORPHA:' + df.iloc[100121:, [1]]


with open(output, 'w') as outfile:
    for row in df.values.tolist():
        disease = row[1].strip()
        feature = row[4].strip()
        outfile.write(feature + '\t' + predicate[0] + '\t' + disease + '\n')


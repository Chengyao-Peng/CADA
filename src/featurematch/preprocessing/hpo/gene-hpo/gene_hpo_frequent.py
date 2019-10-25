import pandas as pd

predicate = ['is_feature_of_mutation']

input_frequent = '../../../../../data/raw/hpo/gene-hpo/ALL_SOURCES_FREQUENT_FEATURES_genes_to_phenotype.txt'
output_frequent = '../../../../../data/processed/hpo/gene-hpo/genes_hpos_frequent.triples'
df_frequent = pd.read_csv(input_frequent, skiprows=1, sep ='\t').applymap(str)

with open(output_frequent, 'w') as outfile:
    for row in df_frequent.values.tolist():
        gene = "Entrez:" + row[0].strip()
        feature = row[3].strip()
        outfile.write(feature + '\t' + predicate[0] + '\t' + gene + '\n')
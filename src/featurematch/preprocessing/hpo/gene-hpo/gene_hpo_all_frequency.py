import pandas as pd

predicate = ['is_feature_of_mutation']

# all_frequency frequency features
input_all_frequency = '../../../../../data/raw/hpo/gene-hpo/ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt'
output_all_frequency = '../../../../../data/processed/hpo/gene-hpo/genes_hpos_all_frequency.triples'
df_all_frequency = pd.read_csv(input_all_frequency, skiprows=1, sep ='\t').applymap(str)

with open(output_all_frequency, 'w') as outfile:
    for row in df_all_frequency.values.tolist():
        gene = "Entrez:" + row[0].strip()
        feature = row[3].strip()
        outfile.write(feature + '\t' + predicate[0] + '\t' + gene + '\n')





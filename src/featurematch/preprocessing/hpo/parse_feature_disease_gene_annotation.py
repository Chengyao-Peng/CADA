import pandas as pd

predicate = ['is_feature_of_disease', 'is_feature_of_mutation', 'mutation_contributes_to_disease']
# all frequency features
input_all_frequency = '/home/peng/PycharmProjects/featurematch/data/raw/hpo/gene-disease-hpo/ALL_SOURCES_ALL_FREQUENCIES_diseases_to_genes_to_phenotypes.txt'
df_all = pd.read_csv(input_all_frequency, skiprows=1, sep ='\t').applymap(str)

with open('../../../../data/processed/hpo/gene-disease-hpo/feature_disease_gene.triples', 'w') as outfile:
    for row in df_all.values.tolist():
        disease = row[0]
        gene = row[2]
        feature= row[3]
        outfile.write(feature + '\t' + predicate[0] + '\t' + disease + '\n')
        outfile.write(feature + '\t' + predicate[1] + '\t' + gene + '\n')
        outfile.write(gene + '\t' + predicate[2] + '\t' + disease + '\n')



# frequent features
input_frequent = '/home/peng/PycharmProjects/featurematch/data/raw/hpo/gene-disease-hpo/ALL_SOURCES_FREQUENT_FEATURES_diseases_to_genes_to_phenotypes.txt'
df_frequent = pd.read_csv(input_frequent, skiprows=1, sep = '\t').applymap(str)

with open('../../../../data/processed/hpo/gene-disease-hpo/feature_disease_gene_frequent.triples', 'w') as outfile:
    for row in df_all.values.tolist():
        disease = row[0]
        gene = row[2]
        feature= row[3]
        outfile.write(feature + '\t' + predicate[0] + '\t' + disease + '\n')
        outfile.write(feature + '\t' + predicate[1] + '\t' + gene + '\n')
        outfile.write(gene + '\t' + predicate[2] + '\t' + disease + '\n')




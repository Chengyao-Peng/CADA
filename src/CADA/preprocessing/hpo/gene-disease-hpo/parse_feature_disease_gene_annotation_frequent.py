import pandas as pd

predicate = ['is_feature_of_disease', 'is_feature_of_mutation', 'mutation_contributes_to_disease']

# frequent features
#input_frequent = '../../../../data/raw/hpo/gene-disease-hpo/ALL_SOURCES_FREQUENT_FEATURES_diseases_to_genes_to_phenotypes_omim_mapped.tsv'
#df_frequent = pd.read_csv(input_frequent, sep = '\t').applymap(str)

input_frequent = '/home/peng/PycharmProjects/featurematch/data/raw/hpo/phenotype_annotation_all_mapped_omim.tab'
df_frequent = pd.read_csv(input_frequent, sep = '\t').applymap(str)

with open('../../../../data/processed/hpo/gene-disease-hpo/feature_disease_gene_frequent.triples', 'w') as outfile_frequent:
    disease_feature_frequent = {}
    gene_feature_frequent = {}
    disease_gene_frequent = {}

    for row in df_frequent.values.tolist():
        disease = row[0]
        gene = "Entrez:" + row[2]
        feature = row[3]
        if disease in disease_feature_frequent:
            if not feature in disease_feature_frequent[disease]:
                disease_feature_frequent[disease].append(feature)
        else:
            disease_feature_frequent[disease] = []
        if gene in gene_feature_frequent:
            if not feature in gene_feature_frequent[gene]:
                gene_feature_frequent[gene].append(gene)
        else:
            gene_feature_frequent[gene] = []
        if disease in disease_gene_frequent:
            if not gene in disease_gene_frequent[disease]:
                disease_gene_frequent[disease].append(gene)
        else:
            disease_gene_frequent[disease] = []

    for disease in disease_feature_frequent.keys():
        for feature in disease_feature_frequent[disease]:
            outfile_frequent.write(feature + '\t' + predicate[0] + '\t' + disease + '\n')

    for gene in gene_feature_frequent.keys():
        for feature in gene_feature_frequent[gene]:
            outfile_frequent.write(feature + '\t' + predicate[1] + '\t' + gene + '\n')

    for disease in disease_gene_frequent.keys():
        for gene in disease_gene_frequent[disease]:
            outfile_frequent.write(gene + '\t' + predicate[2] + '\t' + disease + '\n')

import pandas as pd

predicate = ['is_feature_of_disease', 'is_feature_of_mutation', 'mutation_contributes_to_disease']

# all_frequency frequency features
input_all_frequency = '../../../../data/raw/hpo/gene-disease-hpo/ALL_SOURCES_ALL_FREQUENCIES_diseases_to_genes_to_phenotypes_omim_mapped.tsv'
df_all_frequency = pd.read_csv(input_all_frequency, sep ='\t').applymap(str)

with open('../../../../data/processed/hpo/gene-disease-hpo/feature_disease_gene.triples', 'w') as outfile:
    disease_feature = {}
    gene_feature = {}
    disease_gene = {}


    for row in df_all_frequency.values.tolist():
        disease = row[0]
        gene = "Entrez:" + row[2]
        feature= row[3]
        if disease in disease_feature:
            if not feature in disease_feature[disease]:
                disease_feature[disease].append(feature)
        else:
            disease_feature[disease] = []
        if gene in gene_feature:
            if not feature in gene_feature[gene]:
                gene_feature[gene].append(gene)
        else:
            gene_feature[gene] = []
        if disease in disease_gene:
            if not gene in disease_gene[disease]:
                disease_gene[disease].append(gene)
        else:
            disease_gene[disease] = []

    for disease in disease_feature.keys():
        for feature in disease_feature[disease]:
            outfile.write(feature + '\t' + predicate[0] + '\t' + disease + '\n')

    for gene in gene_feature.keys():
        for feature in gene_feature[gene]:
            outfile.write(feature + '\t' + predicate[1] + '\t' + gene + '\n')

    for disease in disease_gene.keys():
        for gene in disease_gene[disease]:
            outfile.write(gene + '\t' + predicate[2] + '\t' + disease + '\n')






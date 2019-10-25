import pandas as pd
#change orphnet id to OMIM id if available

df = pd.read_csv('../../../../data/raw/mapping/all-mondo-disease-terms.tsv', sep='\t', header=0)[['Orphanet','OMIM']].dropna()
dict_orpha_omim = dict(zip(df.Orphanet, df.OMIM))


df1 = pd.read_csv('../../../../data/raw/hpo/gene-disease-hpo/ALL_SOURCES_FREQUENT_FEATURES_diseases_to_genes_to_phenotypes.txt', skiprows=1, sep='\t', header=None)
df1[0].replace(dict_orpha_omim, inplace=True)
df1.to_csv('../../../../data/raw/hpo/gene-disease-hpo/ALL_SOURCES_FREQUENT_FEATURES_diseases_to_genes_to_phenotypes_omim_mapped.tsv', index=False, header=False, sep='\t')

df2 = pd.read_csv('../../../../data/raw/hpo/gene-disease-hpo/ALL_SOURCES_ALL_FREQUENCIES_diseases_to_genes_to_phenotypes.txt', skiprows=1, sep='\t', header=None)
df2[0].replace(dict_orpha_omim, inplace=True)
df2.to_csv('../../../../data/raw/hpo/gene-disease-hpo/ALL_SOURCES_ALL_FREQUENCIES_diseases_to_genes_to_phenotypes_omim_mapped.tsv', index=False, header=False, sep='\t')

df3 = pd.read_csv('../../../../data/processed/hpo/disease-gene/diseases_to_genes.triples', sep='\t', header=None)
df3[2].replace(dict_orpha_omim, inplace=True)
df3.to_csv('../../../../data/processed/hpo/disease-gene/diseases_to_genes_omim_mapped.triples', index=False, header=False, sep='\t')


import pandas as pd



input_dir= '../../../../data/raw/hpo/gene-disease-hpo/ALL_SOURCES_ALL_FREQUENCIES_diseases_to_genes_to_phenotypes_omim_mapped.txt'
df= pd.read_csv(input_dir, sep ='\t').applymap(str)
import pandas as pd
import pickle

input_dir = '../../../../data/raw/hpo/gene-hpo/ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt'
output_dir = '../../../../data/processed/ids/gene_id_name.dict'


with open(input_dir) as infile:
    with open(output_dir, 'wb') as outfile:
        df1 = pd.read_csv(input_dir, skiprows=1, header=None, sep='\t').applymap(str)
        dict_id_symbol = dict(zip("Entrez:" + df1.iloc[:,0], df1.iloc[:,1]))
        pickle.dump(dict_id_symbol, outfile)

# df2 = pd.read_csv('../../../../data/raw/hpo/gene-disease-hpo/ALL_SOURCES_FREQUENT_FEATURES_diseases_to_genes_to_phenotypes.txt', skiprows=1, sep='\t', header=None)
# df2[0].replace(dict_orpha_omim, inplace=True)
# df2.to_csv('../../../../data/raw/hpo/gene-disease-hpo/ALL_SOURCES_FREQUENT_FEATURES_diseases_to_genes_to_phenotypes_omim_mapped.tsv', index=False, header=False, sep='\t')







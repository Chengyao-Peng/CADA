import os
import pandas as pd
from CADA.paths import DATA_DIRECTORY
import pickle

annotation = os.path.join(DATA_DIRECTORY, 'raw', 'hpo', 'disease-hpo', 'phenotype_annotation.tab')
out_id_name = os.path.join(DATA_DIRECTORY, 'processed', 'ids', 'omim_id_name.dict')
out_name_id = out_id_name = os.path.join(DATA_DIRECTORY, 'processed', 'ids', 'omim_id_name.dict')

input_dir = '../../../../data/raw/hpo/gene-hpo/ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt'
output_id_name = '../../../../data/processed/ids/gene_id_name.dict'
output_name_id = '../../../../data/processed/ids/gene_name_id.dict'


with open(input_dir) as infile:
    with open(output_id_name, 'wb') as outfile_id_name:
        df1 = pd.read_csv(input_dir, skiprows=1, header=None, sep='\t').applymap(str)
        dict_id_symbol = dict(zip("Entrez:" + df1.iloc[:,0], df1.iloc[:,1]))
        pickle.dump(dict_id_symbol, outfile_id_name)

with open(input_dir) as infile:
    with open(output_name_id, 'wb') as outfile_name_id:
        df1 = pd.read_csv(input_dir, skiprows=1, header=None, sep='\t').applymap(str)
        dict_symbol_id = dict(zip(df1.iloc[:,1], 'Entrez:' + df1.iloc[:,0]))
        pickle.dump(dict_symbol_id, outfile_name_id)


# df2 = pd.read_csv('../../../../data/raw/hpo/gene-disease-hpo/ALL_SOURCES_FREQUENT_FEATURES_diseases_to_genes_to_phenotypes.txt', skiprows=1, sep='\t', header=None)
# df2[0].replace(dict_orpha_omim, inplace=True)
# df2.to_csv('../../../../data/raw/hpo/gene-disease-hpo/ALL_SOURCES_FREQUENT_FEATURES_diseases_to_genes_to_phenotypes_omim_mapped.tsv', index=False, header=False, sep='\t')







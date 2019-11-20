import pandas as pd
import pickle

input_dir = 'diseases_to_genes.txt'
output_dir = '../../../../data/processed/ids/gene_disease.dict'


with open(input_dir) as infile:
    with open(output_dir, 'wb') as outfile:
        df1 = pd.read_csv(input_dir, skiprows=1, header=None, sep='\t').applymap(str)
        dict_id_symbol = dict(zip("Entrez:" + df1.iloc[:,0], df1.iloc[:,1]))
        pickle.dump(dict_id_symbol, outfile)
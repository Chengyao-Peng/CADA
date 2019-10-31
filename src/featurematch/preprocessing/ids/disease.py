import pandas as pd
import pickle

input_dir = '/home/peng/PycharmProjects/featurematch/data/raw/mapping/all-70patients-disease-terms.tsv'
output_dir = '../../../../data/processed/ids/mondo_id_name.dict'

with open(input_dir) as infile:
    with open(output_dir, 'wb') as outfile:
        df1 = pd.read_csv(input_dir, skiprows=1, header=0, sep='\t')
        dict_id_name = dict(zip(df1.iloc[:,0], df1.iloc[:,1]))
        pickle.dump(dict_id_name, outfile)

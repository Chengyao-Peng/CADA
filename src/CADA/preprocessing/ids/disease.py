import os
import pandas as pd
import pickle
from ...paths import DATA_DIRECTORY


annotation = os.path.join(DATA_DIRECTORY, 'raw', 'hpo', 'disease-hpo', 'phenotype_annotation.tab')
cases = os.path.join(DATA_DIRECTORY, 'raw', 'patients', 'disease-hpo', 'phenotype_annotation.tab')

        '/home/peng/PycharmProjects/featurematch/data/raw/patients/f2g/tucases_patient_disease_feature.tsv'
    input_pedia = '/home/peng/PycharmProjects/featurematch/data/raw/patients/supplementary_table_PEDIA/pedia.tsv'
    input_fm_benchmark = '/home/peng/PycharmProjects/featurematch/data/raw/patients/f2g/FM_Benchmark_Gathering_PK.csv'
    output_omim = '../../../../data/processed/final/ids/omim_id_name.dict'

omim_id_name = {}

df = pd.read_csv(input_omim, sep='\t', header=None).applymap(str)
df.iloc[248:100369, [1]] = 'OMIM:' + df.iloc[248:100369, [1]]
for row in df.values.tolist()[248:100369]:
    id = row[1].strip()
    name = row[2].strip()
    omim_id_name[id] = name

df_tucases = pd.read_csv(input_tucases, sep='\t', header=None).applymap(str)
for row in df_tucases.values.tolist():
    id = 'OMIM:' + row[2].strip()
    name = row[1].strip()
    omim_id_name[id] = name

df_pedia = pd.read_csv(input_pedia, sep='\t', header=None).applymap(str)
for row in df_pedia.values.tolist():
    id = row[0].strip()
    name = row[1].strip()
    omim_id_name[id] = name

unclear_diagnosis = ['DIFFERENTIAL_DIAGNOSIS']
with open(input_fm_benchmark, "r") as infile:
    bulk = infile.read().rstrip()
    blocks = bulk.split("\n\n")
    for block in blocks:
        lines = block.split('\n')
        diagnosis = lines[12].split('\t')[1:]
        diseases = lines[10].split('\t')[1:]
        if (diagnosis != unclear_diagnosis) and (len(diseases) == 1) and ('NA' not in diseases):
            id = 'OMIM:' + diseases[0]
            name = lines[11].split('\t')[1]
            omim_id_name[id] = name


for key in omim_id_name:
    print(omim_id_name[key])

pickle.dump(omim_id_name, open(output_omim, 'wb'))









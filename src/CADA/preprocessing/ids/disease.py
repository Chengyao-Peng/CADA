import os
import pandas as pd
from CADA.paths import DATA_DIRECTORY
import pickle

annotation = os.path.join(DATA_DIRECTORY, 'raw', 'hpo', 'disease-hpo', 'phenotype_annotation.tab')
out = os.path.join(DATA_DIRECTORY, 'processed', 'ids', 'omim_id_name.dict')

omim_id_name = {}

df = pd.read_csv(annotation, sep='\t', header=None).applymap(str)
df.iloc[285:102514, [1]] = 'OMIM:' + df.iloc[285:102514, [1]]

omim_id_name = {}
for row in df.values.tolist()[285:102514]:
    id = row[1].strip()
    name = row[2].strip()
    omim_id_name[id] = name

pickle.dump(omim_id_name, open(out, 'wb'))
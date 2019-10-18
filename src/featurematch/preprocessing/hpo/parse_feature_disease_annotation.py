import pandas as pd

predicate = 'is_feature_of_disease'

## input_dir = '../../../data/raw/hpo/phenotype_annotation.tab'
input_dir = '../../../data/raw/hpo/phenotype_annotation_all_mapped_omim.tab'

#df_all = pd.read_csv(input_dir, sep='\t', header=None).loc[:,[2,4]]
df_all = pd.read_csv(input_dir, sep='\t', header=None).loc[:,[1,4]].astype(str)


## with open('../../../data/processed/hpo/disease_hpo_annotation.triples', 'w') as outfile:

with open('../../../data/processed/hpo/disease_hpo_annotation/disease_mapped_hpo_annotation_omim.triples', 'w') as outfile:
    for disease_feature_pairs in df_all.values.tolist():
        disease = disease_feature_pairs[0]
        feature= disease_feature_pairs[1]
        outfile.write(feature + '\t' + predicate + '\t' + disease + '\n')



# df_orphanet = pd.read_csv(input_dir, sep='\t', header=None).loc[:,[2,4]].iloc[100406:176494]
# with open('../../../data/processed/hpo/disease_hpo_annotaion_orphanet.triples', 'w') as outfile_orphanet:
#     for disease_feature_pairs in df_orphanet.values.tolist():
#         disease = disease_feature_pairs[0]
#         feature= disease_feature_pairs[1]
#         outfile_orphanet.write(feature + '\t' + predicate + '\t' + disease + '\n')
import pandas as pd

df1 = pd.read_csv('../../../../data/raw/mapping/all-mondo-disease-terms.tsv', sep='\t', header=0)[['Orphanet','OMIM']].dropna()
dict_orpha_omim = dict(zip(df1.Orphanet, df1.OMIM))
print(dict_orpha_omim)

#add OMIM and Orphanet tag to original ids

df2 = pd.read_csv('../../../../data/raw/hpo/gene-disease-hpo/phenotype_annotation_decipher_mapped.tab', sep='\t', header=None)
df2.loc[248:100369, [1]] = 'OMIM:' + df2.loc[248:100369, [1]].astype(str)
df2.loc[100369:, [1]] = 'ORPHA:' + df2.iloc[100369:, [1]].astype(str)

#change orphnet id to OMIM id if available in dict_orpha_omim
df2[1].replace(dict_orpha_omim, inplace=True)
print(df2)
df2.to_csv('../../../../data/raw/hpo/phenotype_annotation_all_mapped_omim.tab', index=False, header=False, sep='\t')



import pandas as pd

df1 = pd.read_csv('../../../../data/raw/mapping/all-mondo-disease-terms.tsv', sep='\t', header=0)[['class','class_label']].dropna()
df2 = pd.read_csv('../../../../data/raw/mapping/all-mondo-disease-terms.tsv', sep='\t', header=0)[['class', 'OMIM']].dropna()
df3 = pd.read_csv('../../../../data/raw/mapping/all-mondo-disease-terms.tsv', sep='\t', header=0)[['class', 'Orphanet']].dropna()


mondoid_mondoname = dict(zip(df1['class'], df1['class_label']))
mondoid_ominid = dict(zip(df2['OMIM'], df2['class']))
mondoid_orphaid= dict(zip(df3['Orphanet'], df3['class']))

#add OMIM and Orphanet tag to original ids
df4 = pd.read_csv('../../../../data/raw/hpo/phenotype_annotation_decipher_mapped.tab', sep='\t', header=None)
df4.loc[248:100369,[1]] = 'OMIM:' + df4.loc[248:100369,[1]].astype(str)
df4.loc[100369:, [1]] = 'Orphanet:' + df4.loc[100369:, [1]].astype(str)

df4[1].replace(mondoid_ominid, inplace=True)
df4[1].replace(mondoid_orphaid, inplace=True)
df4.to_csv('../../../../data/raw/hpo/phenotype_annotation_all_mapped_mondo.tab', index=False, header=False, sep='\t')
import pandas as pd
import pronto
#change old hpo id to newest version

old_new_hpo = {}
hpo = pronto.Ontology('../../../../data/raw/hpo/hpo_hierarchical_information/hp.obo')

for term in hpo:
    # get term id as key
    id = term.id
    # get the alt_ids and store them into dict
    if 'alt_id' in term.other:
        alt_ids = (term.other['alt_id'])
        for alt_id in alt_ids:
            old_new_hpo[alt_id] = id

df1 = pd.read_csv('../../../../data/processed/f2g/fm.triples', sep='\t', header=None)
df1[0].replace(old_new_hpo, inplace=True)
df1[2].replace(old_new_hpo, inplace=True)
df1.to_csv('../../../../data/processed/f2g/fm.newest_hpo.triples', index=False, header=False, sep='\t')

df2 = pd.read_csv('../../../../data/processed/f2g/tucases.triples', sep='\t', header=None)
df2[0].replace(old_new_hpo, inplace=True)
df2[2].replace(old_new_hpo, inplace=True)
df2.to_csv('../../../../data/processed/f2g/tucases.newest_hpo.triples', index=False, header=False, sep='\t')

df3 = pd.read_csv('../../../../data/processed/supplementary_table_PEDIA/pedia.triples', sep='\t', header=None)
df3[0].replace(old_new_hpo, inplace=True)
df3[2].replace(old_new_hpo, inplace=True)
df3.to_csv('../../../../data/processed/supplementary_table_PEDIA/pedia.newest_hpo.triples', index=False, header=False, sep='\t')


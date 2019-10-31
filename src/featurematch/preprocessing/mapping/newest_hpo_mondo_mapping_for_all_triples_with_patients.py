import pandas as pd
import pronto
#change old hpo id to newest version

indir =  '../../../../data/processed/final/with_patients/with_patients.triples'
mapping_outdir = '../../../../data/processed/final/with_patients/with_patients_mapping.triples'


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

df_mondo_omim = pd.read_csv('../../../../data/raw/mapping/all-mondo-disease-terms.tsv', sep='\t', header=0)[['MONDO', 'OMIM']].dropna()
df_mondo_orpha = pd.read_csv('../../../../data/raw/mapping/all-mondo-disease-terms.tsv', sep='\t', header=0)[['MONDO', 'Orphanet']].dropna()
dict_omim_mondo = dict(zip(df_mondo_omim.OMIM, df_mondo_omim.MONDO))
dict_orpha_mondo = dict(zip(df_mondo_orpha.Orphanet, df_mondo_orpha.MONDO))


df = pd.read_csv(indir, sep='\t', header=None)
df[0].replace(old_new_hpo, inplace=True)
df[0].replace(dict_omim_mondo, inplace=True)
df[0].replace(dict_orpha_mondo, inplace=True)
df[2].replace(old_new_hpo, inplace=True)
df[2].replace(dict_omim_mondo, inplace=True)
df[2].replace(dict_orpha_mondo, inplace=True)
df.to_csv(mapping_outdir, index=False, header=False, sep='\t')



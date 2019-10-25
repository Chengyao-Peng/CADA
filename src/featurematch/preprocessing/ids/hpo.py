import pronto


hpo_dict = {}
hpo = pronto.Ontology('../../../data/raw/hpo/hp.obo')

for term in hpo:
    # get term id as key
    id = term.id
    # get the alt_ids and store them into dict
    if 'alt_id' in term.other:
        alt_ids = (term.other['alt_id'])
        hpo_dict[id] = alt_ids

with open("../../../data/processed/hpo/ids/hpo.", "w") as f:
    for term in hpo_dict.keys():
        if 'parents'in hpo_dict[term]:
            for parent in hpo_dict[term]['parents']:
                f.write(term + '\t' + 'is_a' + '\t' + parent + '\n')

import pronto
import pickle

hpo_dict = {}
hpo = pronto.Ontology('../../../../data/raw/hpo/hpo_hierarchical_information/hp.obo')

for term in hpo.terms():
    id = term.id
    name = term.name
    hpo_dict[id] = name

with open("../../../../data/processed/ids/hpo_id_name.dict", "wb") as outfile:
        pickle.dump(hpo_dict, outfile)

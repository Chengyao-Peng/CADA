import pronto
import os
from .paths import MODEL_DIRECTORY, DATA_DIRECTORY

old_new_hpo = {}
hpo_path = os.path.join(DATA_DIRECTORY, 'raw', 'hpo', 'hpo_hierarchical_information', 'hp.obo')
hpo = pronto.Ontology(hpo_path)

def hpo_old_new():
    for term in hpo:
        # get term id as key
        id = term.id
        # get the alt_ids and store them into dict
        if 'alt_id' in term.other:
            alt_ids = (term.other['alt_id'])
            for alt_id in alt_ids:
                old_new_hpo[alt_id] = id
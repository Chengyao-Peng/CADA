import pronto
import os
import networkx as nx
from .paths import MODEL_DIRECTORY, DATA_DIRECTORY
import collections

hpo_path = os.path.join(DATA_DIRECTORY, 'raw', 'hpo', 'hpo_hierarchical_information', 'hp.obo')
hpo = pronto.Ontology(hpo_path)
old_new_hpo = {}
hpo_dict = collections.defaultdict(dict)


def make_graph():
    edges = []
    edges += edges_hierarchical_hpo()
    edges += edges_patients()
    G = nx.Graph()
    G.add_edges_from(edges)
    nx.write_gpickle(G, '../../data/knowledge_graph/your_graph.gpickle')


def hpo_old_new():
    """This function save HPO terms and their alternative ids."""
    for term in hpo:
        # get term id as key
        id = term.id
        # get the alt_ids and store them into dict
        if 'alt_id' in term.other:
            alt_ids = (term.other['alt_id'])
            for alt_id in alt_ids:
                old_new_hpo[alt_id] = id


def edges_hierarchical_hpo():
    """This function parses hierarchical relationships of HPO."""
    relationships = []
    for term in hpo.terms():
        # get term id
        id = term.id
        # get the parents and store them into dict
        for parent in list(term.superclasses(distance=1))[1:]:
            relationships.append([id, parent.id])
    return relationships


def edges_patients(train_patients):
    """This function parses gene-phenotype relationships of training patients."""
    relationships = []
    for patient in train_patients:
        patient_id = patient[0]
        gene = patient[1]
        features = patient[2].split(',')
        for feature in features:
            relationships.append([gene, hpo_dict.get(feature, feature)])
    return relationships

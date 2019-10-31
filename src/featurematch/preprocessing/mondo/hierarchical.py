import pronto
import collections

hpo_dict = collections.defaultdict(dict)
hpo = pronto.Ontology('/home/peng/PycharmProjects/featurematch/data/raw/mondo/mondo.obo')

for term in hpo:
    # get term id as key
    id = term.id
    # get the name and store it into dict
    name = term.name
    hpo_dict[id]['name'] = name
    # get the synonyms and store them into dict
    if len(term.synonyms) > 0:
        synonyms = []
        for synonym in term.synonyms:
            synonyms.append(synonym.desc)
        hpo_dict[id]['synonyms'] = synonyms
    # get the parents and store them into dict
    if len(term.parents) > 0:
        parents = []
        for parent in term.parents:

            parents.append(parent.id)
        hpo_dict[id]['parents'] = parents

with open("../../../../data/processed/mondo/hierarchical.triples", "w") as f:
    for term in hpo_dict.keys():
        if 'parents'in hpo_dict[term]:
            for parent in hpo_dict[term]['parents']:
                parent = parent.split(' ')[0]
                f.write(term + '\t' + 'is_a' + '\t' + parent + '\n')

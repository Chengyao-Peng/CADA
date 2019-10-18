#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pronto
import collections

hpo_dict = collections.defaultdict(dict)
hpo = pronto.Ontology('../../../data/raw/hpo/hp.obo')
total = 0

for term in hpo:
    total += 1
    # get term id as key
    id = term.id
    # get the name and store it into dict
    name = term.name
    hpo_dict[id]['name'] = name
    if name == 'All':
        print(len(term.rchildren()))
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
    # get the alt_ids and store them into dict
    if 'alt_id' in term.other:
        alt_ids = (term.other['alt_id'])
        hpo_dict[id]['alt_ids'] = alt_ids

print(total)
with open("../../../data/processed/hpo/hierarchical.triples", "w") as f:
    for term in hpo_dict.keys():
        if 'parents'in hpo_dict[term]:
            for parent in hpo_dict[term]['parents']:
                f.write(term + '\t' + 'is_a' + '\t' + parent + '\n')



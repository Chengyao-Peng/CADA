#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pronto
import collections
from featurematch.paths import DATA_DIRECTORY
import itertools

def triples_hierarchical_hpo():
    predicate = 'is_a'
    triples = []
    hpo_dict = collections.defaultdict(dict)
    hpo = pronto.Ontology(os.path.join(DATA_DIRECTORY, 'raw', 'hpo', 'hpo_hierarchical_information', 'hp.obo'))
    for term in hpo.terms():
    # get term id as key
        id = term.id
    # get the name and store it into dict
        name = term.name
        hpo_dict[id]['name'] = name
        # if name == 'All':
        # print(len(term.rchildren()))

    # get the parents and store them into dict
        parents = []
        for parent in itertools.islice(term.superclasses(), 1):
            parents.append(parent.id)
        hpo_dict[id]['parents'] = parents

    for term in hpo_dict.keys():
        if 'parents'in hpo_dict[term]:
            for parent in hpo_dict[term]['parents']:
                triples.append([term, predicate, parent])

    return triples



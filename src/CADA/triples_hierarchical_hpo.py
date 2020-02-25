#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pronto
import collections
from CADA.paths import DATA_DIRECTORY

def triples_hierarchical_hpo():
    predicate = 'is_a'
    triples = []
    hpo_dict = collections.defaultdict(dict)
    hpo = pronto.Ontology(os.path.join(DATA_DIRECTORY, 'raw', 'hpo', 'hpo_hierarchical_information', 'hp.obo'))
    out_file = os.path.join(DATA_DIRECTORY, 'processed', 'hpo', 'hpo_hierarchical_information', 'hpo_hierarchical.triples')

    with open(out_file, 'w') as outfile:
        for term in hpo.terms():
        # get term id as key
            id = term.id
        # get the parents and store them into dict
            parents = []
            for parent in list(term.superclasses(distance=1))[1:]:
                parents.append(parent.id)
            hpo_dict[id]['parents'] = parents

        for term in hpo_dict.keys():
            if 'parents'in hpo_dict[term]:
                for parent in hpo_dict[term]['parents']:
                    outfile.write(term + '\t' + predicate + '\t' + parent + '\n')
                    triples.append([term, predicate, parent])

    return triples



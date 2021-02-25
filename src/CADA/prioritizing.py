import os
import logging
import sys
import pickle
import pandas as pd
import networkx as nx
import pathlib
from progress.bar import Bar
from tqdm import tqdm
from gensim.models import Word2Vec
import numpy as np
from collections import defaultdict
from .paths import DATA_DIRECTORY


logger = logging.getLogger(__name__)

def prioritizing(hpo_terms, model_path, graph_path, out_dir, topn):
    """This function prioritizes genes based on hpo terms."""
    # reload trained model
    model = Word2Vec.load(model_path)
    # parse hpo terms
    features = hpo_terms.split(',')
    # generate a score for each gene in the knowledge graph
    graph = nx.read_gpickle(graph_path)
    recursivedict = lambda: defaultdict(recursivedict)
    genes_scores_dict = recursivedict()
    for node in list(graph.nodes()):
        if node.startswith("Entrez:"):
            gene = node
            gene_scores = []
            for feature in features:
                try:
                    score = model.similarity(feature, gene)
                    gene_scores.append(score)
                except KeyError as e:
                    print('"%s". Please change the term to another one or delete it.'  % str(e))
                    return sys.exit(1)
            genes_scores_dict[gene] = sum(gene_scores)/len(features)
    prioritized_dict = dict(sorted(genes_scores_dict.items(), reverse=True, key=lambda item: item[1]))

    # prioritized_list = sorted(genes_scores_dict, reverse=True, key=genes_scores_dict.__getitem__)
    topn_genes = {k: prioritized_dict[k] for k in list(prioritized_dict)[:topn]}

    # save result to the output directory
    gene_id_name_dict = c
    with open(gene_id_name_dict, 'rb') as handle:
        gene_id_name = pickle.load(handle)

    pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True)
    out_file = os.path.join(out_dir, 'result.txt')
    with open(out_file, 'w') as result_tsv:
        rank = 0
        result_tsv.write("%s\t%s\t%s\t%s\n" % ('rank', 'gene_id', 'gene_name', 'score'))
        for key in topn_genes.keys():
            rank+=1
            result_tsv.write("%s\t%s\t%s\t%s\n" % (rank,key, gene_id_name[key], topn_genes[key]))



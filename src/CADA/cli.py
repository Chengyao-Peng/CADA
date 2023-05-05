# -*- coding: utf-8 -*-

"""Command line interface for CADA."""

import os
import json
import click
import logging
from .paths import MODEL_DIRECTORY, DATA_DIRECTORY
from .prioritizing import prioritizing
from.embeddings import embeddings

__all__ = [
    'main',
]

logger = logging.getLogger(__name__)

@click.command()

@click.option('--hpo_terms', type=click.STRING, required=True, help='a string of comma-separated HPO terms.HPO terms')
@click.option('--weighted', type=click.BOOL, default=False, help='use weighted knowledge graph ')
@click.option('--topn', type=click.IntRange(min=0), default=0, help='the number of output prioritized genes')
@click.option('--out_dir', type=click.Path(), help='an output file')

def main(out_dir, hpo_terms, weighted, topn):
    """This cli runs the CADA NRL."""
    # choose unweighted or weighted model and knowledge graph
    if weighted:
        graph_path = os.path.join(DATA_DIRECTORY, 'processed', 'knowledge_graph', 'weighted', 'train100.gpickle')
        model_path= os.path.join(MODEL_DIRECTORY, 'weighted', 'node2vec.model')

    else:
        model_path= os.path.join(MODEL_DIRECTORY, 'unweighted', 'node2vec.model')
        graph_path = os.path.join(DATA_DIRECTORY, 'processed', 'knowledge_graph', 'unweighted', 'train100.gpickle')

    # prioritizing based on provided hpo terms
    prioritizing(hpo_terms, model_path, graph_path, out_dir, topn)



if __name__ == '__main__':
    main()
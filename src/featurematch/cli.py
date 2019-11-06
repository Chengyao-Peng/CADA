# -*- coding: utf-8 -*-

import json
import click
from typing import TextIO
from .node2vec.embeddings import embeddings

__all__ = [
    'main',
]

@click.command()
@click.argument('config', type=click.File())

def main(config: TextIO):
    config = json.load(config)
    # # Interpret as JSON file
    # config = json.load(config)
    # dimensions = config['dimensions']
    # walk_length = config['walk_length']
    # q = config['q']
    # p = config['p']
    # num_walks = config['num_walks']

    embeddings(**config)

if __name__ == '__main__':
    main()
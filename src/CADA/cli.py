# -*- coding: utf-8 -*-

import json
import click
from typing import TextIO
from CADA.embeddings import embeddings

__all__ = [
    'main',
]

@click.command()
@click.argument('config', type=click.File())

def main(config: TextIO):
    # Interpret as JSON file
    config = json.load(config)
    embeddings(**config)

if __name__ == '__main__':
    main()
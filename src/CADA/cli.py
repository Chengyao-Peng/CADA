# -*- coding: utf-8 -*-

"""Command line interface for CADA."""

import json
import os
import click
import logging
from typing import TextIO
from CADA.paths import MODEL_DIRECTORY
from CADA.embeddings import embeddings

__all__ = [
    'main',
]

logger = logging.getLogger(__name__)

@click.command()
@click.argument('config', type=click.File())

def main(config: TextIO):
    """This cli runs the CADA NRL."""
    config = json.load(config)
    # get model output directory
    output_directory = config['output_directory']
    log_file = os.path.join(MODEL_DIRECTORY, output_directory, 'cada.log')
    logging.basicConfig(filename = log_file, level=logging.INFO)
    # Interpret as JSON file

    embeddings(**config)

if __name__ == '__main__':
    main()
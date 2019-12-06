# -*- coding: utf-8 -*-

"""Command line interface for CADA."""

import json
import os
import click
import logging
from typing import TextIO
from CADA.paths import MODEL_DIRECTORY
from CADA.embeddings import embeddings
from CADA.prioritizing_from_disease import prioritizing_from_disease

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
    with_patients = config['with_patients']
    log_file = os.path.join(MODEL_DIRECTORY, output_directory, 'cada.log')
    logging.basicConfig(filename = log_file, level=logging.INFO)
    # Interpret as JSON file
    embeddings(**config)
    # prioritizing_from_disease(with_patients, output_directory)

if __name__ == '__main__':
    main()
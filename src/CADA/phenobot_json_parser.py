import pandas as pd
from CADA.paths import DATA_DIRECTORY,MODEL_DIRECTORY
import pickle
import os
import logging

def phenobot_json_parser(output_directory: str):
    evaluation_tsv = os.path.join(MODEL_DIRECTORY, output_directory, 'evaluation.tsv')
    phenobot_dir = os.path.join(MODEL_DIRECTORY, output_directory, 'phenobot')
    for filename in os.listdir(phenobot_dir):
        print(filename)
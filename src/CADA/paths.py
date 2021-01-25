import os

HERE = os.path.abspath(os.path.dirname(__file__))
data_DIRECTORY = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, 'data'))
DATA_DIRECTORY = os.environ.get('FEATURE_MATCH_DATA_DIRECTORY', data_DIRECTORY)


model_DIRECTORY = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, 'models'))
MODEL_DIRECTORY = os.environ.get('FEATURE_MATCH_MODEL_DIRECTORY', model_DIRECTORY)
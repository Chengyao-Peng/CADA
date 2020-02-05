from gensim.models import Word2Vec
import pandas as pd
import logging
from CADA.paths import DATA_DIRECTORY,MODEL_DIRECTORY
import pickle
import os
from CADA.disease_gene_mapping import disease_gene

logger = logging.getLogger(__name__)

with open(os.path.join(DATA_DIRECTORY, 'processed', 'ids', 'gene_id_name.dict'), 'rb') as handle:
    gene_id_name = pickle.load(handle)

with open(os.path.join(DATA_DIRECTORY, 'processed', 'ids', 'hpo_id_name.dict'), 'rb') as handle:
    hpo_id_name = pickle.load(handle)

dict_disease_gene = disease_gene()


def prioritizing(with_patients, output_directory):
    in_dir = os.path.join(MODEL_DIRECTORY, output_directory)
    out_tsv = os.path.join(in_dir, 'evaluation.tsv')
    out_xlsx = os.path.join(in_dir, 'evaluation.xlsx')
    # reload trained model
    if with_patients:
        in_dir = os.path.join(MODEL_DIRECTORY, output_directory)
        model = Word2Vec.load(os.path.join(in_dir, 'with_patients.model'))
    else:
        in_dir = os.path.join(MODEL_DIRECTORY, output_directory)
        model = Word2Vec.load(os.path.join(in_dir, 'without_patients.model'))

    train = os.path.join(in_dir, 'patient_training.tsv')
    test = os.path.join(in_dir, 'patient_testing.tsv')
    evaluation_save = list()
    evaluation_vis = list()

    train_pd = pd.read_csv(train, header=None, sep = '\t', names = ['patient_id', 'syndrome','mutation_gene','features', 'submitter', 'from_file'])
    gene_counts = train_pd['mutation_gene'].value_counts().to_dict()

    with open(test, 'r') as t_file:
        content = t_file.read().splitlines()
        content = [x.split('\t') for x in content]
        for line in content:
            patient_id = line[0]
            gene_nodes = []
            gene_id = line[2]
            # count patients with same mutation incorporated into graph
            if gene_id in gene_counts:
                no_patients = gene_counts[gene_id]
            else:
                no_patients = 0
            # find similar nodes by adding vectors of features and calculating cosine distance
            features = line[3].split(',')
            similar_nodes = model.most_similar(positive=features, topn=100000)
            # prioritizing gene
            for node in similar_nodes:
                if node[0].startswith('Entrez'):
                        gene_nodes.append(node[0])
            # get the rank
            rank = gene_nodes.index(gene_id) + 1

            evaluation_save.append([patient_id, gene_id, no_patients,','.join(features), gene_nodes[:30], rank])
            evaluation_vis.append([patient_id, gene_id_name[gene_id], no_patients,
                                   ','.join([hpo_id_name[feature] for feature in features]), ','.join([gene_id_name[gene_id] for gene_id in gene_nodes[:30]]), rank])
        saveframe = pd.DataFrame(evaluation_save, columns = ['patient_id', 'gene_id','no_patients', 'features', 'result', 'rank'])
        saveframe.to_csv(out_tsv, sep='\t', index=None)
        visframe = pd.DataFrame(evaluation_vis, columns=['patient_id', 'gene', 'no_patients', 'features', 'result', 'rank'])
        visframe.to_excel(out_xlsx, index=None)
        logger.info(f'Statistics: {saveframe.describe()}')



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


def prioritizing(output_directory):
    in_dir = os.path.join(MODEL_DIRECTORY, output_directory)
    out_tsv = os.path.join(in_dir, 'evaluation.tsv')
    out_xlsx = os.path.join(in_dir, 'evaluation.xlsx')
    # reload trained model
    in_dir = os.path.join(MODEL_DIRECTORY, output_directory)
    model = Word2Vec.load(os.path.join(in_dir, 'node2vec.model'))

    train = os.path.join(in_dir, 'patient_training.tsv')
    test = os.path.join(in_dir, 'patient_testing.tsv')
    evaluation_save = list()
    evaluation_vis = list()

    gene_counts = {}

    if os.path.exists(train):
        train_pd = pd.read_csv(train, header=None, sep='\t',
                               names=['patient_id', 'omim_id', 'gene_id', 'features', 'submitter',
                                      'from_file', 'no_features'])
        gene_counts = train_pd['gene_id'].value_counts().to_dict()


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
            if gene_id in gene_nodes:
                rank = gene_nodes.index(gene_id) + 1
            else:
                rank = 'NA'

            evaluation_save.append([patient_id, gene_id, no_patients,','.join(features), gene_nodes[:30], rank])
            evaluation_vis.append([patient_id, gene_id_name[gene_id], no_patients,
                                   ','.join([hpo_id_name[feature] for feature in features]), ','.join([gene_id_name[gene_id] for gene_id in gene_nodes[:30]]), rank])
        saveframe = pd.DataFrame(evaluation_save, columns = ['patient_id', 'gene_id','no_patients', 'features', 'result', 'rank'])
        saveframe.to_csv(out_tsv, sep='\t', index=None)
        visframe = pd.DataFrame(evaluation_vis, columns=['patient_id', 'gene', 'no_patients', 'features', 'result', 'rank'])
        visframe.to_excel(out_xlsx, index=None)
        ranks = saveframe['rank'].tolist()
        count1 = count5 = count10 = count50 = count100 = count1000 = 0
        counts = len(ranks)
        for rank in ranks:
            if isinstance(rank, int):
                if rank == 1:
                    count1 += 1
                if rank <= 5:
                    count5 += 1
                if rank <= 10:
                    count10 += 1
                if rank <= 50:
                    count50 += 1
                if rank <= 100:
                    count100 += 1
                if rank <= 1000:
                    count1000 += 1
        top1 = round(count1/counts, 2)
        top5 = round(count5/counts, 2)
        top10 = round(count10/counts, 2)
        top50 = round(count50/counts, 2)
        top100 = round(count100/counts, 2)
        top1000 = round(count1000/counts, 2)

        logger.info(f'top1: {top1}')
        logger.info(f'top5: {top5}')
        logger.info(f'top10: {top10}')
        logger.info(f'top50: {top50}')
        logger.info(f'top100: {top100}')
        logger.info(f'top1000: {top1000}')




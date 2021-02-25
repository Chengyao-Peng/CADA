import os
from node2vec import Node2Vec
import networkx as nx
from .paths import MODEL_DIRECTORY



def embeddings(
        *,
        train_graph='../../data/processed/knowledge_graph/unweighted/train100.gpickle',
        dimensions=300,
        walk_length=60,
        p=1.7987535798694703,
        q=3.875406134463754,
        num_walks=10,
        window=4,
        output_directory='../../models/unweighted',
        ):
    '''
    :param train_graph: the path of the gene-phenotype knowledge graph
    :param dimensions: The number of dimensions of feature vectors. Default is 100.
    :param walk_length: The number of nodes in each random walk. Default is 80
    :param p: It controls the probability for a walk to visit immediately back to the previous node. Default is 1.
    :param q: It controls the probability for a walk to visit previously unexplored neighborhoods in the graph. Default is 1.
    :param num_walks: The number of random walks to be generated from each node in the graph. Default is 10
    :param window: The limit on the number of words in each context. Default is 5.
    :param output_directory: the path of the output embeddings and model
    '''

    embedding_outdir = os.path.join(MODEL_DIRECTORY, output_directory, 'node2vec.embeddings')
    model_outdir = os.path.join(output_directory, output_directory, 'node2vec.model')

    g = nx.read_gpickle(train_graph)
    node2vec = Node2Vec(g, dimensions=dimensions, walk_length=walk_length, num_walks=num_walks, workers=1, p=p, q=q)
    model = node2vec.fit(window=window, min_count=1, batch_words=4)
    model.wv.save_word2vec_format(embedding_outdir)
    model.save(model_outdir)
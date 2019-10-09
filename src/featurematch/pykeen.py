import pykeen

output_directory = "/home/peng/PycharmProjects/feature_match/result"

config = dict(
    training_set_path           = '/home/peng/PycharmProjects/feature_match/result/triples.tsv',
    execution_mode              = 'Training_mode',
    kg_embedding_model_name     = 'TransE',
    embedding_dim               = 50,
    normalization_of_entities   = 2,  # corresponds to L2
    scoring_function            = 1,  # corresponds to L1
    margin_loss                 = 1,
    learning_rate               = 0.01,
    batch_size                  = 32,
    num_epochs                  = 1000,
    test_set_ratio              = 0.1,
    filter_negative_triples     = True,
    random_seed                 = 2,
    preferred_device            = 'gpu',
)

results = pykeen.run(
    config = config,
    output_directory = output_directory,
)


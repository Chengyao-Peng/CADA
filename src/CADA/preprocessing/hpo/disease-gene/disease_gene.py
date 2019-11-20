import os
from featurematch.paths import DATA_DIRECTORY


def disease_gene():
    predicate = 'mutation_contributes_to_disease'
    input_file = os.path.join(DATA_DIRECTORY, 'raw', 'hpo', 'disease-gene', 'diseases_to_genes.txt')
    out_file = os.path.join(DATA_DIRECTORY, 'processed', 'hpo', 'disease-gene', 'diseases_to_genes.triples')
    diseases = list()
    with open(input_file) as infile:
        with open(out_file, 'w') as outfile:
            content = infile.read().splitlines()
            content = [x.split('\t') for x in content]
            for line in content:
                if len(line) == 3:
                    gene = 'Entrez:' + line[1].strip()
                    disease = line[0].strip()
                    if disease not in diseases:
                        diseases.append(disease)
                    outfile.write(gene + '\t' + predicate + '\t' + disease + '\n')



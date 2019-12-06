import os
from CADA.paths import DATA_DIRECTORY


def triples_disease_gene():
    predicate = 'contributes_to'
    triples = []
    in_file = os.path.join(DATA_DIRECTORY, 'raw', 'hpo', 'disease-gene', 'diseases_to_genes.txt')
    out_file = os.path.join(DATA_DIRECTORY, 'processed', 'hpo', 'disease-gene', 'diseases_to_genes.triples')
    with open(in_file) as infile:
        with open(out_file, 'w') as outfile:
            content = infile.read().splitlines()
            content = [x.split('\t') for x in content]
            for line in content:
                if len(line) == 3:
                    disease = line[0].strip()
                    if disease.startswith('OMIM:'):
                        gene = 'Entrez:' + line[1].strip()
                        outfile.write(gene + '\t' + predicate + '\t' + disease + '\n')
                        triples.append([gene, predicate, disease])
    return triples




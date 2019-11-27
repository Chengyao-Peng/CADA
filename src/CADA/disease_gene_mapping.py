import pandas as pd
import pickle
import os
from CADA.paths import DATA_DIRECTORY

input_file = os.path.join(DATA_DIRECTORY, 'raw', 'hpo', 'disease-gene', 'diseases_to_genes.txt')

def disease_gene():
    disease_genes = {}
    with open(input_file, 'r') as infile:
        content = infile.read().splitlines()
        lines = [x.split('\t') for x in content][1:]
        for line in lines:
            if len(line) == 3 and line[0].startswith('OMIM'):
                disease = line[0]
                gene = 'Entrez:' + line[1]
                if disease in disease_genes:
                    disease_genes[disease].append(gene)
                else:
                    disease_genes[disease] = []
                    disease_genes[disease].append(gene)
    return disease_genes

def gene_disease():
    gene_diseases = {}
    with open(input_file, 'r') as infile:
        content = infile.read().splitlines()
        lines = [x.split('\t') for x in content][1:]
        for line in lines:
            if len(line) == 3 and line[0].startswith('OMIM'):
                disease = line[0]
                gene = 'Entrez:' + line[1]
                if gene in gene_diseases:
                    gene_diseases[gene].append(disease)
                else:
                    gene_diseases[gene] = []
                    gene_diseases[gene].append(disease)

    return gene_diseases



predicate = ['mutation_contributes_to_disease']

input_dir = '../../../../../data/raw/hpo/disease-gene/diseases_to_genes.txt'
output_dir = '../../../../../data/processed/hpo/disease-gene/diseases_to_genes.triples'
diseases = []
with open(input_dir) as infile:
    with open(output_dir, 'w') as outfile:
        content = infile.read().splitlines()
        content = [x.split('\t') for x in content]
        for line in content:
            if len(line) == 3:
                gene = 'Entrez:' + line[1].strip()
                disease = line[0].strip()
                if disease not in diseases:
                    diseases.append(disease)
                outfile.write(gene + '\t' + 'mutation_contributes_to_disease' + '\t' + disease + '\n')



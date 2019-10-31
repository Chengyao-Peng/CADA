import pandas as pd

predicates = ['has_mutation', 'has_feature', 'is_feature_of_mutation', 'has_disease', 'is_feature_of_disease']

input = ['/home/peng/PycharmProjects/featurematch/data/processed/patients/reform/f2g/f2g_benchmark.tsv','/home/peng/PycharmProjects/featurematch/data/processed/patients/reform/f2g/f2g_tucases.tsv','/home/peng/PycharmProjects/featurematch/data/processed/patients/reform/supplementary_table_PEDIA/training_pedia.tsv']

outdir = '/home/peng/PycharmProjects/featurematch/data/processed/patients/triple/training.triples'

df1 = pd.read_csv(input[0], sep='\t', header=None)
df2 = pd.read_csv(input[1], sep='\t', header=None)
df3 = pd.read_csv(input[2], sep='\t', header=None)
df = pd.concat([df1, df2, df3])

with open(outdir, 'w') as outfile:
    for line in df.values.tolist():
        patient = line[0]
        disease = line[1]
        features = line[2].split(',')
        gene = line[3]
        for feature in features:
            outfile.write(patient + '\t' + predicates[1] + '\t' + feature + '\n')
            if not gene == 'unknown':
                outfile.write(feature + '\t' + predicates[2] + '\t' + gene + '\n')
            outfile.write(feature + '\t' + predicates[4] + '\t' + disease + '\n')
        if not gene == 'unknown':
            outfile.write(patient + '\t' + predicates[0] + '\t' + gene + '\n')
            outfile.write(patient + '\t' + predicates[3] + '\t' + disease + '\n')






predicates = ['has_mutation', 'has_feature', 'is_feature_of_mutation', 'has_disease', 'is_feature_of_disease']
unclear_diagnosis = ['DIFFERENTIAL_DIAGNOSIS']

#comorbidiy
with open('../../../../data/raw/f2g/FM_Benchmark_Gathering_PK.csv', "r") as infile:
    with open('../../../../data/processed/f2g/fm.triples', 'w') as outfile:
        bulk = infile.read().rstrip()
        blocks = bulk.split("\n\n")
        for block in blocks:
            lines = block.split('\n')
            diagnosis = lines[12].split('\t')[1:]
            diseases = lines[10].split('\t')[1:]

            if (diagnosis != unclear_diagnosis) and (len(diseases) == 1) and ('NA' not in diseases):
                case = 'Patient:' + lines[0].split('\t')[1].strip()
                features = lines[3].split('\t')[1:]
                disease = 'OMIM:' + diseases[0]
                outfile.write(case + '\t' + predicates[3] + '\t' + disease + '\n')
                for feature in features:
                    outfile.write(case + '\t' + predicates[1] + '\t' + feature + '\n')
                    outfile.write(feature + '\t' + predicates[4] + '\t' + disease + '\n')

                genes = lines[8].split('\t')[1:]
                if genes != ['']:
                    gene = 'Entrez:' + genes[0]
                    outfile.write(case + '\t' + predicates[0] + '\t' + gene + '\n')
                    for feature in features:
                        outfile.write(feature + '\t' + predicates[2] + '\t' + gene + '\n')







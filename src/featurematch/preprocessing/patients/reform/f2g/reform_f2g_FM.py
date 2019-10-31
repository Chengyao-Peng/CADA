unclear_diagnosis = ['DIFFERENTIAL_DIAGNOSIS']

#comorbidiy
with open('../../../../../../data/raw/patients/f2g/FM_Benchmark_Gathering_PK.csv', "r") as infile:
    with open('../../../../../../data/processed/patients/reform/f2g/f2g_benchmark.tsv', 'w') as outfile:
        bulk = infile.read().rstrip()
        blocks = bulk.split("\n\n")
        for block in blocks:
            lines = block.split('\n')
            diagnosis = lines[12].split('\t')[1:]
            diseases = lines[10].split('\t')[1:]

            if (diagnosis != unclear_diagnosis) and (len(diseases) == 1) and ('NA' not in diseases):
                case = 'Patient:' + lines[0].split('\t')[1].strip()
                features = lines[3].split('\t')[1:]
                absent_features = lines[5].split('\t')[1:]
                print(absent_features)
                disease = 'OMIM:' + diseases[0]
                genes = lines[8].split('\t')[1:]
                outfile.write(case +  '\t' + disease)
                outfile.write('\t' + ','.join(features))

                if genes != ['']:
                    gene = 'Entrez:' + genes[0]
                    outfile.write('\t' + gene )
                else:
                    outfile.write('\t' + 'unknown')

                if absent_features != ['']:
                    outfile.write('\t' + ','.join(absent_features) + '\n')
                else:
                    outfile.write('\t' + 'unknown' + '\n')



import pandas as pd

with open("../../../../../../data/raw/patients/supplementary_table_PEDIA/pedia.tsv") as infile:
    with open("../../../../../../data/processed/patients/reform/supplementary_table_PEDIA/training_pedia.tsv", "w") as training:
        with open("../../../../../../data/processed/patients/reform/supplementary_table_PEDIA/evaluation_pedia.tsv", "w") as evaluation:
            content = infile.read().splitlines()
            content = [x.split('\t') for x in content]
            patients = []
            for line in content:
                disease = line[0].strip()
                case = 'Patient:' + line[4].strip()
                gene = 'Entrez:' + line[5].strip()
                features = line[14].split(', ')
                features_line = ','.join(features)
                absent_features = line[15].split(', ')
                if absent_features != ['']:
                    absent_features_line = ','.join(absent_features)
                    patients.append([case, disease, features_line , gene, absent_features_line])
                else:
                    patients.append([case, disease, features_line , gene, 'unknown'])
            df = pd.DataFrame(patients, columns=['case_id', 'disease', 'features', 'gene', 'absent_features'])


            trainingframe = pd.DataFrame()
            traininglist = list()

            for i,j in df.groupby("disease"):
                if len(j)==1:
                    traininglist.append(j)
                    df = df.drop(j.index)
                elif len(j)==2:
                    trainingsample = j.sample(n=1)
                    traininglist.append(trainingsample)
                    df = df.drop(trainingsample.index)
                else:
                    trainingsample = j.sample(n=2*len(j)//3)
                    traininglist.append(trainingsample)
                    df = df.drop(trainingsample.index)

            trainingframe = pd.concat(traininglist)
            evaluationframe = df
            trainingframe.to_csv(training, sep='\t', header=None, index=False)
            evaluationframe.to_csv(evaluation, sep='\t', header=None, index=False)
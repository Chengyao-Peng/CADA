import os
import pandas as pd
import numpy as np
from featurematch.paths import DATA_DIRECTORY

__all__ = [
    'reform_f2g_fm',
    'reform_f2g_tucases',
    'reform_pedia'
]

def reform_f2g_fm(hpo_dict):
    unclear_diagnosis = ['DIFFERENTIAL_DIAGNOSIS']
    input_file = os.path.join(DATA_DIRECTORY, 'raw', 'patients', 'f2g', 'FM_Benchmark_Gathering_PK.csv')
    patients = []
    with open(input_file, "r") as infile:
        bulk = infile.read().rstrip()
        blocks = bulk.split("\n\n")
        for block in blocks:
            lines = block.split('\n')
            diagnosis = lines[12].split('\t')[1:]
            diseases = lines[10].split('\t')[1:]
            # filtering out patients only with differential diagnosis and patients with comorbidity
            if (diagnosis != unclear_diagnosis) and (len(diseases) == 1) and ('NA' not in diseases):
                case = 'Patient:' + lines[0].split('\t')[1].strip()
                features = lines[3].split('\t')[1:]
                features = [hpo_dict.get(feature, feature) for feature in features]
                features_line = ','.join(features)
                disease = 'OMIM:' + diseases[0]
                genes = lines[8].split('\t')[1:]
                if genes != ['']:
                    gene = 'Entrez:' + genes[0]
                else:
                    gene = 'unknown'
                patients.append([case, disease, features_line, gene])

    return patients
                # # if absent_features != ['']:
                # #     outfile.write('\t' + ','.join(absent_features) + '\n')
                # # else:
                # # outfile.write('\t' + 'unknown' + '\n')


def reform_f2g_tucases(hpo_dict):
    input_diseases = os.path.join(DATA_DIRECTORY, 'raw', 'patients', 'f2g', 'TUcases_disease.xlsx')
    input_features = os.path.join(DATA_DIRECTORY, 'raw', 'patients', 'f2g', 'TUcases_feature.xlsx')
    known_patients = os.path.join(DATA_DIRECTORY, 'raw', 'patients', 'f2g', 'tucases_unknown.tsv')
    unknown_patients = os.path.join(DATA_DIRECTORY, 'raw', 'patients', 'f2g', 'tucases_known.tsv')

    df_diseases = pd.read_excel(input_diseases, header=0, converters={'case_id': str, 'omim_id': str})[
        ['case_id', 'syndrome_name', 'omim_id', 'diagnosis']]

    # remove differential diagnosis
    df_diseases = df_diseases.loc[df_diseases['diagnosis'] != 'DIFFERENTIAL_DIAGNOSIS']
    # remove duplicated
    df_diseases = df_diseases.drop_duplicates()
    # remove patients with multiple diseases
    df_diseases = df_diseases.groupby('case_id').filter(lambda x: len(x) == 1)
    # fillna of omim id
    df_diseases[['omim_id']] = df_diseases[['omim_id']].replace('0', np.nan)
    df_diseases[['omim_id']] = df_diseases[['omim_id']].fillna('unknown')
    # seperate patients with known and unknown omim disease
    df_unknownOmim = df_diseases.loc[df_diseases['omim_id'] == 'unknown']
    df_knownOmim = df_diseases.loc[df_diseases['omim_id'] != 'unknown']

    df_features = pd.read_excel(input_features, header=0, converters={'case_id': str, 'is_present': str})[
        ['case_id', 'hpo_id', 'is_present']]
    df_features = df_features.loc[df_features['is_present'] == '1'].drop(columns=['is_present'])
    # update hpo ids to newest version
    df_features['hpo_id'].update(pd.Series(hpo_dict))
    # join features of a patient into a new column
    df_features = df_features.groupby(by="case_id", as_index=False).agg(','.join)

    # merge disease and feature information of patients of unknown omim disease
    df_combined_unknownOmim = pd.merge(df_unknownOmim, df_features, how='left', on='case_id').dropna()
    df_combined_unknownOmim['Gene'] = 'unknown'
    df_combined_unknownOmim.to_csv(known_patients, sep='\t', index=False)

    # merge disease and feature information of patients of known omim disease!!!!!!!!!!!!!!
    df_combined_knownOmim = pd.merge(df_knownOmim, df_features, how='left', on='case_id').dropna()
    df_combined_knownOmim['Gene'] = 'unknown'
    df_combined_knownOmim.to_csv(unknown_patients, sep='\t', index=False, header=False)

    df_combined_knownOmim.iloc[:, 0] = 'Patient:' + df_combined_knownOmim.iloc[:, 0]
    df_combined_knownOmim.iloc[:, 2] = 'OMIM:' + df_combined_knownOmim.iloc[:, 2]
    patients = df_combined_knownOmim.iloc[:, [0, 2, 4, 5]].values.tolist()
    return patients


def reform_pedia(hpo_dict):
    input_file = os.path.join(DATA_DIRECTORY, 'raw', 'patients', 'supplementary_table_PEDIA', 'pedia.tsv')
    patients = []
    with open(input_file, 'r') as infile:
        content = infile.read().splitlines()
        content = [x.split('\t') for x in content]
        for line in content:
            disease = line[0].strip()
            case = 'Patient:' + line[4].strip()
            gene = 'Entrez:' + line[5].strip()
            features = line[14].split(', ')
            features_line = ','.join([hpo_dict.get(feature, feature) for feature in features])
            absent_features = line[15].split(', ')
            patients.append([case, disease, features_line, gene])

    return patients


import os
import json
import pandas as pd
import numpy as np
from CADA.paths import DATA_DIRECTORY
import pickle

__all__ = [
    'reform_f2g_fm',
    'reform_f2g_tucases',
    'reform_pedia',
    'reform_f2g_json',
    'reform_genetikum'
]

def reform_f2g_fm(hpo_dict):
    from_file = 'fm_benchmarking'
    unclear_diagnosis = ['DIFFERENTIAL_DIAGNOSIS']
    input_file = os.path.join(DATA_DIRECTORY, 'raw', 'patients', 'f2g', 'FM_Benchmark_Gathering_PK.csv')
    patients = []

    with open(input_file, "r") as infile:
        bulk = infile.read().rstrip()
        blocks = bulk.split("\n\n")
        for block in blocks:
            lines = block.split('\n')
            submitter = lines[1].split('\t')[1:][0]
            diagnosis = lines[12].split('\t')[1:]
            diseases = lines[10].split('\t')[1:]
            # filtering out patients only with differential diagnosis and patients with comorbidity
            if (diagnosis != unclear_diagnosis) and (len(diseases) == 1) and ('NA' not in diseases):
                case = 'Patient:' + lines[0].split('\t')[1].strip()
                features = lines[3].split('\t')[1:]
                features = [hpo_dict.get(feature, feature) for feature in features]
                features_line = ','.join(features)
                disease = diseases[0]
                if disease.startswith('PS'):
                    disease = 'OMIM:' + disease[2:] # get rid of 'ps'
                else:
                    disease = 'OMIM:' + disease
                # get gene
                genes = lines[8].split('\t')[1:]
                if genes != ['']:
                    gene = 'Entrez:' + genes[0]
                else:
                    gene = 'unknown'
                patients.append([case, disease, gene, features_line, submitter, from_file])

    return patients



def reform_f2g_tucases(hpo_dict):
    from_file = 'tucases'
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
    df_combined_unknownOmim.to_csv(known_patients, sep='\t', index=False)

    # merge disease and feature information of patients of known omim disease!!!!!!!!!!!!!!
    df_combined_knownOmim = pd.merge(df_knownOmim, df_features, how='left', on='case_id').dropna()

    df_combined_knownOmim.to_csv(unknown_patients, sep='\t', index=False, header=False)

    df_combined_knownOmim.iloc[:, 0] = 'Patient:' + df_combined_knownOmim.iloc[:, 0]
    df_combined_knownOmim.iloc[:, 2] = 'OMIM:' + df_combined_knownOmim.iloc[:, 2]
    df_combined_knownOmim['Gene'] = 'unknown'
    df_combined_knownOmim['Submitter'] = 'f2g2years'
    df_combined_knownOmim['From'] = from_file

    patients = df_combined_knownOmim.iloc[:, [0, 2, 5, 4, 6, 7]].values.tolist()
    return patients


def reform_pedia(hpo_dict):
    from_file = 'pedia'
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
            submitter = line[16]
            patients.append([case, disease, gene, features_line, submitter, from_file])

    return patients


def reform_f2g_json(hpo_dict):
    from_file = 'json_from_f2g'
    input_dir = os.path.join(DATA_DIRECTORY, 'raw', 'patients', 'aleksandra')
    patients = []

    for json_file in os.listdir(input_dir):
        json_file = os.path.join(DATA_DIRECTORY, 'raw', 'patients', 'aleksandra', json_file)
        with open(json_file) as f:
            patient = json.load(f)
            case = 'Patient:' + patient['f2g_case_id']
            # get disease
            diseases = patient['case_data']['selected_syndromes']
            if len(diseases) == 1:
                omim_id = diseases[0]['syndrome']['omim_id']
                if not omim_id:
                    omim_ps_id = diseases[0]['syndrome']['omim_ps_id']
                    disease = 'OMIM:' + omim_ps_id[2:] # get rid of 'ps'
                else:
                    disease = 'OMIM:' + omim_id
            elif len(diseases) > 1:
                disease = 'cormorbidity'
            else:
                disease = 'unknown'
            #get gene
            genes = patient['case_data']['selected_genes']
            if len(genes) == 1:
                gene = 'Entrez:' + genes[0]['gene_entrez_id']
            else:
                gene = 'unknown'
            # get features
            features = patient['case_data']['selected_features']
            features_list = []
            for feature in features:
                if feature['is_present'] == '1':
                    features_list.append(feature['feature']['hpo_full_id'])
            features_line = ','.join([hpo_dict.get(feature, feature) for feature in features_list])
            # get submitter
            submitter = patient['shared_by_display_name']
            patients.append([case, disease, gene, features_line, submitter, from_file])
    return patients


def reform_genetikum(hpo_dict):
    patients = []
    from_file = 'genetikum'
    submitter = 'genetikum'

    input_fm = os.path.join(DATA_DIRECTORY, 'raw', 'patients', 'genetikum_patients',
                            'FeatureMatch_Liste_genetikum.xlsx')
    df_fm = pd.read_excel(input_fm, header=0, converters={'Case_id': str})
    for patient in df_fm.values.tolist():
        case = 'Patient:' + patient[0]
        disease = 'unknown'
        features_line = patient[1]
        features_list = features_line.split(',')
        features_line = ','.join([hpo_dict.get(feature, feature) for feature in features_list])
        gene = patient[2]
        gene_mappings = os.path.join(DATA_DIRECTORY, 'processed', 'ids', 'gene_name_id.dict')
        gene_dict = pickle.load(open(gene_mappings, 'rb'))
        patients.append([case, disease, gene_dict[gene], features_line, submitter, from_file])

    input_unsa = os.path.join(DATA_DIRECTORY, 'raw', 'patients', 'genetikum_patients', 'genetikum_patients_known.xlsx')
    df_ubsa = pd.read_excel(input_unsa, header=None)
    for patient in df_ubsa.values.tolist():
        case = 'Patient:' + str(patient[0])
        disease = 'unknown'
        features_line = patient[1]
        features_list = features_line.split(',')
        features_line = ','.join([hpo_dict.get(feature, feature) for feature in features_list])
        gene = patient[3]
        patients.append([case, disease, gene_dict[gene], features_line, submitter, from_file])

    return patients






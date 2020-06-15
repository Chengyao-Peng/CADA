import os
import pandas as pd
import pickle
import csv
from sklearn.model_selection import train_test_split
from CADA.paths import DATA_DIRECTORY
from CADA.reform import *
from CADA.disease_gene_mapping import disease_gene, gene_disease

with open(os.path.join(DATA_DIRECTORY, 'processed', 'ids', 'hpo_old_new.dict'), 'rb') as handle:
    hpo_dict = pickle.load(handle)
with open(os.path.join(DATA_DIRECTORY, 'processed', 'ids', 'gene_id_name.dict'), 'rb') as handle:
    gene_id_name = pickle.load(handle)
with open(os.path.join(DATA_DIRECTORY, 'processed', 'ids', 'omim_id_name.dict'), 'rb') as handle:
    omim_id_name = pickle.load(handle)
with open(os.path.join(DATA_DIRECTORY, 'processed', 'ids', 'hpo_id_name.dict'), 'rb') as handle:
    hpo_id_name = pickle.load(handle)
with open(os.path.join(DATA_DIRECTORY, 'processed', 'hpo', 'gene-hpo', 'genes.list'), 'rb') as handle:
    gene_list = pickle.load(handle)


def split(train_size, output_directory):
    out_all_csv = os.path.join(output_directory, 'patient.tsv')
    out_all_excel = os.path.join(output_directory, 'patient.xlsx')
    out_train = os.path.join(output_directory, 'patient_training.tsv')
    out_test = os.path.join(output_directory, 'patient_testing.tsv')
    # get all patients and update their hpo id to the newest version
    patients = []
    patients += reform_pedia()
    patients += reform_f2g_fm()
    patients += reform_f2g_tucases()
    patients += reform_f2g_json()
    patients += reform_genetikum()
    patients += reform_pki()
    patients += reform_tubingen()
    patients += reform_clinvar()
    patients += reform_berlin()

    patients = filter_identical_patients(patients)
    patients = final_preprocessing(patients)
    patients = filter_only_disease(patients)
    patients = filter_gene_not_included(patients)
    patients = update_hpo(patients)
    patients = remove_BRCA(patients)
    save_patient(out_all_csv, out_all_excel, patients)

    if train_size == 0:
        train = []
        test = patients
        with open(out_test, "w", newline="") as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(test)
    elif train_size == 1:
        train = patients
        test = []
        with open(out_train, "w", newline="") as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(train)
    else:
        train, test = train_test_split(patients, train_size=train_size)
        train.to_csv(out_train, index=False, header=None, sep='\t')
        test.to_csv(out_test, index=False, header=None, sep='\t')
        train = train.values.tolist()
        test = test.values.tolist()

    return train, test

def remove_BRCA(patients):
    patients_return = []
    for patient in patients:
        gene = patient[2]
        if gene == 'Entrez:672' or gene == 'Entrez:675':
            pass
        else:
            patients_return.append(patient)
    return patients_return


def final_preprocessing(patients):
    ''' filter out identical hpo terms
     add gene or disease information if a 1-to-1 relationship for those patients with only gene or disease information
     add a column of feature numbers'''
    for patient in patients:
        disease = patient[1]
        gene = patient[2]
        feature_list = patient[3].split(',')
        filtered_feature_list = list(set(feature_list))
        num_features = len(filtered_feature_list)
        filtered_feature_line = ','.join(filtered_feature_list)
        patient[3] = filtered_feature_line
        patient.append(num_features)
        if disease == 'unknown':
            gene_disease_map = gene_disease()
            if gene in gene_disease_map:
                if len(gene_disease_map[gene]) == 1:
                    patient[1] = gene_disease_map[gene][0]
                else:
                    pass
        if gene == 'unknown':
            disease_gene_map = disease_gene()
            if disease in disease_gene_map:
                if len(disease_gene_map[disease]) == 1:
                    patient[2] = disease_gene_map[disease][0]
                else:
                    pass
    return patients


def filter_identical_patients(patients):
    filtered_patients = {}
    list_filtered_patients = []
    for patient in patients:
        patient_id = patient[0]
        if patient_id in filtered_patients:
            pass
        else:
            filtered_patients[patient_id] = patient[1:]
    for key, value in filtered_patients.items():
        item = [key] + value
        list_filtered_patients.append(item)
    return list_filtered_patients

def update_hpo(patients):
    for patient in patients:
        features = patient[3].split(',')
        updated_features = [hpo_dict.get(feature, feature) for feature in features]
        features_line = ','.join(updated_features)
        patient[3] = features_line
    return patients


def save_patient(out_all_csv, out_all_excel, patients):
    # generate an csv file of all patient
    patients = pd.DataFrame(patients, columns=['patient_id', 'omim_id', 'gene_id', 'features', 'submitter', 'from_file',
                                               'num_features'])
    patients = patients.sort_values(patients.columns[2])  # sort patients by gene information
    patients.to_csv(out_all_csv, index=False, sep='\t')
    # generate an visualizable xlsx file of all patient
    excel_patients_list = patients.values.tolist()
    for patient in excel_patients_list:
        omim_id = patient[1]
        if not omim_id == 'unknown' and omim_id in omim_id_name:
            patient[1] = omim_id_name[omim_id]
        gene_id = patient[2]
        if not gene_id == 'unknown' and gene_id in gene_id_name:
            patient[2] = gene_id_name[gene_id]
        features_list = patient[3].split(',')
        features_line = ','.join([hpo_id_name.get(feature, feature) for feature in features_list])
        patient[3] = features_line
    excel_patients_pd = pd.DataFrame(excel_patients_list,
                                     columns=['patient_id', 'omim', 'gene', 'features', 'submitter', 'from_file',
                                              'num_features'])
    excel_patients_pd = excel_patients_pd.sort_values(excel_patients_pd.columns[2])
    excel_patients_pd.to_excel(out_all_excel, index=None)


def filter_only_disease(patients):
    filtered_patients = []
    for patient in patients:
        if patient[2] != 'unknown':
            filtered_patients.append(patient)
    return filtered_patients


def filter_gene_not_included(patients):
    filtered_patients = []
    for patient in patients:
        if patient[2] in gene_list:
            filtered_patients.append(patient)
    return filtered_patients

import os
import pandas as pd
import pickle
from pronto import Ontology
from sklearn.model_selection import train_test_split
from CADA.paths import DATA_DIRECTORY
from CADA.reform import *
from CADA.disease_gene_mapping import disease_gene, gene_disease

with open(os.path.join(DATA_DIRECTORY, 'processed', 'ids', 'gene_id_name.dict'), 'rb') as handle:
    gene_id_name = pickle.load(handle)
with open(os.path.join(DATA_DIRECTORY, 'processed', 'ids', 'omim_id_name.dict'), 'rb') as handle:
    omim_id_name = pickle.load(handle)
with open(os.path.join(DATA_DIRECTORY, 'processed', 'ids', 'hpo_id_name.dict'), 'rb') as handle:
    hpo_id_name = pickle.load(handle)

def split(output_directory):
    out_all = os.path.join(output_directory, 'patient.tsv')
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

    # filter out identical patients from different resources
    patients = filter_identical_patients(patients)

    # add gene or disease information if a 1-to-1 relationship for those patients with only gene or disease information
    for patient in patients:
        disease = patient[1]
        gene = patient[2]
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


    # patients = pd.DataFrame(patients, columns=['f2g_id', 'OMIM_id', 'gene_id', 'features', 'submitter', 'from_file'])
    # patients_old_evaluation = pd.read_excel('prioritization.xlsx', header=0)['patient_id']
    # train = patients[~patients['f2g_id'].isin(patients_old_evaluation.values.tolist())]
    # test = patients[patients['f2g_id'].isin(patients_old_evaluation.values.tolist())]
    # patients.to_csv(out_all, index=False, sep='\t')
    # train.to_csv(out_train, index=False, header=None, sep='\t')
    # test.to_csv(out_test, index=False, header=None, sep='\t')
    # train = train.values.tolist()
    # test = test.values.tolist()
    # return train, test

    # split patients into training set and test set

    patients = pd.DataFrame(patients, columns=['patient_id', 'omim_id', 'gene_id', 'features', 'submitter', 'from_file'])
    # train = patients[patients.submitter != 'genetikum']
    # test = patients[patients.submitter == 'genetikum']

    #
    patients = patients.sort_values(patients.columns[2])# sort patients by gene information
    patients.to_csv(out_all, index=False, sep='\t')

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
        patient[3]=features_line
    excel_patients_pd = pd.DataFrame(excel_patients_list, columns=['f2g_id', 'OMIM', 'gene', 'features', 'submitter', 'from_file'])
    excel_patients_pd.to_excel(out_all_excel, index = None)

    train, test = train_test_split(patients, train_size=0.9)
    train.to_csv(out_train, index=False, header=None, sep='\t')
    test.to_csv(out_test, index=False, header=None, sep='\t')
    train = train.values.tolist()
    # test = test.values.tolist()
    return train

def filter_identical_patients(patients):
    filtered_patients = {}
    list_filtered_patients = []
    for patient in patients:
        patient_id = patient[0]
        gene = patient[2]
        if patient_id in filtered_patients:
            if patient[1:] != filtered_patients[patient_id]:
                if gene != 'unknown':
                    filtered_patients[patient_id][1] = gene
        else:
            filtered_patients[patient_id] = patient[1:]

    for key, value in filtered_patients.items():
        item = [key] + value
        list_filtered_patients.append(item)
    return list_filtered_patients

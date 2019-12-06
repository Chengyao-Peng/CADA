import os
import pandas as pd
from pronto import Ontology
from CADA.paths import DATA_DIRECTORY
from CADA.reform import *
from CADA.disease_gene_mapping import disease_gene, gene_disease


def split(output_directory):
    out_all = os.path.join(output_directory, 'patient.tsv')
    out_train = os.path.join(output_directory, 'patient_training.tsv')
    out_test = os.path.join(output_directory, 'patient_testing.tsv')
    # get all patients and update their hpo id to the newest version
    patients = []
    old_new_hpo = {}
    hpo_dir = os.path.join(DATA_DIRECTORY, 'raw', 'hpo', 'hpo_hierarchical_information', 'hp.obo')
    hpo = Ontology(hpo_dir)
    for term in hpo.terms():
        id = term.id
        for alt_id in term.alternate_ids:
            old_new_hpo[alt_id] = id

    patients += reform_pedia(old_new_hpo)
    patients += reform_f2g_fm(old_new_hpo)
    patients += reform_f2g_tucases(old_new_hpo)
    patients += reform_f2g_json(old_new_hpo)
    patients += reform_genetikum(old_new_hpo)

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

    patients = pd.DataFrame(patients, columns=['f2g_id', 'OMIM_id', 'gene_id', 'features', 'submitter', 'from_file'])
    train = patients[patients.submitter != 'genetikum']
    # test = patients[patients.submitter == 'genetikum']
    patients = patients.sort_values(patients.columns[2])# sort patients by gene information
    # train, test = train_test_split(patients, train_size=train_size)
    patients.to_csv(out_all, index=False, sep='\t')
    train.to_csv(out_train, index=False, header=None, sep='\t')
    # test.to_csv(out_test, index=False, header=None, sep='\t')
    train = train.values.tolist()
    # test = test.values.tolist()
    #
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

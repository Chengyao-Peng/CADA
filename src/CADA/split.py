import os
import pandas as pd
from pronto import Ontology
from sklearn.model_selection import train_test_split
from CADA.paths import DATA_DIRECTORY
from CADA.reform import *

def split(train_size, output_directory):
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
    # filter out identical patients from different resources
    patients = filter_identical_patients(patients)

    # split patients into training set and test set
    patients = pd.DataFrame(patients)
    train, test = train_test_split(patients, train_size=train_size)
    patients.to_csv(out_all, index=False, header=None, sep='\t')
    train.to_csv(out_train, index=False, header=None, sep='\t')
    test.to_csv(out_test, index=False, header=None, sep='\t')
    train = train.values.tolist()
    test = test.values.tolist()
    print(train)

    return train, test



def filter_identical_patients(patients):
    filtered_patients = {}
    list_filtered_patients = []
    for patient in patients:
        patient_id = patient[0]
        gene = patients[3]
        if patient_id in filtered_patients:
            if patient[1:] != filtered_patients[patient_id]:
                if gene != 'unknown':
                    filtered_patients[patient_id][2] = gene
        else:
            filtered_patients[patient_id] = patient[1:]

    for key, value in filtered_patients.items():
        item = [key] + value
        list_filtered_patients.append(item)
    return list_filtered_patients

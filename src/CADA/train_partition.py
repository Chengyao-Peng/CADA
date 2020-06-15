import random

def train_partition(train_patient):
    num_percent25 = int(round(len(train_patient)/4))
    list_samples0 = []
    list_samples25 = random.sample(train_patient, num_percent25)
    list_samples50 = list_samples25 + random.sample(diff(train_patient, list_samples25), num_percent25)
    list_samples75 = list_samples50 + random.sample(diff(train_patient, list_samples50), num_percent25)
    list_samples100 = train_patient
    return list_samples0, list_samples25, list_samples50, list_samples75, list_samples100


def diff(li1, li2):
    return [x for x in li1 if x not in li2]
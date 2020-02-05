import requests
import json
import csv
import time


case_ids = []
hpos = []
genes = []
patient_ids = []

with open('result_from_disease.tsv', 'r') as f:
    csv_reader = csv.reader(f, delimiter='\t')
    flag = 1
    for row in csv_reader:
        if flag:
            flag = 0
            continue
        case_id = row[0]
        hpo = row[1]
        gene = row[2]
        case_ids.append(case_id)
        hpos.append(hpo)
        genes.append(gene)
        patient_ids.append(row[3])


create_patient = "https://solutions-sandbox-api.fdna.com/api/patients"
api_key = 'xfsLYg8B29qOnggWcCMJdgsOwv9iDQrQ'

outlist = []
gene_output = []
ranks = []
count = -1

for case_id, hpo_ids, gene, patient_id in zip(case_ids, hpos, genes, patient_ids):
    create_patient = "https://phenobot-api.fdna.com/api/patients"
    external_id = case_id
    if hpo_ids == '':
        continue
    ###### 1. create patient
    response = requests.post(create_patient, data=json.dumps({"external_id": external_id}),
            headers={"apikey": api_key, "Content-Type": "application/json", "Accept": "application/json"})
    token = ''
    if response.status_code == 200:
        patient_data = json.loads(response.content.decode('utf-8'))
    else:
        print(response.status_code)
    patient_id = patient_data['patient_id']
    external_id = patient_data['external_id']
    outline = '{} {}'.format(patient_id, external_id)
    print('Patient created: ' + outline)
    outlist.append(outline)

    ####### 2. upload hpo
    upload_hpo = "https://phenobot-api.fdna.com/api/patients/{}/hpo-annotation"
    response = requests.post(upload_hpo.format(patient_id), data=json.dumps({"hpo_ids": hpo_ids}),
            headers={"apikey": api_key, "Content-Type": "application/json", "Accept": "application/json"})

    if response.status_code == 200:
        patient_data = json.loads(response.content.decode('utf-8'))
    else:
        print(response.status_code)
    print('Upload HPO: ' + hpo_ids)
    time.sleep(10)
    get_analysis = "https://phenobot-api.fdna.com/api/patients/{}/analysis".format(patient_id)
    response = requests.get(get_analysis,
            headers={"apikey": api_key, "Content-Type": "application/json", "Accept": "application/json"})
    results = json.loads(response.content.decode('utf-8'))
    with open('{}.json'.format(external_id), 'w') as f:
        json.dump(results, f)
    if hpo_ids == '':
        gene_output.append([])
        ranks.append('not found')
        continue
    with open('{}.json'.format(external_id), 'r') as f:
        results = json.load(f)
    gene_list = results["genes"]
    gene_rank_list = [t["symbol"] for t in gene_list]
    if gene in gene_rank_list:
        rank = gene_rank_list.index(gene) + 1
    else:
        rank = 'not found'
    ranks.append(rank)
    gene_output.append(gene_rank_list)
for i in outlist:
    print(i)
with open('all_results.csv', 'w') as f:
    for case_id, hpo_ids, gene, rank, gene_list, patient_id in \
            zip(case_ids, hpos, genes, ranks, gene_output, patient_ids):
        out = '\t'.join([case_id, hpo_ids, gene, str(rank), str(gene_list)[1:-1], patient_id]) + '\n'
        f.write(out)

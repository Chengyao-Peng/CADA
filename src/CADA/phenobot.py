import requests
import os
import argparse
import json
import csv
import time
import sys

#api_key = "MDQzN2Q2NTIwNDM2YmM4YTJmMWM5MmMx" # production
api_key = 'xfsLYg8B29qOnggWcCMJdgsOwv9iDQrQ'


def parse_arguments(parser):
    # Parse input arguments
    parser.add_argument('input_file', help='input tsv file')
    parser.add_argument('output', help='output folder')
    parser.add_argument('--download_only',
                        action='store_true',
                        help="For the exsited patient, we only download the results, "
                             "we won't upload HPO for another analysis.")

    return parser.parse_args()


def create_patient(external_id):
    #create_patient = "https://phenobot-api.fdna.com/api/patients"
    create_patient = "https://solutions-sandbox-api.fdna.com/api/patients"
    response = requests.post(create_patient, data=json.dumps({"external_id": external_id}),
            headers={"apikey": api_key, "Content-Type": "application/json", "Accept": "application/json"})
    token = ''
    patient_id = ''
    if response.status_code == 200:
        patient_data = json.loads(response.content.decode('utf-8'))
        patient_id = patient_data['patient_id']
        external_id = patient_data['external_id']
    else:
        print(response.status_code)
        print(response.content)

    return patient_id, response


def upload_hpo(patient_id, hpo_ids, output_dir):
    ##upload_hpo = "https://phenobot-api.fdna.com/api/patients/{}/hpo-annotation"
    upload_hpo = "https://solutions-sandbox-api.fdna.com/api/patients/{}/hpo-annotation"
    response = requests.post(upload_hpo.format(patient_id), data=json.dumps({"hpo_ids": hpo_ids}),
            headers={"apikey": api_key, "Content-Type": "application/json", "Accept": "application/json"})

    if response.status_code == 200:
        patient_data = json.loads(response.content.decode('utf-8'))
    else:
        print(response.status_code)
    print('Upload HPO: ' + hpo_ids)


def get_analysis(patient_id, external_id, output_dir):
    #get_analysis = "https://phenobot-api.fdna.com/api/patients/{}/analysis".format(patient_id)
    retry_count = 10
    get_analysis = "https://solutions-sandbox-api.fdna.com/api/patients/{}/analysis".format(patient_id)
    while retry_count > 0:
        response = requests.get(get_analysis,
            headers={"apikey": api_key, "Content-Type": "application/json", "Accept": "application/json"})
        results = json.loads(response.content.decode('utf-8'))
        if "genes" not in results:
            # did not get results due to some unknow issue
            print('Get analysis error {}, retry {}'.format(patient_id, retry_count))
            time.sleep(15)
            retry_count -= 1
        else:
            break

    with open(os.path.join(output_dir, '{}.json'.format(external_id)), 'w') as f:
        json.dump(results, f)

    return results


def main():
    parser = argparse.ArgumentParser(description='Upload case to Face2Gene API for CADA project')
    args = parse_arguments(parser)

    input_file = args.input_file
    output_dir = args.output
    download_only = args.download_only

    print('Input: {}'.format(input_file))
    print('Output: {}'.format(output_dir))
    print('Download only: {}'.format(download_only))

    case_ids = []
    hpos = []
    genes = []
    patient_ids = []
    count = 0
    #with open('FeatureMatch_Liste_genetikum.csv', 'r') as f:
    #with open('result_from_disease.tsv', 'r') as f:
    #with open('phenobot/evaluation.tsv', 'r') as f:
    with open(input_file, 'r') as f:
        csv_reader = csv.reader(f, delimiter='\t')
        flag = 1
        for row in csv_reader:
            if flag:
                flag = 0
                continue
            case_id = row[0]
            hpo = row[3]
            gene = row[2]
            case_ids.append('case_'+str(count))
            hpos.append(hpo)
            genes.append(gene)
            patient_ids.append(case_id)
            count += 1

    print(patient_ids[0:5])
    print(hpos[0:5])
    print(genes[0:5])
    print(len(case_ids))

    # remove ':' from external id since api doesn't accept this symbol
    patient_ids = [i.replace(':', '_') for i in patient_ids]
    outlist = []
    gene_output = []
    ranks = []
    count = -1
    log_file = open('patien_log_file.csv', 'a')
    for case_id, hpo_ids, gene, external_id in zip(case_ids, hpos, genes, patient_ids):
        if hpo_ids == '':
            continue

        patient_json = os.path.join(output_dir, '{}.json'.format(external_id))
        json_exist = os.path.isfile(patient_json)
        if json_exist:
            print('json already existed')
            continue

        ###### 1. create patient
        patient_id, response = create_patient(external_id)
        outline = '{} {}'.format(patient_id, external_id)

        # case already existed and file already download
        if response.status_code != 200:
            continue

        print('Patient created: ' + outline)
        outlist.append(outline)
        log_file.write("{}, {}\n".format(external_id, patient_id))

        ####### 2. upload hpo
        if not download_only:
            upload_hpo(patient_id, hpo_ids, output_dir)
            time.sleep(15)

        # Get results
        results = get_analysis(patient_id, external_id, output_dir)

        if hpo_ids == '':
            gene_output.append([])
            ranks.append('not found')
            continue
        with open(os.path.join(output_dir, '{}.json'.format(external_id)), 'r') as f:
            results = json.load(f)
        gene_list = results["genes"]
        gene_rank_list = [t["symbol"] for t in gene_list]
        if gene in gene_rank_list:
            rank = gene_rank_list.index(gene) + 1
        else:
            rank = 'not found'
        ranks.append(rank)
        gene_output.append(gene_rank_list)

    log_file.close()

    for i in outlist:
        print(i)

    with open('all_results.csv', 'w') as f:
        for case_id, hpo_ids, gene, rank, gene_list, patient_id in \
                zip(case_ids, hpos, genes, ranks, gene_output, patient_ids):
            out = '\t'.join([case_id, hpo_ids, gene, str(rank), str(gene_list)[1:-1], patient_id]) + '\n'
            f.write(out)

if __name__ == '__main__':
    main()

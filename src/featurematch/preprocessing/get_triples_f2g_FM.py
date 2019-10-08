import pandas as pd
import collections

# items = ['Case_ID', 'Disease', 'HPO_Features', 'absent_HPO_Features']


with open('../../../data/raw/f2g/FM_Benchmark_Gathering_PK.csv', "r") as infile:
    with open('../../../data/raw/f2g/FM_Benchmark_Gathering_PK_comorbidity_filtered.csv', 'w') as outfile:
        bulk = infile.read().rstrip()
        blocks = bulk.split("\n\n")
        for block in blocks:
            lines = block.split('\n')
            f2g_id = lines[0].split('\t')[1]
            present_hpo_id = lines[3].split('\t')[1:]
            present_hpo_name = lines[4].split('\t')[1:]
            absent_hpo_id = lines[5].split('\t')[1:]
            absent_hpo_name = lines[6].split('\t')[1:]
            selected_gene_name = lines[7].split('\t')[1:]
            selected_gene_id = lines[8].split('\t')[1:]
            syndrome_omim_id = lines[9].split('\t')[1:]
            syndrome_name = lines[10].split('\t')[1:]
            diagnosis = lines[11].split('\t')[1:]
            if len(selected_gene_id) <= 1:
                if len(syndrome_name) == 1:
                    outfile.write(f2g_id + '\n')
                    outfile.write(",".join(present_hpo_id) + '\n')
                    outfile.write(",".join(present_hpo_name) + '\n')
                    outfile.write(",".join(absent_hpo_id) + '\n')
                    outfile.write(",".join(absent_hpo_name) + '\n')
                    outfile.write(",".join(selected_gene_name) + '\n')
                    outfile.write(",".join(selected_gene_id) + '\n')
                    outfile.write(",".join(syndrome_omim_id) + '\n')
                    outfile.write(",".join(syndrome_name) + '\n')
                    outfile.write(",".join(diagnosis) + '\n')

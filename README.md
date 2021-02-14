# CADA
CADA (**C**ase **A**nnotations and **D**isease **D**nnotations)  is a phenotype-driven gene prioritization tool for rare syndromes. The tool utilizes both disease-level annotations from Human Phenotype Ontology (HPO) and clinical cases-level annotations to construct a gene-phenotype association network. Later, by applying network representation learning method on the network, disease-causing genes are prioritized by a link prediction task.

This tool was developed during the master's thesis of Chengyao Peng <https://github.com/Chengyao-Peng>.

## Underlying data
The case data used in CADA is in `data/processed/cases/`. There you can find all cases in `all_cases.tsv`, which consist of cases from Clinvar in `clinvar_cases.tsv` and cases from our collaborators in `collaborator_cases.tsv`. All cases are splitted into sets of training `cases_train.tsv`, validation `cases_validate.tsv` and test `cases_test.tsv` with the ratios 60%, 20% and 20%.

       
## Installation

``CADA`` can be installed locally with:
```
    $ git clone https://github.com/Chengyao-Peng/CADA.git
    $ cd CADA
    $ pip install -e . 
```
 
## CLI Usage 
### Arguments:
#### Required:
```
  --hpo_terms        a string of comma-separated HPO terms.
```
#### Optional:
```
  --weighted        use weighted knowledge graph
  --topn            the number of wanted output prioritized genes
  --out_dir         an output file
```
### Example run:
```
CADA --out_dir cada_result --hpo_terms HP:0000573,HP:0001102,HP:0003115,HP:0001681,HP:0008067,HP:0004417 --weighted False --topn 10
```
### Output result file
The out result file from the example run will at 'cada_result/result.txt'.
```
rank    gene_id gene_name       score
1       Entrez:368      ABCC6   84.62940470377605
2       Entrez:5167     ENPP1   69.57813326517741
3       Entrez:54790    TET2    57.23555533091227
4       Entrez:64132    XYLT2   57.030126889546715
5       Entrez:3949     LDLR    55.80375734965006
6       Entrez:64240    ABCG5   53.74869124094645
7       Entrez:348      APOE    53.691530545552574
8       Entrez:462      SERPINC1        51.44988568623861
9       Entrez:255738   PCSK9   50.51583385467529
10      Entrez:2162     F13A1   50.0550905863444
```
## Web Server
We also provide a CADA [Web Server](https://cada.gene-talk.de/webservice).



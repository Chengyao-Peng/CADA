I'm Chengyao. Thank you for this meeting. I'm responsible for a new project, which plan to develop a new algorithm to help diagnosis, like phenomizer does.

But in this project, we don't need any information regarding photos or the F2G project.

We just need highly curated features and the final diagnosis. 



Selected features: by doctors(is_present:1; reliable？) 



Detected features: suggested by algorithm? Are they all present? Score?



Selected syndromes: which is the final and firm diagnosis? Clinical? molecular! Differential? diagnosis

​									208333, two clinical diagnoses, is this a patient with comorbidity? 

​									I've noticed that some consecutive rows have same information. Are they just the same 									so I can just keep one row?

Detected syndromes: suggested by algorithm? final diagnosis?



## Data preparation

### 1. Supplement table from PEDIA

​		**<u>OMIM IDs</u>：126 Autosome ; 3 Xchromosome ; 4 Ychromosome ; 5 Mitochondria** 

​		**<u>Diagnosis</u>: Disease name, some with abbreviation**

​		**<u>In Deep Gestalt test set</u>: n or y**

​		PMID: 

​		**<u>Case ID</u>: Case ids**

​		**<u>Gene</u>: Gene names** 

​		HGVS：	

​		PEDIA rank: 

​		N° of features: 

​		**<u>HPO Features</u>: HPO Term Names**

​		N° of absent features:	

​		Absent HPO Features:	

​		Variation ID:	

​		Clinvar Accession Number:	

​		**<u>HPO</u> : HPO term ids**

​		Absent HPO	

### 2. HPO

#### 		2.1. Ontology(hp.obo): block by block

​				id: HPO term ids

​				synonyms

#### 		2.2. Annotation



​			 **2nd row: Gene names**

​		     **3rd row: HPO Term Names**

​			 **4th row: HPO term ids**

​			1) phenotype_annotation.tab: contains manual and semi-automated annotations

​							**3rd row: Disease name, some with subtypes**

​							**4th row: HPO term ids**

​			2) phenotype_annotation_hpoteam.tab: contains annotations made manually

​														

​							

​			3) negative_phenotype_annotation.tab: contains negative annotations(i.e. a disease is NOT associated with this HPO-term)

​			4) ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt: provides a link between genes and HPO terms. All phenotype terms associated with any disease that is associated with variants in a gene are assigned to that gene in this file. Other files are available on our Jenkins server that filter terms according to provenance of the annotation and frequency of the features in the disease.

​			5) ALL_SOURCES_ALL_FREQUENCIES_phenotype_to_genes.txt: a analogous, but instead provides links from HPO terms to genes.

​		**2nd row: Gene names**

​		**3rd row: HPO Term Names**

​		**4th row: HPO term ids**

### 3. Face2Gene

​		**Case ID: Case ids**

​		**feature_name: HPO Term Names**ls



### 4. Clinvar


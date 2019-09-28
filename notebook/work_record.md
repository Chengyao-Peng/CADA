>>>Setting virtual environment
https://click.palletsprojects.com/en/7.x/quickstart/#virtualenv







Selected features: by doctors(is_present:1; reliable？) 



Detected features: suggested by algorithm? Are they all present? Score?



Selected syndromes: which is the final and firm diagnosis? Clinical? molecular! Differential? diagnosis

​									208333, two clinical diagnoses, is this a patient with comorbidity? 

​									I've noticed that some consecutive rows have same information. Are they just the same 									so I can just keep one row?

Detected syndromes: suggested by algorithm? final diagnosis?



## Data preparation

### 1. Supplement table from PEDIA(六百多)

​		OMIM IDs：126 Autosome ; 3 Xchromosome ; 4 Ychromosome ; 5 Mitochondria 

​		**<u>Diagnosis: Disease name, some with abbreviation</u>**

​		**<u>Case ID: Case ids</u>**

​		<u>**Gene: Gene names**</u> 

​		N° of features: 

​		**<u>HPO Features</u><u>: HPO term names</u>**

​		N° of absent features:	

​		Absent HPO Features:	

​		**<u>HPO : HPO term ids</u>**



### 2. HPO

#### 		2.1. Ontology(hp.obo): block by block

​							<u>**id: HPO term ids**</u>

​							name: HPO term names

​							synonym: synonyms (put it in the data contained in each node or make a map outside KG)

​							**<u>is_a: HPO term ids ! HPO term names</u>**

#### 		2.2. Annotation

​			1) phenotype_annotation.tab: contains manual and semi-automated annotations(176494行)

​							**<u>3rd column: Disease name, some with subtypes</u>**

​							**<u>4th column: HPO term ids</u>**

​			2) phenotype_annotation_hpoteam.tab: contains annotations made manually(100406行)

​							**<u>3rd column: Disease name, some with subtypes</u>**

​							**<u>4th column: HPO term ids</u>**

​			3) negative_phenotype_annotation.tab: contains negative annotations(i.e. a disease is NOT associated with this HPO-term)(可以apply作downstream，906行)

​			4) ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt: provides a link between genes and HPO terms. All phenotype terms associated with any disease that is associated with variants in a gene are assigned to that gene in this file. Other files are available on our Jenkins server that filter terms according to provenance of the annotation and frequency of the features in the disease.(161004行)

​							**<u>2nd column: Gene names</u>**

​							**<u>3rd column: HPO Term Names</u>**（一个基因的所有的有关phenotypes）

​							**<u>4th column: HPO term ids</u>**

​			5) ALL_SOURCES_ALL_FREQUENCIES_phenotype_to_genes.txt: a analogous, but instead provides links from HPO terms to genes.(552815行)

​							**<u>1st column: HPO term ids</u>**

​							**<u>2nd column: HPO-Name</u>**

​							**<u>4th column: Gene-Name</u>**	（一个phenotype有关的所有基因）



### 3. Face2Gene

​		Selected features: case_id, feature_name, hpo_id, is_present

​		Selected syndromes: case_id, syndrrome_name (molecularly_diagnoses的行）去掉那些有comorbidity的



### 4. Clinvar


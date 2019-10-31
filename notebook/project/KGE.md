[TOC]

# Network Representation Learning**

Networks are important ways of representing objects and their relationships. A key problem in the study of networks is how to represent the network information properly. With the developments in machine learning, feature learning of network vertices has become an important area of study. Network representation learning algorithms turn network information into dense, low-dimensional real-valued vectors that can be used as **inputs for existing machine learning algorithms.** For example, the representation of vertices can be fed to a classifier such as a Support Vector Machine (SVM) for vertex classification. In addition, the representations can be used for visualization by taking the representations as points in a Euclidean space. 



## **Definition of  knowledge graph(KG)**

A KG is a multi-relational graph composed of entities (nodes) and relations (different types of edges). Each edge is represented as a **triple** of the form (head entity, relation, tail entity), also called a **fact**, indicating that two entities are connected by a specific relation, e.g., (AlfredHitchcock, DirectorOf, Psycho) 



## **The key idea of KG Embedding(KGE)**

The key idea is to embed components of a KG including **entities and relations into continuous vector spaces**, so as to simplify the manipulation while preserving the inherent structure of the KG.  Those entity and relation embeddings can further be used to benefit all kinds of tasks, such as KG completion, relation extraction, entity classification (http://www.icml-2011.org/papers/438_icmlpaper.pdf; https://www2012.universite-lyon.fr/proceedings/proceedings/p271.pdf) and entity resolution.



## **Techniques of KGE**

Most of the currently available techniques perform the embedding task **solely on the basis of observed facts**. Given a Knowledge graph, such a technique first represents entities and relations in a continuous vector space, and defines a **scoring function** on **each fact** to measure its **plausibility**. Entity and relation embeddings can then be obtained by maximizing the total plausibility of observed facts. During this whole procedure, the learned embeddings are **only** required to be **compatible within each individual fact**, and hence might **not be predictive enough** for downstream tasks. 

As a result, more and more researchers have started to further leverage other types of information, e.g., entity types, relation paths, textual descriptions, and even logical rules, to learn more predictive embeddings. 

### KGE with Facts alone

Suppose we are given a KG consisting of n entities and m relations. E denotes the set of entities, and R the set of relations. Facts observed in the KG are stored as a collection of triples D+ = {(h, r, t)}. Each triple is composed of a head entity h ∈ E, a tail entity t ∈ E, and a relation r∈R between them, e.g., (AlfredHitchcock, DirectorOf, Psycho).

Most of the currently available techniques use facts stored in the KG to perform the embedding task, enforcing embedding to be compatible with the facts.

A typical KG embedding technique generally consists of three steps: 

**(i) representing entities and relations**

**(ii) defining a scoring function**

**(iii) learning entity and relation representations** 

The first step specifies the form in which entities and relations are represented in a continuous vector space. Entities are usually represented as vectors, i.e., deterministic points in the vector space.

Recent work further takes into account uncertainties of entities, and models them through multivariate Gaussian distributions. Relations are typically taken as operations in the vector space, which can be represented as vectors, matrices, tensors, multivariate Gaussian distributions, or even mixtures of Gaussians. Then, in the second step, a scoring function fr(h,t) is defined on each fact (h, r, t) to measure its plausibility. Facts observed in the KG tend to have higher scores than those that have not been observed. Finally, to learn those entity and relation







Skip-gram model

The man hit his son. 
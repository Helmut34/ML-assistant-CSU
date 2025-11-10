## Notes for The Automation of Ontology by Aaron Wacker ##

Taxonomy - a hiearichal and systematic structure into which you classify data

Challange Scenario - Youre a data scientist. You have existing data an have recently acquired a new dataset to supplement your own. However, the new dataset is classified into a different taxonomy from what you have. You want to reconcile the data in orer to develop categorical metrics and dashboard of ALL the data.


# Potential Fixes #

Possible Technique 1: Append - no categories contain records from both datasets.

Possible Technique 2: Map - map both taxonomies into a dictionary, Problem: Things map in multiple ways and hierarchy structure is lost

Proposed Technique 3: Merge - align each taxonomy to one between txonomy of common industry vocabulary

The Proposal: use an ontology as a way of translating one to the other to combine data sources aroun a single taxonomy, rather than linking Taxonomy A and Taxonomy B, map them to a new ontology, allowing us to have centralized hierachile strucutre, while not disturbing the original taxonomy. 

## General ##

What is an Ontology? - framework of common indutry vocabulary defining hierachial taxonomy, relationships, etc. according to industry standard.

** List of Common Ontologies **
** MedDRA, OAE, FIBO **

## Datasets ## 

	Datasets can be used to generate taxonomies, which can later be used to create the ontology (testing purposes)


## Ingesting Ontology## 
 #look into Neo4j with semantics plugin#

 PICK BACK UP AT 16:0 IN THE VIDEO
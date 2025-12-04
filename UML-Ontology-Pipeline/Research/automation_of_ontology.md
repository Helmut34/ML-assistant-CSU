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

---

## Detailed Solutions for Taxonomy Alignment ##

The following outlines comprehensive solutions to the challenge of aligning disparate taxonomies from different datasets into a unified framework for effective classification and analysis.

### 1. Appending Taxonomies Directly
**Approach**: The simplest method - append the two taxonomies together, assuming no overlap.

**Limitations**:
- Leads to a large, duplicated taxonomy with no unified categories
- No semantic relationships between similar concepts
- Ineffective for meaningful analysis and classification

### 2. Mapping One Taxonomy into Another via Dictionary
**Approach**: Choose one taxonomy as the "preferred" taxonomy and map categories from the other taxonomy into it using a dictionary/lookup table.

**Advantages**:
- Better than simple appending
- Provides some unification

**Limitations**:
- Risks losing hierarchical structure
- Reduced trustworthiness because categories in one taxonomy may map to multiple places in the other
- One-directional mapping may lose information
- No preservation of original taxonomic relationships

### 3. Using a Universal Taxonomy or Ontology as a Wrapper ⭐ (Main Proposed Solution)
**Approach**: Use an ontology as a universal, trusted taxonomy that encapsulates overarching concepts from both taxonomies.

**Key Concept**: Rather than mapping taxonomies directly onto each other, both taxonomies are mapped to a central ontology.

**Advantages**:
- Preserves the integrity of each original taxonomy
- Provides a unified structure for analysis and interoperability
- Maintains hierarchical relationships
- Enables cross-taxonomy queries and analysis
- Industry-standard approach
- Scalable to multiple taxonomies

**Implementation**: Map Taxonomy A → Ontology ← Map Taxonomy B

### 4. Automated Mapping Algorithms to Ontology
**Approach**: Develop programmatic algorithms that automatically map categories from each dataset into the ontology.

**Purpose**:
- Handle large and evolving datasets
- Avoid massive manual effort required to align taxonomies
- Allow continuous updates without redoing the entire mapping
- Scale to hundreds or thousands of categories

**Benefits**:
- Reduces human error
- Enables real-time taxonomy alignment
- Reproducible and auditable process

### 5. Semantic Matching Using Embeddings

#### 5.1 Doc2Vec on Category Names
**Approach**: Use Doc2Vec trained on external corpora (like Wikipedia) to generate vector embeddings of category names.

**Process**:
1. Train Doc2Vec model on large corpus (Wikipedia, domain-specific texts)
2. Generate embeddings for category names from both taxonomies
3. Compute cosine similarity between category embeddings and ontology concepts
4. Find best matches based on similarity scores

**Advantages**:
- Captures semantic meaning of category names
- Leverages existing knowledge from training corpus
- Can identify synonyms and related concepts

#### 5.2 Doc2Vec on Book Titles (or Content)
**Approach**: Embed the aggregated book titles (or other content) within each category to provide additional context for semantic matching.

**Hypothesis**: The titles/content reflect the category's meaning better than the category name alone.

**Process**:
1. Aggregate all titles/content within a category
2. Generate Doc2Vec embeddings from this aggregated text
3. Compare to ontology concept embeddings
4. Use similarity scores for mapping

**Advantages**:
- Richer context than category names alone
- Handles ambiguous or generic category names
- More robust to naming inconsistencies

#### 5.3 Node2Vec Graph Embeddings
**Approach**: Generate node embeddings based on graph traversal of the taxonomy hierarchy to capture structural relationships.

**Process**:
1. Represent taxonomy as a graph (nodes = categories, edges = relationships)
2. Use Node2Vec to generate embeddings based on graph structure
3. Capture hierarchical and neighborhood information
4. Compare structural similarity between taxonomies and ontology

**Note**: Showed less reliability in initial testing but captures structural information that text-based methods miss.

### 6. Building an Answer Key and Model Evaluation
**Approach**: Create a manually curated "Answer Key" to evaluate and compare the effectiveness of different embedding and similarity metrics.

**Process**:
1. Manually create ground truth mappings for a sample of categories
2. Test different embedding methods (Doc2Vec on names, Doc2Vec on content, Node2Vec)
3. Evaluate accuracy, precision, recall
4. Select the best approach for automatic mapping
5. Fine-tune parameters based on evaluation results

**Benefits**:
- Ensures quality before full-scale automation
- Identifies edge cases and challenges
- Provides confidence metrics for automated mappings

### 7. Graph Database Implementation
**Technology**: Neo4j with neosemantics plugin

**Capabilities**:
- Ingest ontology and taxonomies as graph structures
- Enable efficient traversal of hierarchical relationships
- Store embeddings as node properties
- Perform similarity computations at scale
- Query relationships across taxonomies via ontology

**Workflow**:
1. Import ontology into Neo4j using neosemantics
2. Import taxonomies as separate graph layers
3. Store embeddings as node properties
4. Use Cypher queries to find mappings based on similarity
5. Visualize and validate mappings

### 8. Alternative Future Enhancements

#### 8.1 Domain-Specific Training Corpora
**Approach**: Train Doc2Vec or other embedding models on domain-specific corpora (e.g., library databases, scientific literature, domain-specific websites).

**Benefits**:
- Improved semantic accuracy for domain-specific terminology
- Better handling of jargon and specialized vocabulary
- More accurate similarity measures

#### 8.2 Incorporating Additional Textual Data
**Sources**:
- Book descriptions and summaries
- Amazon/vendor reviews
- User-generated tags and keywords
- Metadata fields (authors, subjects, keywords)
- Full-text content (when available)

**Benefits**:
- Richer embeddings with more context
- Multiple perspectives on category meaning
- Improved disambiguation

#### 8.3 Automated ML/Classification Tools
**Approach**: Consider vendor-provided or cloud-based automated machine learning tools for classification and mapping.

**Examples**:
- Azure ML AutoML
- Google Cloud AutoML
- AWS SageMaker Autopilot
- Specialized taxonomy alignment tools

**Benefits**:
- Reduced implementation effort
- Leverages state-of-the-art models
- Continuous model updates

---

## Summary of Solution Progression

1. **Naïve Methods** (Append, Dictionary Mapping)
   - Simple but ineffective
   - Loss of information and structure

2. **Ontology-Centered Approach** ⭐
   - Central unified framework
   - Preserves original taxonomies
   - Industry standard

3. **Automated Semantic Mapping**
   - Embedding-based similarity
   - Multiple embedding strategies
   - Evaluation and validation

4. **Graph Database Infrastructure**
   - Efficient storage and traversal
   - Similarity computations at scale
   - Visualization and validation

5. **Continuous Improvement**
   - Domain-specific training
   - Richer data sources
   - ML automation tools

---
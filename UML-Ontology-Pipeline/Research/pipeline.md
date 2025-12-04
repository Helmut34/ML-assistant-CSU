# How to go from UML diagram to an Ontology #
*by Helmut Cespedes*

## Overview

This document outlines the implementation of multiple pipeline approaches for converting UML class diagrams to OWL ontologies, comparing different transformation strategies and LLM backends.

---

## UML to OWL Transformation Rules

### Core Mapping Rules

**Class** → `owl:Class`
Basic concept mapping

**Attribute** → `owl:DatatypeProperty`
Properties with literal values (strings, numbers, dates)

**Association** → `owl:ObjectProperty`
Relationships between classes

**Generalization** → `rdfs:subClassOf`
Inheritance hierarchy

**Multiplicity 1..1** → `owl:FunctionalProperty`
Exactly one value required

**Multiplicity 0..\*** → No restrictions
Optional, unbounded

**Multiplicity 1..\*** → `owl:minCardinality 1`
At least one value required

**Abstract Class** → `owl:Class` with disjointness
Cannot be directly instantiated

**Interface** → `owl:Class`
Typically abstract

### Advanced Mappings

- **Composition**: `owl:ObjectProperty` with domain/range restrictions
- **Aggregation**: `owl:ObjectProperty` with weaker constraints
- **Bidirectional Associations**: Inverse properties (`owl:inverseOf`)
- **Association Classes**: Reified relationships
- **Enumerations**: `owl:oneOf` for closed sets

---

## Challenges & Considerations

### Semantic Gap
There is a **high semantic gap** between UML and ontologies:
- UML focuses on software structure and behavior
- OWL focuses on knowledge representation and reasoning
- Different modeling philosophies require careful translation

### Key Issues
1. **Open World Assumption**: OWL assumes incomplete information
2. **Unique Name Assumption**: UML assumes unique names, OWL does not
3. **Closed vs Open**: UML models are typically closed, ontologies are open
4. **Cardinality Semantics**: Different interpretation of constraints
5. **Methods/Operations**: No direct OWL equivalent

## Pipeline 1: Direct Transformation (ontologyGenerator)

### Architecture
```
┌─────────────┐
│  UML XMI    │
│   Input     │
└──────┬──────┘
       │
       │ 
       │
       ▼
┌─────────────┐
│OWL Ontology │
│   (Turtle)  │
└─────────────┘
```


### Implementation
```python
ontology = model.generate(
    uml_xmi,
    prompt="Convert UML to OWL Turtle format"
)
```

### Models
- Ollama (LLaMA 3.1, Mixtral)
- GPT-4
- Codex/GPT-3.5

### Location
`/ontologyGenerator/`

---

## Pipeline 2: Two-Step Transformation (V1)

### Architecture
```
┌─────────────┐
│  UML XMI    │
└──────┬──────┘
       │
       ├
       ▼
┌─────────────┐
│  UML Code   │
│ (Structured)│
└──────┬──────┘
       │
       ├
       ▼
┌─────────────┐
│OWL Ontology │
└─────────────┘
```

### Key Insight
The intermediate UML Code representation:
- Makes structure explicit and parseable
- Allows validation before ontology generation
- Improves handling of complex relationships
- Enables debugging of transformation

### Implementation
```python
# Step 1: UML → Structured Code
uml_code = model.uml_to_code(uml_xmi)

# Step 2: Code → Ontology
ontology = model.code_to_ontology(uml_code)
```

### Location
`/ontologyGenerator_V1/`

---

## Pipeline 3: Three-Step with Taxonomy (V2)

### Architecture
```
┌─────────────┐
│  UML XMI    │
└──────┬──────┘
       │
       ├
       ▼
┌─────────────┐
│  UML Code   │
└──────┬──────┘
       │
       ├
       ▼
┌─────────────┐
│  Taxonomy   │
│   		  │
└──────┬──────┘
       │
       ├
       ▼
┌─────────────┐
│OWL Ontology │
│  + SKOS     │
└─────────────┘
```

### Implementation
```python
# Step 1: UML → Structured Code
uml_code = model.uml_to_code(uml_xmi)

# Step 2: Code → Taxonomy
taxonomy = model.code_to_taxonomy(uml_code)

# Step 3: Taxonomy → Ontology
ontology = model.taxonomy_to_ontology(taxonomy)
```

### Location
`/ontologyGenerator_V2/`

---

## Pipeline 4: Custom Proprietary Model ( - WIP)


### Location
`/ontologyGenerator_V3/` (WIP)


### Metrics Collected

All pipelines track:
- **Input size**: Characters, KB
- **Generation time**: Per step and total
- **Output size**: Ontology size
- **Token usage**: For API-based models
- **Success rate**: Completion status
- **Error tracking**: Detailed error messages






 # How to go from UML diagram to a Ontologie #
*by Helmut Cespedes*

**Notes**
	May need to use multiple models in order to achieve a full ontologie. A "thinking" model may be needed along with a nonthinking model. One specializing in code, and the other in the transformation itself.


**Rules**
	Class	->	owl:Class

	Attribute -> owl:DatatypeProperty

	Association -> owl:ObjectProperty

	Generalization -> rdfs:subClassOf

	Multiplicity 1-1 -> Functional Property

	Multiplicity 0 -> No Restrictions

	Abstract Class -> owl:Class + disjointness


**Issues**
	There is a High semantic gap between UMLs and ontologies.


**How to**
*Will be updated as development begins*

1.	Preprocessing - Parse UML

2.	TBD





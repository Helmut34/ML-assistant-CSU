#Ollama Model 1.80 integration for ontology generation, for benchmarking purposes.
#by Helmut Cespedes

import json
import ollama

def generate_ontology_with_ollama(uml: str, model: str = "ollama1.8b"):

    prompt = f"""You are an expert in converting UML diagrams into OWL ontologies.
    Given the following UML diagram XMI, generate a corresponding OWL ontology in Turtle format.

    UML XMI:
    {uml}
    
    Respond only with the OWL ontology in Turtle format, without any additional explanations.

    Args:
        uml (str): The UML diagram in XMI format.
        model (str): The Ollama model to use for generation.

    Respond ONLY with the OWL ontology in Turtle format in a JSON file:
    
    """
    try:
        response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error generating ontology with Ollama: {e}")
        return ""
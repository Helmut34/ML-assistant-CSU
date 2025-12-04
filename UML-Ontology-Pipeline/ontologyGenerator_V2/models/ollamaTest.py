"""
Ollama Model integration for V2 pipeline: UML → UML Code → Taxonomy → Ontology.
Uses Ollama with three-step transformation for benchmarking purposes.

Author: Helmut Cespedes
"""

import json
import time
from datetime import datetime
from typing import Tuple, Union, Dict
import ollama


def uml_to_code(uml: str, model: str = "llama3.1:8b") -> str:
    """
    Convert UML XMI to structured UML code representation.

    Args:
        uml (str): The UML diagram in XMI format.
        model (str): The Ollama model to use.

    Returns:
        str: Structured UML code representation.
    """
    prompt = f"""You are an expert in parsing UML diagrams.
Convert the following UML XMI into a structured, human-readable UML code representation.

Extract and format:
1. All classes with their attributes and types
2. Inheritance relationships
3. Associations and their cardinalities
4. Data types

Format as clean, structured code-like notation.

UML XMI:
{uml}

Respond ONLY with the structured UML code, no explanations.
"""

    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content'].strip()
    except Exception as e:
        raise RuntimeError(f"Error converting UML to code: {e}")


def code_to_taxonomy(uml_code: str, model: str = "llama3.1:8b") -> str:
    """
    Convert structured UML code to taxonomy (hierarchical classification).

    Args:
        uml_code (str): Structured UML code representation.
        model (str): The Ollama model to use.

    Returns:
        str: Taxonomy representation in a structured format.
    """
    prompt = f"""You are an expert in knowledge organization and taxonomy design.
Convert the following structured UML code into a taxonomy (hierarchical classification system).

A taxonomy should:
1. Identify the main concepts and their hierarchical relationships
2. Organize classes into broader and narrower terms
3. Group related concepts together
4. Define clear parent-child relationships
5. Include properties as characteristics of concepts

Format the taxonomy in a clear, hierarchical text format using indentation.

UML Code:
{uml_code}

Respond ONLY with the taxonomy in hierarchical format, no explanations.
"""

    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content'].strip()
    except Exception as e:
        raise RuntimeError(f"Error converting code to taxonomy: {e}")


def taxonomy_to_ontology(taxonomy: str, model: str = "llama3.1:8b") -> str:
    """
    Convert taxonomy to full OWL ontology.

    Args:
        taxonomy (str): Taxonomy representation.
        model (str): The Ollama model to use.

    Returns:
        str: OWL ontology in Turtle format.
    """
    prompt = f"""You are an expert in creating OWL ontologies.
Convert the following taxonomy into a complete OWL ontology in Turtle format.

Requirements:
1. Use proper OWL/RDFS namespaces (owl:, rdfs:, rdf:)
2. Convert concepts to owl:Class
3. Preserve hierarchical relationships with rdfs:subClassOf
4. Define properties as owl:DatatypeProperty or owl:ObjectProperty
5. Include cardinality constraints using owl:Restriction
6. Add SKOS annotations for taxonomy terms (skos:broader, skos:narrower)
7. Include rdfs:label and rdfs:comment for documentation

Taxonomy:
{taxonomy}

Respond ONLY with the OWL ontology in Turtle format, without explanations.
"""

    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content'].strip()
    except Exception as e:
        raise RuntimeError(f"Error converting taxonomy to ontology: {e}")


def generate_ontology_with_ollama_v2(
    uml: str,
    model: str = "llama3.1:8b",
    benchmark: bool = True
) -> Union[Tuple[str, str, str], Tuple[str, str, str, Dict]]:
    """
    Generate OWL ontology from UML using V2 pipeline: UML → UML Code → Taxonomy → Ontology.

    Args:
        uml (str): The UML diagram in XMI format.
        model (str): The Ollama model to use.
        benchmark (bool): Whether to collect benchmarking metrics.

    Returns:
        If benchmark=True: (uml_code, taxonomy, ontology, metrics_dict)
        If benchmark=False: (uml_code, taxonomy, ontology)
    """
    metrics = {
        "model": model,
        "pipeline": "V2 (UML → Code → Taxonomy → Ontology)",
        "timestamp": datetime.now().isoformat(),
        "input_size_chars": len(uml),
        "input_size_kb": len(uml.encode('utf-8')) / 1024,
    }

    try:
        overall_start = time.time()

        # Step 1: UML → UML Code
        step1_start = time.time()
        uml_code = uml_to_code(uml, model)
        step1_time = time.time() - step1_start

        # Step 2: UML Code → Taxonomy
        step2_start = time.time()
        taxonomy = code_to_taxonomy(uml_code, model)
        step2_time = time.time() - step2_start

        # Step 3: Taxonomy → Ontology
        step3_start = time.time()
        ontology = taxonomy_to_ontology(taxonomy, model)
        step3_time = time.time() - step3_start

        total_time = time.time() - overall_start

        if benchmark:
            metrics.update({
                "step1_uml_to_code_seconds": round(step1_time, 3),
                "step2_code_to_taxonomy_seconds": round(step2_time, 3),
                "step3_taxonomy_to_ontology_seconds": round(step3_time, 3),
                "total_generation_time_seconds": round(total_time, 3),
                "intermediate_code_size_chars": len(uml_code),
                "intermediate_code_size_kb": len(uml_code.encode('utf-8')) / 1024,
                "intermediate_taxonomy_size_chars": len(taxonomy),
                "intermediate_taxonomy_size_kb": len(taxonomy.encode('utf-8')) / 1024,
                "output_size_chars": len(ontology),
                "output_size_kb": len(ontology.encode('utf-8')) / 1024,
                "success": True,
                "error": None
            })
            return uml_code, taxonomy, ontology, metrics
        else:
            return uml_code, taxonomy, ontology

    except Exception as e:
        error_msg = f"Error in V2 pipeline with Ollama: {e}"
        print(error_msg)

        if benchmark:
            metrics.update({
                "total_generation_time_seconds": 0,
                "output_size_chars": 0,
                "output_size_kb": 0,
                "success": False,
                "error": str(e)
            })
            return "", "", "", metrics
        else:
            return "", "", ""


def save_benchmark_results(metrics: dict, output_file: str = "benchmark_results_v2.json") -> None:
    """
    Save benchmark metrics to a JSON file (append mode).

    Args:
        metrics (dict): The metrics dictionary to save.
        output_file (str): Path to the output JSON file.
    """
    try:
        try:
            with open(output_file, "r") as f:
                results = json.load(f)
        except FileNotFoundError:
            results = []

        results.append(metrics)

        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)

        print(f"V2 Benchmark results saved to {output_file}")

    except Exception as e:
        print(f"Error saving benchmark results: {e}")


def print_metrics(metrics: dict) -> None:
    """
    Pretty print V2 pipeline benchmark metrics.

    Args:
        metrics (dict): The metrics dictionary to print.
    """
    print("\n" + "="*60)
    print("BENCHMARK RESULTS - OLLAMA V2 PIPELINE")
    print("="*60)
    print(f"Model: {metrics['model']}")
    print(f"Pipeline: {metrics['pipeline']}")
    print(f"Timestamp: {metrics['timestamp']}")
    print(f"Status: {'Success' if metrics['success'] else 'Failed'}")
    print("="*60)
    print(f"Input Size: {metrics['input_size_chars']} chars ({metrics['input_size_kb']:.2f} KB)")

    if 'intermediate_code_size_chars' in metrics:
        print(f"Intermediate Code: {metrics['intermediate_code_size_chars']} chars ({metrics['intermediate_code_size_kb']:.2f} KB)")

    if 'intermediate_taxonomy_size_chars' in metrics:
        print(f"Intermediate Taxonomy: {metrics['intermediate_taxonomy_size_chars']} chars ({metrics['intermediate_taxonomy_size_kb']:.2f} KB)")

    if 'output_size_chars' in metrics:
        print(f"Output Size: {metrics['output_size_chars']} chars ({metrics['output_size_kb']:.2f} KB)")

    print("="*60)
    if 'step1_uml_to_code_seconds' in metrics:
        print(f"Step 1 (UML → Code): {metrics['step1_uml_to_code_seconds']} seconds")
    if 'step2_code_to_taxonomy_seconds' in metrics:
        print(f"Step 2 (Code → Taxonomy): {metrics['step2_code_to_taxonomy_seconds']} seconds")
    if 'step3_taxonomy_to_ontology_seconds' in metrics:
        print(f"Step 3 (Taxonomy → Ontology): {metrics['step3_taxonomy_to_ontology_seconds']} seconds")
    if 'total_generation_time_seconds' in metrics:
        print(f"Total Time: {metrics['total_generation_time_seconds']} seconds")

    if metrics.get('error'):
        print("="*60)
        print(f"Error: {metrics['error']}")

    print("="*60 + "\n")


if __name__ == "__main__":
    with open("../UML-test/test1.xml", "r") as f:
        uml_xmi = f.read()

    print("Generating ontology with Ollama V2 Pipeline...")
    uml_code, taxonomy, ontology_ttl, metrics = generate_ontology_with_ollama_v2(
        uml_xmi,
        model="llama3.1:8b",
        benchmark=True
    )

    print_metrics(metrics)

    if uml_code:
        with open("../benchmark/ollama_v2_uml_code.txt", "w") as f:
            f.write(uml_code)
        print("UML code saved to ../benchmark/ollama_v2_uml_code.txt")

    if taxonomy:
        with open("../benchmark/ollama_v2_taxonomy.txt", "w") as f:
            f.write(taxonomy)
        print("Taxonomy saved to ../benchmark/ollama_v2_taxonomy.txt")

    if ontology_ttl:
        with open("../benchmark/ollama_v2_ontology.ttl", "w") as f:
            f.write(ontology_ttl)
        print("Ontology saved to ../benchmark/ollama_v2_ontology.ttl")

    save_benchmark_results(metrics, "../benchmark/ollama_v2_benchmark.json")

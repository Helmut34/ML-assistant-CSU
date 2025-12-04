"""
Codex Model integration for V1 pipeline: UML ’ UML Code ’ Ontology.
Uses OpenAI Codex API for benchmarking purposes.

Author: Helmut Cespedes
"""

import json
import time
from datetime import datetime
from typing import Tuple, Union, Dict
import openai
import os


def uml_to_code(uml: str, model: str = "gpt-3.5-turbo", api_key: str = None) -> str:
    """
    Convert UML XMI to structured UML code representation.

    Args:
        uml (str): The UML diagram in XMI format.
        model (str): The model to use.
        api_key (str): OpenAI API key (if None, uses OPENAI_API_KEY env var).

    Returns:
        str: Structured UML code representation.
    """
    if api_key:
        openai.api_key = api_key
    elif os.getenv("OPENAI_API_KEY"):
        openai.api_key = os.getenv("OPENAI_API_KEY")
    else:
        raise ValueError("No OpenAI API key provided. Set OPENAI_API_KEY environment variable or pass api_key parameter.")

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
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert in UML modeling and parsing."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Error converting UML to code: {e}")


def code_to_ontology(uml_code: str, model: str = "gpt-3.5-turbo", api_key: str = None) -> str:
    """
    Convert structured UML code to OWL ontology.

    Args:
        uml_code (str): Structured UML code representation.
        model (str): The model to use.
        api_key (str): OpenAI API key (if None, uses OPENAI_API_KEY env var).

    Returns:
        str: OWL ontology in Turtle format.
    """
    if api_key:
        openai.api_key = api_key
    elif os.getenv("OPENAI_API_KEY"):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    prompt = f"""You are an expert in creating OWL ontologies.
Convert the following structured UML code into an OWL ontology in Turtle format.

Requirements:
1. Use proper OWL/RDFS namespaces (owl:, rdfs:, rdf:)
2. Convert classes to owl:Class
3. Preserve inheritance with rdfs:subClassOf
4. Define properties as owl:DatatypeProperty or owl:ObjectProperty
5. Include cardinality constraints using owl:Restriction
6. Maintain all associations and multiplicities

UML Code:
{uml_code}

Respond ONLY with the OWL ontology in Turtle format, without explanations.
"""

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert ontology engineer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Error converting code to ontology: {e}")


def generate_ontology_with_codex_v1(
    uml: str,
    model: str = "gpt-3.5-turbo",
    api_key: str = None,
    benchmark: bool = True
) -> Union[Tuple[str, str], Tuple[str, str, Dict]]:
    """
    Generate OWL ontology from UML using V1 pipeline: UML ’ UML Code ’ Ontology.

    Args:
        uml (str): The UML diagram in XMI format.
        model (str): The model to use.
        api_key (str): OpenAI API key (if None, uses OPENAI_API_KEY env var).
        benchmark (bool): Whether to collect benchmarking metrics.

    Returns:
        If benchmark=True: (uml_code, ontology, metrics_dict)
        If benchmark=False: (uml_code, ontology)
    """
    metrics = {
        "model": model,
        "pipeline": "V1 (UML ’ Code ’ Ontology)",
        "timestamp": datetime.now().isoformat(),
        "input_size_chars": len(uml),
        "input_size_kb": len(uml.encode('utf-8')) / 1024,
    }

    try:
        overall_start = time.time()

        # Step 1: UML ’ UML Code
        step1_start = time.time()
        uml_code = uml_to_code(uml, model, api_key)
        step1_time = time.time() - step1_start

        # Step 2: UML Code ’ Ontology
        step2_start = time.time()
        ontology = code_to_ontology(uml_code, model, api_key)
        step2_time = time.time() - step2_start

        total_time = time.time() - overall_start

        if benchmark:
            metrics.update({
                "step1_uml_to_code_seconds": round(step1_time, 3),
                "step2_code_to_ontology_seconds": round(step2_time, 3),
                "total_generation_time_seconds": round(total_time, 3),
                "intermediate_code_size_chars": len(uml_code),
                "intermediate_code_size_kb": len(uml_code.encode('utf-8')) / 1024,
                "output_size_chars": len(ontology),
                "output_size_kb": len(ontology.encode('utf-8')) / 1024,
                "success": True,
                "error": None
            })
            return uml_code, ontology, metrics
        else:
            return uml_code, ontology

    except Exception as e:
        error_msg = f"Error in V1 pipeline with Codex: {e}"
        print(error_msg)

        if benchmark:
            metrics.update({
                "total_generation_time_seconds": 0,
                "output_size_chars": 0,
                "output_size_kb": 0,
                "success": False,
                "error": str(e)
            })
            return "", "", metrics
        else:
            return "", ""


def save_benchmark_results(metrics: dict, output_file: str = "benchmark_results_v1.json") -> None:
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

        print(f"V1 Benchmark results saved to {output_file}")

    except Exception as e:
        print(f"Error saving benchmark results: {e}")


def print_metrics(metrics: dict) -> None:
    """
    Pretty print V1 pipeline benchmark metrics.

    Args:
        metrics (dict): The metrics dictionary to print.
    """
    print("\n" + "="*60)
    print("BENCHMARK RESULTS - CODEX V1 PIPELINE")
    print("="*60)
    print(f"Model: {metrics['model']}")
    print(f"Pipeline: {metrics['pipeline']}")
    print(f"Timestamp: {metrics['timestamp']}")
    print(f"Status: {'Success' if metrics['success'] else 'Failed'}")
    print("="*60)
    print(f"Input Size: {metrics['input_size_chars']} chars ({metrics['input_size_kb']:.2f} KB)")

    if 'intermediate_code_size_chars' in metrics:
        print(f"Intermediate Code: {metrics['intermediate_code_size_chars']} chars ({metrics['intermediate_code_size_kb']:.2f} KB)")

    if 'output_size_chars' in metrics:
        print(f"Output Size: {metrics['output_size_chars']} chars ({metrics['output_size_kb']:.2f} KB)")

    print("="*60)
    if 'step1_uml_to_code_seconds' in metrics:
        print(f"Step 1 (UML ’ Code): {metrics['step1_uml_to_code_seconds']} seconds")
    if 'step2_code_to_ontology_seconds' in metrics:
        print(f"Step 2 (Code ’ Ontology): {metrics['step2_code_to_ontology_seconds']} seconds")
    if 'total_generation_time_seconds' in metrics:
        print(f"Total Time: {metrics['total_generation_time_seconds']} seconds")

    if metrics.get('error'):
        print("="*60)
        print(f"Error: {metrics['error']}")

    print("="*60 + "\n")


if __name__ == "__main__":
    with open("../UML-test/test1.xml", "r") as f:
        uml_xmi = f.read()

    print("Generating ontology with Codex V1 Pipeline...")
    uml_code, ontology_ttl, metrics = generate_ontology_with_codex_v1(
        uml_xmi,
        model="gpt-3.5-turbo",
        benchmark=True
    )

    print_metrics(metrics)

    if uml_code:
        with open("../benchmark/codex_v1_uml_code.txt", "w") as f:
            f.write(uml_code)
        print("UML code saved to ../benchmark/codex_v1_uml_code.txt")

    if ontology_ttl:
        with open("../benchmark/codex_v1_ontology.ttl", "w") as f:
            f.write(ontology_ttl)
        print("Ontology saved to ../benchmark/codex_v1_ontology.ttl")

    save_benchmark_results(metrics, "../benchmark/codex_v1_benchmark.json")

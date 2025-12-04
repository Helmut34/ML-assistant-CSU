"""
Mixtral Model integration for direct UML to ontology generation.
Uses Ollama with Mixtral model for benchmarking purposes.

Author: Helmut Cespedes
"""

import json
import time
from datetime import datetime
from typing import Tuple, Union
import ollama


def generate_ontology_with_mixtral(uml: str, model: str = "mixtral:latest", benchmark: bool = True) -> Union[str, Tuple[str, dict]]:
    """
    Generate an OWL ontology directly from UML XMI using Mixtral via Ollama.

    Args:
        uml (str): The UML diagram in XMI format.
        model (str): The Mixtral model to use (default: "mixtral:latest").
        benchmark (bool): Whether to collect benchmarking metrics (default: True).

    Returns:
        tuple: (ontology_content, metrics_dict) if benchmark=True, else just ontology_content
    """

    metrics = {
        "model": model,
        "timestamp": datetime.now().isoformat(),
        "input_size_chars": len(uml),
        "input_size_kb": len(uml.encode('utf-8')) / 1024,
    }

    prompt = f"""You are an expert in converting UML diagrams into OWL ontologies.
Given the following UML diagram in XMI format, generate a corresponding OWL ontology in Turtle format.

Requirements:
1. Use proper OWL/RDFS namespaces (owl:, rdfs:, rdf:)
2. Convert UML classes to owl:Class
3. Preserve inheritance relationships with rdfs:subClassOf
4. Define properties as owl:DatatypeProperty or owl:ObjectProperty
5. Include cardinality constraints using owl:Restriction
6. Maintain all associations and their multiplicities

UML XMI:
{uml}

Respond ONLY with the OWL ontology in Turtle format, without any additional explanations or JSON wrapping.
"""

    try:
        start_time = time.time()

        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )

        end_time = time.time()

        ontology_content = response['message']['content'].strip()

        if benchmark:
            metrics.update({
                "generation_time_seconds": round(end_time - start_time, 3),
                "output_size_chars": len(ontology_content),
                "output_size_kb": len(ontology_content.encode('utf-8')) / 1024,
                "success": True,
                "error": None
            })

            if 'eval_count' in response:
                metrics["tokens_generated"] = response.get('eval_count', 0)
                metrics["tokens_per_second"] = round(
                    response.get('eval_count', 0) / (end_time - start_time), 2
                )

            return ontology_content, metrics
        else:
            return ontology_content

    except Exception as e:
        error_msg = f"Error generating ontology with Mixtral: {e}"
        print(error_msg)

        if benchmark:
            metrics.update({
                "generation_time_seconds": 0,
                "output_size_chars": 0,
                "output_size_kb": 0,
                "success": False,
                "error": str(e)
            })
            return "", metrics
        else:
            return ""


def save_benchmark_results(metrics: dict, output_file: str = "benchmark_results.json") -> None:
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

        print(f"Benchmark results saved to {output_file}")

    except Exception as e:
        print(f"Error saving benchmark results: {e}")


def print_metrics(metrics: dict) -> None:
    """
    Pretty print benchmark metrics.

    Args:
        metrics (dict): The metrics dictionary to print.
    """
    print("\n" + "="*50)
    print("BENCHMARK RESULTS - MIXTRAL")
    print("="*50)
    print(f"Model: {metrics['model']}")
    print(f"Timestamp: {metrics['timestamp']}")
    print(f"Input Size: {metrics['input_size_chars']} chars ({metrics['input_size_kb']:.2f} KB)")
    print(f"Generation Time: {metrics['generation_time_seconds']} seconds")
    print(f"Output Size: {metrics['output_size_chars']} chars ({metrics['output_size_kb']:.2f} KB)")

    if 'tokens_per_second' in metrics:
        print(f"Tokens Generated: {metrics.get('tokens_generated', 'N/A')}")
        print(f"Tokens/Second: {metrics.get('tokens_per_second', 'N/A')}")

    print(f"Success: {metrics['success']}")
    if metrics['error']:
        print(f"Error: {metrics['error']}")
    print("="*50 + "\n")


if __name__ == "__main__":
    with open("../UML-test/test1.xml", "r") as f:
        uml_xmi = f.read()

    print("Generating ontology with Mixtral...")
    ontology_ttl, metrics = generate_ontology_with_mixtral(
        uml_xmi,
        model="mixtral:latest",
        benchmark=True
    )

    print_metrics(metrics)

    if ontology_ttl:
        with open("../benchmark/mixtral_ontology.ttl", "w") as f:
            f.write(ontology_ttl)
        print("Ontology saved to ../benchmark/mixtral_ontology.ttl")

    save_benchmark_results(metrics, "../benchmark/mixtral_benchmark.json")

"""
GPT-4 Model integration for direct UML to ontology generation.
Uses OpenAI API for benchmarking purposes.

Author: Helmut Cespedes
"""

import json
import time
from datetime import datetime
from typing import Tuple, Union
import openai
import os


def generate_ontology_with_gpt4(uml: str, model: str = "gpt-4", api_key: str = None, benchmark: bool = True) -> Union[str, Tuple[str, dict]]:
    """
    Generate an OWL ontology directly from UML XMI using GPT-4.

    Args:
        uml (str): The UML diagram in XMI format.
        model (str): The GPT model to use (default: "gpt-4").
        api_key (str): OpenAI API key (if None, uses OPENAI_API_KEY env var).
        benchmark (bool): Whether to collect benchmarking metrics (default: True).

    Returns:
        tuple: (ontology_content, metrics_dict) if benchmark=True, else just ontology_content
    """

    if api_key:
        openai.api_key = api_key
    elif os.getenv("OPENAI_API_KEY"):
        openai.api_key = os.getenv("OPENAI_API_KEY")
    else:
        raise ValueError("No OpenAI API key provided. Set OPENAI_API_KEY environment variable or pass api_key parameter.")

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

        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert ontology engineer specialized in converting UML to OWL."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        end_time = time.time()

        ontology_content = response.choices[0].message.content.strip()

        if benchmark:
            metrics.update({
                "generation_time_seconds": round(end_time - start_time, 3),
                "output_size_chars": len(ontology_content),
                "output_size_kb": len(ontology_content.encode('utf-8')) / 1024,
                "success": True,
                "error": None,
                "tokens_prompt": response.usage.prompt_tokens,
                "tokens_completion": response.usage.completion_tokens,
                "tokens_total": response.usage.total_tokens,
            })

            return ontology_content, metrics
        else:
            return ontology_content

    except Exception as e:
        error_msg = f"Error generating ontology with GPT-4: {e}"
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
    print("BENCHMARK RESULTS - GPT-4")
    print("="*50)
    print(f"Model: {metrics['model']}")
    print(f"Timestamp: {metrics['timestamp']}")
    print(f"Input Size: {metrics['input_size_chars']} chars ({metrics['input_size_kb']:.2f} KB)")
    print(f"Generation Time: {metrics['generation_time_seconds']} seconds")
    print(f"Output Size: {metrics['output_size_chars']} chars ({metrics['output_size_kb']:.2f} KB)")

    if 'tokens_total' in metrics:
        print(f"Tokens (Prompt): {metrics.get('tokens_prompt', 'N/A')}")
        print(f"Tokens (Completion): {metrics.get('tokens_completion', 'N/A')}")
        print(f"Tokens (Total): {metrics.get('tokens_total', 'N/A')}")

    print(f"Success: {metrics['success']}")
    if metrics.get('error'):
        print(f"Error: {metrics['error']}")
    print("="*50 + "\n")


if __name__ == "__main__":
    with open("../UML-test/test1.xml", "r") as f:
        uml_xmi = f.read()

    print("Generating ontology with GPT-4...")
    ontology_ttl, metrics = generate_ontology_with_gpt4(
        uml_xmi,
        model="gpt-4",
        benchmark=True
    )

    print_metrics(metrics)

    if ontology_ttl:
        with open("../benchmark/gpt4_ontology.ttl", "w") as f:
            f.write(ontology_ttl)
        print("Ontology saved to ../benchmark/gpt4_ontology.ttl")

    save_benchmark_results(metrics, "../benchmark/gpt4_benchmark.json")

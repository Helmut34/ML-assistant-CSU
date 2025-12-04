from ollamaTest import (
    generate_ontology_with_ollama_v2,
    save_benchmark_results,
    print_metrics
)
import os

if __name__ == "__main__":
    benchmark_dir = "../benchmark"

    print("Reading UML XMI file...")
    with open("../UML-test/test1.xml", "r") as f:
        uml_xmi = f.read()

    print(f"Loaded {len(uml_xmi)} characters from test1.xml")

    print("\n" + "="*60)
    print("RUNNING V2 PIPELINE: UML → Code → Taxonomy → Ontology")
    print("="*60 + "\n")

    print("Generating ontology with Ollama V2 Pipeline...")
    uml_code, taxonomy, ontology_ttl, metrics = generate_ontology_with_ollama_v2(
        uml_xmi,
        model="llama3.1:8b",
        benchmark=True
    )

    print_metrics(metrics)

    # Save intermediate UML code
    uml_code_path = os.path.join(benchmark_dir, "v2_uml_code.txt")
    if uml_code:
        with open(uml_code_path, "w") as f:
            f.write(uml_code)
        print(f"UML code saved to {uml_code_path}")
    else:
        print("No UML code generated")

    # Save intermediate taxonomy
    taxonomy_path = os.path.join(benchmark_dir, "v2_taxonomy.txt")
    if taxonomy:
        with open(taxonomy_path, "w") as f:
            f.write(taxonomy)
        print(f"Taxonomy saved to {taxonomy_path}")
    else:
        print("No taxonomy generated")

    # Save final ontology
    ontology_path = os.path.join(benchmark_dir, "v2_generated_ontology.ttl")
    if ontology_ttl:
        with open(ontology_path, "w") as f:
            f.write(ontology_ttl)
        print(f"Ontology saved to {ontology_path}")
    else:
        print("No ontology generated")

    # Save benchmark results
    benchmark_results_path = os.path.join(benchmark_dir, "v2_benchmark_results.json")
    save_benchmark_results(metrics, benchmark_results_path)

    print("\n" + "="*60)
    print("V2 Pipeline Complete!")
    print("="*60)

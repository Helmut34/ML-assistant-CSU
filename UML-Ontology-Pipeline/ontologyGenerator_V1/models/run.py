from ollamaTest import (
    generate_ontology_with_ollama, 
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
    
    print("Generating ontology with Ollama...")
    ontology_ttl, metrics = generate_ontology_with_ollama(
        uml_xmi, 
        model="llama3.1:8b",
        benchmark=True
    )
    
    print_metrics(metrics)
    
    ontology_path = os.path.join(benchmark_dir, "generated_ontology.ttl")
    if ontology_ttl:
        with open(ontology_path, "w") as f:
            f.write(ontology_ttl)
        print(f"Ontology saved to {ontology_path}")
    else:
        print("No ontology generated")
    
    benchmark_results_path = os.path.join(benchmark_dir, "benchmark_results.json")
    save_benchmark_results(metrics, benchmark_results_path)
    
    print("\nDone!")
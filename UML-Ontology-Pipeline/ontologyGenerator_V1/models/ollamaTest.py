"""
Ollama Model integration for ontology generation with benchmarking.
Optimized version with improved error handling, type hints, and performance.

Author: Helmut Cespedes (optimized)
"""

import json
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple, Union
import ollama


@dataclass
class BenchmarkMetrics:
    """Data class for benchmark metrics with automatic serialization."""
    model: str
    timestamp: str
    input_size_chars: int
    input_size_kb: float
    generation_time_seconds: float
    output_size_chars: int
    output_size_kb: float
    success: bool
    error: Optional[str] = None
    tokens_generated: Optional[int] = None
    tokens_per_second: Optional[float] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary, excluding None values."""
        return {k: v for k, v in asdict(self).items() if v is not None}


class OntologyGenerator:
    """Handler for UML to OWL ontology conversion using Ollama."""
    
    DEFAULT_MODEL = "llama3.1:8b"
    PROMPT_TEMPLATE = """You are an expert in converting UML diagrams into OWL ontologies.
Given the following UML diagram in XMI format, generate a corresponding OWL ontology in Turtle format.

Requirements:
1. Use proper OWL/RDFS namespaces (owl:, rdfs:, rdf:)
2. Convert classes with owl:Class
3. Preserve inheritance relationships with rdfs:subClassOf
4. Define properties as owl:DatatypeProperty or owl:ObjectProperty
5. Include cardinality constraints using owl:Restriction
6. Maintain all associations and their multiplicities

UML XMI:
{uml}

Respond ONLY with the OWL ontology in Turtle format, without explanations."""

    def __init__(self, model: str = DEFAULT_MODEL):
        """
        Initialize the ontology generator.
        
        Args:
            model: The Ollama model to use for generation.
        """
        self.model = model
    
    @staticmethod
    def _calculate_size(content: str) -> Tuple[int, float]:
        """Calculate character count and KB size of content."""
        char_count = len(content)
        kb_size = len(content.encode('utf-8')) / 1024
        return char_count, kb_size
    
    def _create_prompt(self, uml: str) -> str:
        """Create the prompt for ontology generation."""
        return self.PROMPT_TEMPLATE.format(uml=uml)
    
    def _extract_metrics(
        self, 
        uml: str, 
        ontology: str, 
        duration: float, 
        response: dict,
        error: Optional[str] = None
    ) -> BenchmarkMetrics:
        """Extract and calculate benchmark metrics."""
        input_chars, input_kb = self._calculate_size(uml)
        output_chars, output_kb = self._calculate_size(ontology)
        
        # Extract token information if available
        tokens = response.get('eval_count') if response else None
        tokens_per_sec = round(tokens / duration, 2) if tokens and duration > 0 else None
        
        return BenchmarkMetrics(
            model=self.model,
            timestamp=datetime.now().isoformat(),
            input_size_chars=input_chars,
            input_size_kb=round(input_kb, 3),
            generation_time_seconds=round(duration, 3),
            output_size_chars=output_chars,
            output_size_kb=round(output_kb, 3),
            success=error is None,
            error=error,
            tokens_generated=tokens,
            tokens_per_second=tokens_per_sec
        )
    
    def generate(
        self, 
        uml: str, 
        benchmark: bool = True
    ) -> Union[str, Tuple[str, BenchmarkMetrics]]:
        """
        Generate an OWL ontology from UML XMI using Ollama.
        
        Args:
            uml: The UML diagram in XMI format.
            benchmark: Whether to collect and return benchmarking metrics.
            
        Returns:
            If benchmark=True: tuple of (ontology_content, metrics)
            If benchmark=False: just ontology_content
            
        Raises:
            ValueError: If UML input is empty.
            RuntimeError: If Ollama API call fails.
        """
        if not uml or not uml.strip():
            raise ValueError("UML input cannot be empty")
        
        prompt = self._create_prompt(uml)
        start_time = time.perf_counter()  # More precise than time.time()
        ontology_content = ""
        response_data = None
        error_msg = None
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            
            ontology_content = response['message']['content'].strip()
            response_data = response
            
        except KeyError as e:
            error_msg = f"Unexpected response format from Ollama: {e}"
            raise RuntimeError(error_msg) from e
        except Exception as e:
            error_msg = f"Ollama API error: {type(e).__name__}: {e}"
            raise RuntimeError(error_msg) from e
        finally:
            duration = time.perf_counter() - start_time
            
            if benchmark:
                metrics = self._extract_metrics(
                    uml, ontology_content, duration, response_data, error_msg
                )
                return ontology_content, metrics
        
        return ontology_content


class BenchmarkLogger:
    """Handler for saving and displaying benchmark results."""
    
    def __init__(self, output_file: Union[str, Path] = "benchmark_results.json"):
        """
        Initialize the benchmark logger.
        
        Args:
            output_file: Path to the JSON file for storing results.
        """
        self.output_file = Path(output_file)
    
    def save(self, metrics: BenchmarkMetrics) -> None:
        """
        Save benchmark metrics to JSON file (append mode).
        
        Args:
            metrics: The metrics to save.
            
        Raises:
            IOError: If file operations fail.
        """
        try:
            # Load existing results or create new list
            results = []
            if self.output_file.exists():
                with open(self.output_file, 'r', encoding='utf-8') as f:
                    results = json.load(f)
            
            # Append new metrics
            results.append(metrics.to_dict())
            
            # Write back to file with atomic operation
            temp_file = self.output_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            temp_file.replace(self.output_file)
            print(f"✓ Benchmark results saved to {self.output_file}")
            
        except Exception as e:
            raise IOError(f"Failed to save benchmark results: {e}") from e
    
    @staticmethod
    def print_metrics(metrics: BenchmarkMetrics) -> None:
        """
        Pretty print benchmark metrics to console.
        
        Args:
            metrics: The metrics to display.
        """
        separator = "=" * 60
        print(f"\n{separator}")
        print("BENCHMARK RESULTS".center(60))
        print(separator)
        print(f"Model:            {metrics.model}")
        print(f"Timestamp:        {metrics.timestamp}")
        print(f"Status:           {'✓ Success' if metrics.success else '✗ Failed'}")
        print(separator)
        print(f"Input Size:       {metrics.input_size_chars:,} chars ({metrics.input_size_kb:.2f} KB)")
        print(f"Output Size:      {metrics.output_size_chars:,} chars ({metrics.output_size_kb:.2f} KB)")
        print(f"Generation Time:  {metrics.generation_time_seconds:.3f} seconds")
        
        if metrics.tokens_generated:
            print(f"Tokens Generated: {metrics.tokens_generated:,}")
        if metrics.tokens_per_second:
            print(f"Tokens/Second:    {metrics.tokens_per_second:.2f}")
        
        if metrics.error:
            print(separator)
            print(f"Error:            {metrics.error}")
        
        print(separator + "\n")


# Convenience functions for backward compatibility
def generate_ontology_with_ollama(
    uml: str, 
    model: str = "llama3.1:8b", 
    benchmark: bool = True
) -> Union[str, Tuple[str, dict]]:
    """
    Legacy function for backward compatibility.
    Generate an OWL ontology from UML XMI using Ollama.
    
    Args:
        uml: The UML diagram in XMI format.
        model: The Ollama model to use.
        benchmark: Whether to return benchmarking metrics.
        
    Returns:
        If benchmark=True: tuple of (ontology_content, metrics_dict)
        If benchmark=False: just ontology_content
    """
    generator = OntologyGenerator(model=model)
    result = generator.generate(uml, benchmark=benchmark)
    
    if benchmark:
        ontology, metrics = result
        return ontology, metrics.to_dict()
    return result


def save_benchmark_results(metrics: dict, output_file: str = "benchmark_results.json") -> None:
    """
    Legacy function for backward compatibility.
    Save benchmark metrics to a JSON file.
    
    Args:
        metrics: The metrics dictionary to save.
        output_file: Path to the output JSON file.
    """
    logger = BenchmarkLogger(output_file)
    # Convert dict to BenchmarkMetrics if needed
    if isinstance(metrics, dict):
        metrics_obj = BenchmarkMetrics(**metrics)
    else:
        metrics_obj = metrics
    logger.save(metrics_obj)


def print_metrics(metrics: dict) -> None:
    """
    Legacy function for backward compatibility.
    Pretty print benchmark metrics.
    
    Args:
        metrics: The metrics dictionary to print.
    """
    if isinstance(metrics, dict):
        metrics_obj = BenchmarkMetrics(**metrics)
    else:
        metrics_obj = metrics
    BenchmarkLogger.print_metrics(metrics_obj)


# Example usage
if __name__ == "__main__":
    # Example UML XMI content
    sample_uml = "UML-test/test1.xml"
    
    # Modern API
    generator = OntologyGenerator(model="llama3.1:8b")
    logger = BenchmarkLogger()
    
    try:
        ontology, metrics = generator.generate(sample_uml, benchmark=True)
        logger.print_metrics(metrics)
        logger.save(metrics)
        print("Generated ontology:")
        print(ontology[:500] + "..." if len(ontology) > 500 else ontology)
    except Exception as e:
        print(f"Error: {e}")
"""
Command-line interface for GLMReasoner.
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Optional, List

from .reasoner import GLMReasoner, Document, Query, ReasoningStrategy, DocumentType
from .config import Config


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="glmreasoner",
        description="GLMReasoner - Long Context Cross-Document Intelligent Reasoning Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with API key
  glmreasoner --api-key YOUR_KEY "What is the main topic?" doc1.md doc2.txt
  
  # Using chain of thought reasoning
  glmreasoner --strategy cot "Explain the relationship" report.pdf
  
  # Batch query from file
  glmreasoner --queries questions.json corpus/
  
  # Save results to file
  glmreasoner --output results.json doc.md "Your question"
  
Environment variables:
  GLM_API_KEY      Your GLM API key
  GLM_API_BASE     API base URL (default: https://open.bigmodel.cn/api/paas/v4)
  GLM_MODEL        Model name (default: glm-5-plus)
  GLM_TEMPERATURE  Default temperature (default: 0.7)
        """
    )
    
    # Main arguments
    parser.add_argument(
        "question",
        nargs="?",
        help="The question to answer"
    )
    parser.add_argument(
        "documents",
        nargs="*",
        help="Document files to analyze"
    )
    
    # API configuration
    api_group = parser.add_argument_group("API Configuration")
    api_group.add_argument(
        "--api-key", "-k",
        help="GLM API key (or set GLM_API_KEY env var)"
    )
    api_group.add_argument(
        "--api-base",
        help="API base URL"
    )
    api_group.add_argument(
        "--model", "-m",
        default="glm-5-plus",
        help="Model to use (default: glm-5-plus)"
    )
    
    # Reasoning configuration
    reason_group = parser.add_argument_group("Reasoning Configuration")
    reason_group.add_argument(
        "--strategy", "-s",
        choices=["direct", "cot", "tot", "self-ask", "hybrid"],
        default="hybrid",
        help="Reasoning strategy (default: hybrid)"
    )
    reason_group.add_argument(
        "--temperature", "-t",
        type=float,
        default=0.7,
        help="Sampling temperature (default: 0.7)"
    )
    reason_group.add_argument(
        "--max-tokens",
        type=int,
        default=4096,
        help="Maximum tokens in response (default: 4096)"
    )
    
    # Input/Output
    io_group = parser.add_argument_group("Input/Output")
    io_group.add_argument(
        "--output", "-o",
        help="Output file for results (JSON format)"
    )
    io_group.add_argument(
        "--format", "-f",
        choices=["text", "json", "markdown"],
        default="text",
        help="Output format (default: text)"
    )
    io_group.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress informational output"
    )
    
    # Batch processing
    batch_group = parser.add_argument_group("Batch Processing")
    batch_group.add_argument(
        "--queries",
        help="JSON file with batch queries"
    )
    batch_group.add_argument(
        "--parallel",
        action="store_true",
        help="Process queries in parallel"
    )
    
    # Utility
    util_group = parser.add_argument_group("Utility")
    util_group.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    util_group.add_argument(
        "--stats",
        action="store_true",
        help="Show usage statistics"
    )
    
    return parser


def load_documents(paths: List[str]) -> List[Document]:
    """Load documents from file paths."""
    documents = []
    
    for path_str in paths:
        path = Path(path_str)
        
        if not path.exists():
            print(f"Warning: File not found: {path_str}", file=sys.stderr)
            continue
        
        if path.is_dir():
            # Load all supported files from directory
            for ext in [".txt", ".md", ".json", ".csv", ".html", ".pdf"]:
                for file_path in path.rglob(f"*{ext}"):
                    try:
                        doc = Document.from_file(str(file_path))
                        documents.append(doc)
                    except Exception as e:
                        print(f"Warning: Failed to load {file_path}: {e}", file=sys.stderr)
        else:
            # Load single file
            try:
                doc = Document.from_file(str(path))
                documents.append(doc)
            except Exception as e:
                print(f"Warning: Failed to load {path_str}: {e}", file=sys.stderr)
    
    return documents


def load_batch_queries(file_path: str) -> List[Query]:
    """Load queries from JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    queries = []
    if isinstance(data, list):
        for item in data:
            if isinstance(item, str):
                queries.append(Query(question=item))
            elif isinstance(item, dict):
                queries.append(Query(**item))
    elif isinstance(data, dict) and "queries" in data:
        for item in data["queries"]:
            if isinstance(item, str):
                queries.append(Query(question=item))
            elif isinstance(item, dict):
                queries.append(Query(**item))
    
    return queries


def format_result_text(result, verbose: bool = False) -> str:
    """Format result as readable text."""
    lines = []
    lines.append("=" * 60)
    lines.append("REASONING RESULT")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"Model: {result.model}")
    lines.append(f"Strategy: {result.strategy.value}")
    lines.append(f"Confidence: {result.confidence:.2%}")
    lines.append(f"Tokens Used: {result.tokens_used}")
    lines.append(f"Latency: {result.latency_ms:.0f}ms")
    lines.append("")
    
    if verbose and result.reasoning:
        lines.append("REASONING PROCESS:")
        lines.append("-" * 40)
        lines.append(result.reasoning)
        lines.append("")
    
    lines.append("ANSWER:")
    lines.append("-" * 40)
    lines.append(result.answer)
    lines.append("")
    
    lines.append("SOURCES:")
    lines.append("-" * 40)
    for source in result.sources:
        lines.append(f"  • {source}")
    
    return "\n".join(lines)


def format_result_json(result) -> str:
    """Format result as JSON."""
    return result.to_json()


def format_result_markdown(result) -> str:
    """Format result as Markdown."""
    lines = []
    lines.append("# Reasoning Result")
    lines.append("")
    lines.append("## Metadata")
    lines.append(f"- **Model**: {result.model}")
    lines.append(f"- **Strategy**: {result.strategy.value}")
    lines.append(f"- **Confidence**: {result.confidence:.2%}")
    lines.append(f"- **Tokens Used**: {result.tokens_used}")
    lines.append(f"- **Latency**: {result.latency_ms:.0f}ms")
    lines.append("")
    
    if result.reasoning:
        lines.append("## Reasoning Process")
        lines.append(result.reasoning)
        lines.append("")
    
    lines.append("## Answer")
    lines.append(result.answer)
    lines.append("")
    
    lines.append("## Sources")
    for source in result.sources:
        lines.append(f"- {source}")
    
    return "\n".join(lines)


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Check for API key
    api_key = args.api_key
    if not api_key:
        import os
        api_key = os.environ.get("GLM_API_KEY")
    
    if not api_key:
        parser.error("API key required. Set GLM_API_KEY env var or use --api-key")
        return 1
    
    # Handle version flag
    if args.version:
        print(f"GLMReasoner 1.0.0")
        return 0
    
    # Load documents
    documents = []
    if args.documents:
        documents = load_documents(args.documents)
        if not documents:
            print("Error: No valid documents loaded", file=sys.stderr)
            return 1
    
    # Load queries
    queries = []
    if args.queries:
        try:
            queries = load_batch_queries(args.queries)
        except Exception as e:
            print(f"Error loading queries: {e}", file=sys.stderr)
            return 1
    elif args.question:
        # Map strategy string to enum
        strategy_map = {
            "direct": ReasoningStrategy.DIRECT,
            "cot": ReasoningStrategy.CHAIN_OF_THOUGHT,
            "tot": ReasoningStrategy.TREE_OF_THOUGHT,
            "self-ask": ReasoningStrategy.SELF_ASK,
            "hybrid": ReasoningStrategy.HYBRID,
        }
        queries = [
            Query(
                question=args.question,
                strategy=strategy_map.get(args.strategy, ReasoningStrategy.HYBRID),
                temperature=args.temperature,
                max_tokens=args.max_tokens,
            )
        ]
    
    if not queries:
        parser.print_help()
        return 0
    
    # Initialize reasoner
    try:
        reasoner = GLMReasoner(
            api_key=api_key,
            api_base=args.api_base,
            model=args.model,
        )
    except Exception as e:
        print(f"Error initializing reasoner: {e}", file=sys.stderr)
        return 1
    
    # Process queries
    try:
        if not documents:
            # Create a simple text document from the question context
            if not args.question:
                print("Error: Question is required", file=sys.stderr)
                return 1
            documents = [
                Document(
                    content="This is the context for the query.",
                    source="cli-input"
                )
            ]
        
        results = []
        for query in queries:
            if not args.quiet:
                print(f"Processing: {query.question[:50]}...")
            
            result = reasoner.reason(documents, query)
            results.append(result)
        
        # Format output
        formatter_map = {
            "text": format_result_text,
            "json": format_result_json,
            "markdown": format_result_markdown,
        }
        formatter = formatter_map.get(args.format, format_result_text)
        
        # Output results
        if len(results) == 1:
            output = formatter(results[0], verbose=True)
        else:
            outputs = [formatter(r, verbose=False) for r in results]
            if args.format == "json":
                output = json.dumps([r.to_dict() for r in results], indent=2, ensure_ascii=False)
            else:
                output = "\n\n".join(outputs)
        
        # Save or print
        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
            if not args.quiet:
                print(f"Results saved to {args.output}")
        else:
            print(output)
        
        # Show stats
        if args.stats:
            stats = reasoner.stats
            print("\nUsage Statistics:")
            print(f"  Total Requests: {stats['total_requests']}")
            print(f"  Total Tokens: {stats['total_tokens']}")
            print(f"  Avg Latency: {stats['avg_latency_ms']:.0f}ms")
            print(f"  Success Rate: {stats['success_rate']:.1f}%")
        
        return 0
        
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    finally:
        reasoner.close()


if __name__ == "__main__":
    sys.exit(main())

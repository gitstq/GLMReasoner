"""
Examples for GLMReasoner
"""

from GLMReasoner.src.reasoner import GLMReasoner, Document, Query, ReasoningStrategy


def example_basic():
    """Basic usage example."""
    # Initialize the reasoner
    reasoner = GLMReasoner(api_key="your-api-key-here")
    
    # Create a document
    doc = Document(
        content="""
        # Research Summary
        
        This study investigates the effects of artificial intelligence on modern software development.
        Key findings include:
        
        1. AI tools increase developer productivity by 40%
        2. Code review time reduced by 60%
        3. Bug detection accuracy improved to 95%
        
        The study was conducted over 12 months with 500 participants.
        """,
        source="research_summary.md"
    )
    
    # Create a query
    query = Query(
        question="What are the key findings from this research?",
        strategy=ReasoningStrategy.HYBRID
    )
    
    # Execute reasoning
    result = reasoner.reason([doc], query)
    
    print(f"Answer: {result.answer}")
    print(f"Confidence: {result.confidence:.2%}")
    print(f"Tokens used: {result.tokens_used}")
    
    reasoner.close()


def example_cross_document():
    """Cross-document analysis example."""
    reasoner = GLMReasoner(api_key="your-api-key-here")
    
    # Load multiple documents
    docs = [
        Document(
            content="Q1 Report: Revenue grew 20% YoY.",
            source="q1_report.txt"
        ),
        Document(
            content="Q2 Report: Revenue grew 25% YoY with new product launch.",
            source="q2_report.txt"
        ),
        Document(
            content="Annual Review: Total revenue growth of 45% for the fiscal year.",
            source="annual_review.txt"
        ),
    ]
    
    # Create query for cross-document analysis
    query = Query(
        question="Summarize the revenue trends across all reports.",
        strategy=ReasoningStrategy.HYBRID
    )
    
    result = reasoner.reason(docs, query)
    
    print(f"Answer: {result.answer}")
    print(f"Sources: {result.sources}")
    
    reasoner.close()


def example_batch_queries():
    """Batch processing example."""
    reasoner = GLMReasoner(api_key="your-api-key-here")
    
    doc = Document(
        content="""
        Technical documentation for the API.
        
        Endpoints:
        - GET /users - List all users
        - POST /users - Create new user
        - GET /users/{id} - Get user by ID
        - PUT /users/{id} - Update user
        - DELETE /users/{id} - Delete user
        
        Authentication: Bearer token required.
        """,
        source="api_docs.md"
    )
    
    # Multiple queries
    queries = [
        Query(question="What endpoints are available?", strategy=ReasoningStrategy.DIRECT),
        Query(question="How do I authenticate?", strategy=ReasoningStrategy.DIRECT),
        Query(question="How do I create a user?", strategy=ReasoningStrategy.CHAIN_OF_THOUGHT),
    ]
    
    results = reasoner.reason_batch([doc], queries)
    
    for i, result in enumerate(results):
        print(f"Query {i+1}: {queries[i].question}")
        print(f"Answer: {result.answer}\n")
    
    reasoner.close()


if __name__ == "__main__":
    print("Basic Example:")
    print("-" * 40)
    # example_basic()
    print("Run with: python -m GLMReasoner.src.examples")
    print("\nNote: Set GLM_API_KEY environment variable before running.")

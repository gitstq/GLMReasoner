"""
GLMReasoner - Long Context Cross-Document Intelligent Reasoning Engine

This module provides the core functionality for cross-document reasoning
using GLM-5.1's 128K context window.
"""

import json
import hashlib
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any, Union
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None


class DocumentType(Enum):
    """Supported document types."""
    TEXT = "text"
    MARKDOWN = "markdown"
    JSON = "json"
    CSV = "csv"
    PDF = "pdf"
    HTML = "html"
    UNKNOWN = "unknown"


class ReasoningStrategy(Enum):
    """Available reasoning strategies."""
    DIRECT = "direct"
    CHAIN_OF_THOUGHT = "chain_of_thought"
    TREE_OF_THOUGHT = "tree_of_thought"
    SELF_ASK = "self_ask"
    HYBRID = "hybrid"


@dataclass
class Document:
    """Represents a document for reasoning."""
    content: str
    source: str
    doc_type: DocumentType = DocumentType.TEXT
    metadata: Dict[str, Any] = field(default_factory=dict)
    chunk_id: Optional[str] = None
    
    def __post_init__(self):
        """Initialize computed fields."""
        if not self.chunk_id:
            self.chunk_id = self._generate_chunk_id()
        if not self.metadata.get("created_at"):
            self.metadata["created_at"] = datetime.now().isoformat()
    
    def _generate_chunk_id(self) -> str:
        """Generate unique ID for this document chunk."""
        content_hash = hashlib.md5(self.content.encode()).hexdigest()[:12]
        return f"doc_{content_hash}_{len(self.content)}"
    
    @property
    def word_count(self) -> int:
        """Get word count of the document."""
        return len(self.content.split())
    
    @property
    def char_count(self) -> int:
        """Get character count of the document."""
        return len(self.content)
    
    @classmethod
    def from_file(cls, file_path: str, doc_type: Optional[DocumentType] = None) -> "Document":
        """Create Document from file."""
        path = Path(file_path)
        
        # Auto-detect type from extension
        if doc_type is None:
            ext_map = {
                ".txt": DocumentType.TEXT,
                ".md": DocumentType.MARKDOWN,
                ".json": DocumentType.JSON,
                ".csv": DocumentType.CSV,
                ".pdf": DocumentType.PDF,
                ".html": DocumentType.HTML,
                ".htm": DocumentType.HTML,
            }
            doc_type = ext_map.get(path.suffix.lower(), DocumentType.UNKNOWN)
        
        content = path.read_text(encoding="utf-8")
        return cls(content=content, source=str(path), doc_type=doc_type)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "content": self.content,
            "source": self.source,
            "doc_type": self.doc_type.value,
            "metadata": self.metadata,
            "chunk_id": self.chunk_id,
        }


@dataclass
class Query:
    """Represents a reasoning query."""
    question: str
    context: Optional[str] = None
    strategy: ReasoningStrategy = ReasoningStrategy.HYBRID
    max_tokens: int = 4096
    temperature: float = 0.7
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize computed fields."""
        if not self.metadata.get("created_at"):
            self.metadata["created_at"] = datetime.now().isoformat()
    
    def build_prompt(self, documents: List[Document]) -> str:
        """Build the full prompt with documents."""
        strategy_prompts = {
            ReasoningStrategy.DIRECT: self._direct_prompt,
            ReasoningStrategy.CHAIN_OF_THOUGHT: self._cot_prompt,
            ReasoningStrategy.TREE_OF_THOUGHT: self._tot_prompt,
            ReasoningStrategy.SELF_ASK: self._self_ask_prompt,
            ReasoningStrategy.HYBRID: self._hybrid_prompt,
        }
        prompt_builder = strategy_prompts[self.strategy]
        return prompt_builder(documents)
    
    def _direct_prompt(self, documents: List[Document]) -> str:
        """Direct answer prompt."""
        docs_section = self._format_documents(documents)
        return f"""Based on the following documents, answer the question.

## Documents:
{docs_section}

## Question:
{self.question}

## Answer:"""
    
    def _cot_prompt(self, documents: List[Document]) -> str:
        """Chain of Thought prompt."""
        docs_section = self._format_documents(documents)
        return f"""Based on the following documents, answer the question step by step.

## Documents:
{docs_section}

## Question:
{self.question}

## Reasoning:
Let me analyze this step by step:

1. First, I need to identify the key information related to this question.
2. Then, I will cross-reference information across the documents.
3. Finally, I will synthesize the findings to provide a comprehensive answer.

"""
    
    def _tot_prompt(self, documents: List[Document]) -> str:
        """Tree of Thought prompt."""
        docs_section = self._format_documents(documents)
        return f"""Based on the following documents, explore multiple reasoning paths to answer the question.

## Documents:
{docs_section}

## Question:
{self.question}

## Reasoning Paths:

### Path A: Direct Evidence
[Explore the most straightforward interpretation]

### Path B: Alternative Interpretation  
[Consider alternative meanings or contexts]

### Path C: Cross-Document Synthesis
[Combine information from multiple sources]

Please evaluate each path and determine the most accurate answer.
"""
    
    def _self_ask_prompt(self, documents: List[Document]) -> str:
        """Self-Ask prompt."""
        docs_section = self._format_documents(documents)
        return f"""Based on the following documents, answer the question by asking follow-up questions.

## Documents:
{docs_section}

## Question:
{self.question}

## Self-Questioning Process:

Let me break this down:
- What is the core question being asked?
- What information do I need to answer this?
- What information is available in the documents?
- What is the answer?

"""
    
    def _hybrid_prompt(self, documents: List[Document]) -> str:
        """Hybrid reasoning prompt combining multiple strategies."""
        docs_section = self._format_documents(documents)
        return f"""Based on the following documents, perform cross-document reasoning to answer the question.

## Documents:
{docs_section}

## Question:
{self.question}

## Analysis Process:

### 1. Information Extraction
Extract relevant facts from each document:

### 2. Cross-Reference
Identify relationships and conflicts between documents:

### 3. Synthesis
Combine information to form a complete answer:

### 4. Verification
Verify the answer against the source documents:

## Final Answer:
"""
    
    def _format_documents(self, documents: List[Document]) -> str:
        """Format documents for the prompt."""
        formatted = []
        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get("title", doc.source)
            formatted.append(f"### Document {i}: {source}\n{doc.content[:5000]}")
            if len(doc.content) > 5000:
                formatted.append(f"... (truncated, total {len(doc)} characters)")
        return "\n\n".join(formatted)


@dataclass
class ReasoningResult:
    """Contains the result of reasoning."""
    answer: str
    reasoning: str
    confidence: float
    sources: List[str]
    tokens_used: int
    latency_ms: float
    model: str
    strategy: ReasoningStrategy
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "answer": self.answer,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
            "sources": self.sources,
            "tokens_used": self.tokens_used,
            "latency_ms": self.latency_ms,
            "model": self.model,
            "strategy": self.strategy.value,
            "metadata": self.metadata,
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
    
    @property
    def success(self) -> bool:
        """Check if reasoning was successful."""
        return bool(self.answer and len(self.answer) > 0)


class GLMReasoner:
    """
    Long Context Cross-Document Intelligent Reasoning Engine.
    
    Leverages GLM-5.1's 128K context window to perform deep reasoning
    across multiple documents simultaneously.
    
    Example:
        >>> from GLMReasoner import GLMReasoner, Document, Query
        >>> reasoner = GLMReasoner(api_key="your-api-key")
        >>> doc = Document(content="...", source="report.pdf")
        >>> query = Query(question="What is the main finding?")
        >>> result = reasoner.reason([doc], query)
        >>> print(result.answer)
    """
    
    DEFAULT_API_BASE = "https://open.bigmodel.cn/api/paas/v4"
    DEFAULT_MODEL = "glm-5-plus"
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        model: Optional[str] = None,
        timeout: int = 120,
        max_retries: int = 3,
        **kwargs
    ):
        """
        Initialize the GLMReasoner.
        
        Args:
            api_key: GLM API key. Can also be set via GLM_API_KEY env variable.
            api_base: API base URL. Defaults to official GLM API.
            model: Model name. Defaults to glm-5-plus.
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retries on failure.
        """
        self.api_key = api_key or self._get_env_var("GLM_API_KEY")
        self.api_base = api_base or self._get_env_var("GLM_API_BASE", self.DEFAULT_API_BASE)
        self.model = model or self._get_env_var("GLM_MODEL", self.DEFAULT_MODEL)
        self.timeout = timeout
        self.max_retries = max_retries
        
        if not self.api_key:
            raise ValueError(
                "API key is required. Provide it via api_key parameter "
                "or GLM_API_KEY environment variable."
            )
        
        self._session = None
        self._stats = {
            "total_requests": 0,
            "total_tokens": 0,
            "total_latency_ms": 0,
            "failed_requests": 0,
        }
    
    @staticmethod
    def _get_env_var(key: str, default: Optional[str] = None) -> Optional[str]:
        """Get environment variable."""
        import os
        return os.environ.get(key, default)
    
    @property
    def stats(self) -> Dict[str, Any]:
        """Get usage statistics."""
        avg_latency = (
            self._stats["total_latency_ms"] / self._stats["total_requests"]
            if self._stats["total_requests"] > 0 else 0
        )
        return {
            **self._stats,
            "avg_latency_ms": avg_latency,
            "success_rate": (
                (self._stats["total_requests"] - self._stats["failed_requests"])
                / self._stats["total_requests"] * 100
                if self._stats["total_requests"] > 0 else 0
            ),
        }
    
    def reason(
        self,
        documents: List[Document],
        query: Query,
        stream: bool = False,
    ) -> ReasoningResult:
        """
        Perform cross-document reasoning.
        
        Args:
            documents: List of documents to reason about.
            query: The reasoning query.
            stream: Whether to stream the response.
            
        Returns:
            ReasoningResult containing the answer and metadata.
        """
        if not documents:
            raise ValueError("At least one document is required.")
        
        if not query.question.strip():
            raise ValueError("Query question cannot be empty.")
        
        # Build prompt
        prompt = query.build_prompt(documents)
        
        # Estimate token count (rough approximation)
        estimated_tokens = len(prompt) // 4
        
        # Track timing
        start_time = datetime.now()
        
        # Make API request
        response = self._make_request(prompt, query, stream)
        
        # Calculate latency
        latency_ms = (datetime.now() - start_time).total_seconds() * 1000
        
        # Parse response
        result = self._parse_response(response, query, documents, latency_ms)
        
        # Update stats
        self._stats["total_requests"] += 1
        self._stats["total_tokens"] += result.tokens_used
        self._stats["total_latency_ms"] += latency_ms
        
        return result
    
    def _make_request(
        self,
        prompt: str,
        query: Query,
        stream: bool = False,
    ) -> Dict[str, Any]:
        """Make API request to GLM."""
        if requests is None:
            raise ImportError(
                "The 'requests' library is required. "
                "Install it with: pip install requests"
            )
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": query.temperature,
            "max_tokens": query.max_tokens,
            "stream": stream,
        }
        
        url = f"{self.api_base}/chat/completions"
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=self.timeout,
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    from .exceptions import AuthenticationError
                    raise AuthenticationError("Invalid API key")
                elif response.status_code == 429:
                    from .exceptions import RateLimitError
                    raise RateLimitError("Rate limit exceeded. Please try again later.")
                else:
                    from .exceptions import APIError
                    raise APIError(f"API error: {response.status_code} - {response.text}")
                    
            except requests.exceptions.Timeout:
                if attempt == self.max_retries - 1:
                    from .exceptions import APIError
                    raise APIError(f"Request timed out after {self.max_retries} attempts")
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    from .exceptions import APIError
                    raise APIError(f"Request failed: {str(e)}")
        
        self._stats["failed_requests"] += 1
        from .exceptions import APIError
        raise APIError("Max retries exceeded")
    
    def _parse_response(
        self,
        response: Dict[str, Any],
        query: Query,
        documents: List[Document],
        latency_ms: float,
    ) -> ReasoningResult:
        """Parse API response into ReasoningResult."""
        try:
            choices = response.get("choices", [])
            if not choices:
                raise APIError("No response choices returned")
            
            message = choices[0].get("message", {})
            content = message.get("content", "")
            
            # Extract answer and reasoning
            answer, reasoning = self._extract_answer_reasoning(content, query.strategy)
            
            # Calculate confidence based on content length and structure
            confidence = self._calculate_confidence(answer, reasoning)
            
            # Get usage stats
            usage = response.get("usage", {})
            tokens_used = usage.get("total_tokens", len(content) // 4)
            
            # Get sources
            sources = [doc.source for doc in documents]
            
            return ReasoningResult(
                answer=answer,
                reasoning=reasoning,
                confidence=confidence,
                sources=sources,
                tokens_used=tokens_used,
                latency_ms=latency_ms,
                model=self.model,
                strategy=query.strategy,
                metadata={
                    "prompt_tokens": usage.get("prompt_tokens", 0),
                    "completion_tokens": usage.get("completion_tokens", 0),
                },
            )
            
        except (KeyError, IndexError) as e:
            from .exceptions import APIError
            raise APIError(f"Failed to parse response: {str(e)}")
    
    def _extract_answer_reasoning(
        self,
        content: str,
        strategy: ReasoningStrategy,
    ) -> tuple:
        """Extract answer and reasoning from response content."""
        # Simple heuristic: look for common patterns
        content_lower = content.lower()
        
        # Try to find the answer section
        answer_patterns = [
            r"(?:final answer|answer)[:\s]*(.+?)(?:\n\n|$)",
            r"(?:conclusion)[:\s]*(.+?)(?:\n\n|$)",
        ]
        
        reasoning = ""
        answer = content
        
        for pattern in answer_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                reasoning = content[:match.start()]
                answer = match.group(1).strip()
                break
        
        return answer, reasoning
    
    def _calculate_confidence(self, answer: str, reasoning: str) -> float:
        """Calculate confidence score based on response characteristics."""
        score = 0.5
        
        # Length-based scoring
        if len(answer) > 100:
            score += 0.1
        if len(reasoning) > 200:
            score += 0.1
        
        # Structure-based scoring
        if any(marker in answer for marker in ["1.", "2.", "3.", "- ", "* "]):
            score += 0.1
        
        # Completeness indicators
        if answer.strip().endswith((".", "!", "?")):
            score += 0.1
        
        return min(score, 1.0)
    
    def reason_batch(
        self,
        documents: List[Document],
        queries: List[Query],
        parallel: bool = True,
    ) -> List[ReasoningResult]:
        """
        Perform reasoning for multiple queries.
        
        Args:
            documents: List of documents.
            queries: List of queries to answer.
            parallel: Whether to process queries in parallel.
            
        Returns:
            List of ReasoningResults.
        """
        if parallel:
            # Note: In production, use asyncio or threading for true parallelism
            return [self.reason(documents, q) for q in queries]
        else:
            return [self.reason(documents, q) for q in queries]
    
    def close(self):
        """Close the session and cleanup resources."""
        if self._session:
            self._session.close()
            self._session = None

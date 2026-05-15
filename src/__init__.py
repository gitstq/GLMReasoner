"""
GLMReasoner - Long Context Cross-Document Intelligent Reasoning Engine
Based on GLM-5.1 model with 128K context support

@Author: gitstq
@License: MIT
@Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "gitstq"
__license__ = "MIT"

from .reasoner import GLMReasoner, Document, Query, ReasoningResult, ReasoningStrategy, DocumentType
from .config import Config, ProviderConfig
from .exceptions import (
    GLMReasonerError,
    AuthenticationError,
    APIError,
    RateLimitError,
    DocumentParseError,
)

__all__ = [
    "GLMReasoner",
    "Document",
    "Query",
    "ReasoningResult",
    "ReasoningStrategy",
    "DocumentType",
    "Config",
    "ProviderConfig",
    "GLMReasonerError",
    "AuthenticationError",
    "APIError",
    "RateLimitError",
    "DocumentParseError",
]

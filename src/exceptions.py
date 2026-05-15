"""
Custom exceptions for GLMReasoner.
"""


class GLMReasonerError(Exception):
    """Base exception for GLMReasoner."""
    pass


class AuthenticationError(GLMReasonerError):
    """Raised when authentication fails."""
    pass


class APIError(GLMReasonerError):
    """Raised when API request fails."""
    pass


class RateLimitError(APIError):
    """Raised when rate limit is exceeded."""
    pass


class DocumentParseError(GLMReasonerError):
    """Raised when document parsing fails."""
    pass


class ConfigurationError(GLMReasonerError):
    """Raised when configuration is invalid."""
    pass


class ValidationError(GLMReasonerError):
    """Raised when input validation fails."""
    pass

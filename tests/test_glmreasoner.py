"""
Tests for GLMReasoner
"""

import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from reasoner import (
    GLMReasoner,
    Document,
    Query,
    ReasoningStrategy,
    ReasoningResult,
    DocumentType,
)
from config import Config
from exceptions import (
    GLMReasonerError,
    AuthenticationError,
    APIError,
)


class TestDocument:
    """Tests for Document class."""
    
    def test_document_creation(self):
        """Test basic document creation."""
        doc = Document(
            content="This is a test document.",
            source="test.txt"
        )
        assert doc.content == "This is a test document."
        assert doc.source == "test.txt"
        assert doc.doc_type == DocumentType.TEXT
        assert doc.chunk_id is not None
    
    def test_document_word_count(self):
        """Test word count property."""
        doc = Document(content="Hello world test document", source="test.txt")
        assert doc.word_count == 4
    
    def test_document_char_count(self):
        """Test character count property."""
        doc = Document(content="Hello", source="test.txt")
        assert doc.char_count == 5
    
    def test_document_to_dict(self):
        """Test document serialization."""
        doc = Document(content="Test", source="test.txt")
        data = doc.to_dict()
        assert data["content"] == "Test"
        assert data["source"] == "test.txt"
        assert "chunk_id" in data


class TestQuery:
    """Tests for Query class."""
    
    def test_query_creation(self):
        """Test basic query creation."""
        query = Query(question="What is this?")
        assert query.question == "What is this?"
        assert query.strategy == ReasoningStrategy.HYBRID
    
    def test_query_with_strategy(self):
        """Test query with specific strategy."""
        query = Query(
            question="Explain this",
            strategy=ReasoningStrategy.CHAIN_OF_THOUGHT
        )
        assert query.strategy == ReasoningStrategy.CHAIN_OF_THOUGHT
    
    def test_build_direct_prompt(self):
        """Test direct reasoning prompt building."""
        doc = Document(content="Test content", source="test.txt")
        query = Query(
            question="What is the content?",
            strategy=ReasoningStrategy.DIRECT
        )
        prompt = query.build_prompt([doc])
        assert "What is the content?" in prompt
        assert "Test content" in prompt
    
    def test_build_cot_prompt(self):
        """Test chain of thought prompt building."""
        doc = Document(content="Test content", source="test.txt")
        query = Query(
            question="Analyze this",
            strategy=ReasoningStrategy.CHAIN_OF_THOUGHT
        )
        prompt = query.build_prompt([doc])
        assert "step by step" in prompt.lower() or "analyze" in prompt.lower()


class TestReasoningStrategy:
    """Tests for ReasoningStrategy enum."""
    
    def test_all_strategies_exist(self):
        """Test that all strategies are defined."""
        assert ReasoningStrategy.DIRECT is not None
        assert ReasoningStrategy.CHAIN_OF_THOUGHT is not None
        assert ReasoningStrategy.TREE_OF_THOUGHT is not None
        assert ReasoningStrategy.SELF_ASK is not None
        assert ReasoningStrategy.HYBRID is not None


class TestReasoningResult:
    """Tests for ReasoningResult class."""
    
    def test_result_creation(self):
        """Test basic result creation."""
        result = ReasoningResult(
            answer="Test answer",
            reasoning="Test reasoning",
            confidence=0.95,
            sources=["doc1.txt"],
            tokens_used=100,
            latency_ms=500,
            model="glm-5-plus",
            strategy=ReasoningStrategy.HYBRID,
        )
        assert result.answer == "Test answer"
        assert result.confidence == 0.95
        assert result.success is True
    
    def test_result_to_dict(self):
        """Test result serialization."""
        result = ReasoningResult(
            answer="Test",
            reasoning="Reasoning",
            confidence=0.9,
            sources=["test.txt"],
            tokens_used=50,
            latency_ms=250,
            model="test-model",
            strategy=ReasoningStrategy.DIRECT,
        )
        data = result.to_dict()
        assert data["answer"] == "Test"
        assert data["confidence"] == 0.9
    
    def test_result_to_json(self):
        """Test JSON serialization."""
        result = ReasoningResult(
            answer="Test",
            reasoning="Reasoning",
            confidence=0.9,
            sources=["test.txt"],
            tokens_used=50,
            latency_ms=250,
            model="test-model",
            strategy=ReasoningStrategy.DIRECT,
        )
        json_str = result.to_json()
        assert "Test" in json_str
        assert "0.9" in json_str
    
    def test_empty_answer_failure(self):
        """Test that empty answer is marked as failure."""
        result = ReasoningResult(
            answer="",
            reasoning="",
            confidence=0.0,
            sources=[],
            tokens_used=0,
            latency_ms=0,
            model="test",
            strategy=ReasoningStrategy.DIRECT,
        )
        assert result.success is False


class TestConfig:
    """Tests for Config class."""
    
    def test_default_config(self):
        """Test default configuration."""
        config = Config()
        assert config.api_base == "https://open.bigmodel.cn/api/paas/v4"
        assert config.model == "glm-5-plus"
        assert config.timeout == 120
    
    def test_config_from_dict(self):
        """Test configuration from dictionary."""
        config = Config(
            api_key="test-key",
            model="custom-model",
        )
        assert config.api_key == "test-key"
        assert config.model == "custom-model"
    
    def test_config_validation(self):
        """Test configuration validation."""
        config = Config(api_key="test-key")
        errors = config.validate()
        # Should have no errors with valid API key
        assert len(errors) == 0
    
    def test_config_validation_missing_key(self):
        """Test validation with missing API key."""
        config = Config()
        errors = config.validate()
        assert len(errors) > 0
        assert any("API key" in e for e in errors)
    
    def test_config_to_dict(self):
        """Test configuration serialization."""
        config = Config(api_key="test-key")
        data = config.to_dict()
        assert data["api_key"] == "test-key"


class TestExceptions:
    """Tests for custom exceptions."""
    
    def test_base_exception(self):
        """Test base exception can be raised."""
        with pytest.raises(GLMReasonerError):
            raise GLMReasonerError("Test error")
    
    def test_authentication_error(self):
        """Test authentication error."""
        with pytest.raises(AuthenticationError):
            raise AuthenticationError("Invalid API key")
    
    def test_api_error(self):
        """Test API error."""
        with pytest.raises(APIError):
            raise APIError("Request failed")


class TestGLMReasonerInit:
    """Tests for GLMReasoner initialization."""
    
    def test_missing_api_key_raises_error(self):
        """Test that missing API key raises error."""
        import os
        # Clear the environment variable
        old_key = os.environ.pop("GLM_API_KEY", None)
        try:
            with pytest.raises(ValueError):
                GLMReasoner()
        finally:
            if old_key:
                os.environ["GLM_API_KEY"] = old_key
    
    def test_init_with_api_key(self):
        """Test initialization with API key."""
        reasoner = GLMReasoner(api_key="test-key")
        assert reasoner.api_key == "test-key"
        assert reasoner.model == "glm-5-plus"
    
    def test_init_with_custom_model(self):
        """Test initialization with custom model."""
        reasoner = GLMReasoner(
            api_key="test-key",
            model="custom-model"
        )
        assert reasoner.model == "custom-model"
    
    def test_init_with_custom_api_base(self):
        """Test initialization with custom API base."""
        reasoner = GLMReasoner(
            api_key="test-key",
            api_base="https://custom.api.com"
        )
        assert reasoner.api_base == "https://custom.api.com"
    
    def test_stats_initialization(self):
        """Test stats are properly initialized."""
        reasoner = GLMReasoner(api_key="test-key")
        stats = reasoner.stats
        assert stats["total_requests"] == 0
        assert stats["total_tokens"] == 0
        assert stats["failed_requests"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

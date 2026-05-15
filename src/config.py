"""
Configuration management for GLMReasoner.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path
import json
import os


@dataclass
class ProviderConfig:
    """Configuration for an API provider."""
    name: str
    api_key: Optional[str] = None
    api_base: str = "https://open.bigmodel.cn/api/paas/v4"
    model: str = "glm-5-plus"
    timeout: int = 120
    max_retries: int = 3
    default_temperature: float = 0.7
    default_max_tokens: int = 4096
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProviderConfig":
        """Create from dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class Config:
    """
    Global configuration for GLMReasoner.
    
    Can be loaded from file or environment variables.
    
    Example:
        >>> config = Config.from_env()
        >>> config = Config.from_file("~/.glmreasoner/config.json")
    """
    # API Configuration
    api_key: Optional[str] = None
    api_base: str = "https://open.bigmodel.cn/api/paas/v4"
    model: str = "glm-5-plus"
    timeout: int = 120
    max_retries: int = 3
    
    # Reasoning Configuration
    default_strategy: str = "hybrid"
    default_temperature: float = 0.7
    default_max_tokens: int = 4096
    context_window: int = 128000  # 128K for GLM-5
    
    # Document Processing
    max_document_size: int = 10_000_000  # 10MB
    supported_formats: List[str] = field(
        default_factory=lambda: ["txt", "md", "json", "csv", "html", "pdf"]
    )
    chunk_size: int = 100_000  # Characters per chunk
    
    # Caching
    cache_enabled: bool = True
    cache_dir: str = "~/.glmreasoner/cache"
    
    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    # Advanced
    extra_headers: Dict[str, str] = field(default_factory=dict)
    proxy: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        return cls(
            api_key=os.environ.get("GLM_API_KEY"),
            api_base=os.environ.get("GLM_API_BASE", cls.api_base),
            model=os.environ.get("GLM_MODEL", cls.model),
            timeout=int(os.environ.get("GLM_TIMEOUT", str(cls.timeout))),
            max_retries=int(os.environ.get("GLM_MAX_RETRIES", str(cls.max_retries))),
            default_temperature=float(os.environ.get("GLM_TEMPERATURE", str(cls.default_temperature))),
            default_max_tokens=int(os.environ.get("GLM_MAX_TOKENS", str(cls.default_max_tokens))),
            cache_dir=os.environ.get("GLM_CACHE_DIR", cls.cache_dir),
            log_level=os.environ.get("GLM_LOG_LEVEL", cls.log_level),
            proxy=os.environ.get("GLM_PROXY"),
        )
    
    @classmethod
    def from_file(cls, file_path: str) -> "Config":
        """Load configuration from JSON file."""
        path = Path(file_path).expanduser()
        
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        return cls(**data)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {}
        for key, value in self.__dict__.items():
            if value is not None:
                result[key] = value
        return result
    
    def to_file(self, file_path: str, create_dirs: bool = True):
        """Save configuration to JSON file."""
        path = Path(file_path).expanduser()
        
        if create_dirs:
            path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    def validate(self) -> List[str]:
        """
        Validate configuration.
        
        Returns:
            List of validation errors (empty if valid).
        """
        errors = []
        
        if not self.api_key:
            errors.append("API key is required (set GLM_API_KEY environment variable)")
        
        if self.timeout < 10:
            errors.append("Timeout must be at least 10 seconds")
        
        if self.max_retries < 0:
            errors.append("Max retries must be non-negative")
        
        if not 0 < self.default_temperature <= 2:
            errors.append("Temperature must be between 0 and 2")
        
        return errors
    
    def ensure_cache_dir(self) -> Path:
        """Ensure cache directory exists and return its path."""
        cache_path = Path(self.cache_dir).expanduser()
        cache_path.mkdir(parents=True, exist_ok=True)
        return cache_path


# Default config instance
_default_config: Optional[Config] = None


def get_default_config() -> Config:
    """Get or create default configuration."""
    global _default_config
    if _default_config is None:
        _default_config = Config.from_env()
    return _default_config


def set_default_config(config: Config):
    """Set default configuration."""
    global _default_config
    _default_config = config

# 🧠 GLMReasoner

> **Long Context Cross-Document Intelligent Reasoning Engine**
> 
> Powered by GLM-5.1 | 128K Context Window | Multi-Strategy Reasoning

---

## 🌐 Language

[![English](https://img.shields.io/badge/English-README-blue)](README.md)
[![简体中文](https://img.shields.io/badge/简体中文-自述文件-green)](README.zh-CN.md)
[![繁體中文](https://img.shields.io/badge/繁體中文-說明文件-orange)](README.zh-TW.md)
[![日本語](https://img.shields.io/badge/日本語-説明-green)](README.ja-JP.md)

---

## 🎯 Project Introduction

**GLMReasoner** is a long-context cross-document intelligent reasoning engine built on GLM-5.1's 128K context window. It enables deep reasoning across multiple documents simultaneously, extracting insights, identifying relationships, and synthesizing information from diverse sources.

### ✨ Key Differentiators

- 🚀 **128K Ultra-Long Context** - Process entire document collections in a single pass
- 🧠 **Multi-Strategy Reasoning** - Chain-of-Thought, Tree-of-Thought, Self-Ask, Hybrid
- 📚 **Cross-Document Analysis** - Find relationships across multiple documents
- ⚡ **Zero-Dependency Core** - Pure Python, minimal dependencies
- 🔄 **Batch Processing** - Handle multiple queries efficiently
- 📊 **Rich Metadata** - Confidence scores, source tracking, token analytics

---

## 🎪 Core Features

### 📖 Multi-Format Document Support

| Format | Extension | Status |
|--------|----------|--------|
| Plain Text | `.txt` | ✅ Full |
| Markdown | `.md` | ✅ Full |
| JSON | `.json` | ✅ Full |
| CSV | `.csv` | ✅ Full |
| HTML | `.html` | ✅ Full |
| PDF | `.pdf` | 🔜 Coming |

### 🧠 Reasoning Strategies

```python
from GLMReasoner import GLMReasoner, Document, Query, ReasoningStrategy

reasoner = GLMReasoner(api_key="your-key")

# Strategy 1: Direct Answer
query = Query(question="What is the main finding?", strategy=ReasoningStrategy.DIRECT)

# Strategy 2: Chain of Thought
query = Query(question="Explain the relationship", strategy=ReasoningStrategy.CHAIN_OF_THOUGHT)

# Strategy 3: Tree of Thought
query = Query(question="Compare different approaches", strategy=ReasoningStrategy.TREE_OF_THOUGHT)

# Strategy 4: Self-Ask
query = Query(question="Analyze the implications", strategy=ReasoningStrategy.SELF_ASK)

# Strategy 5: Hybrid (Recommended)
query = Query(question="Synthesize all findings", strategy=ReasoningStrategy.HYBRID)
```

### 🔍 Cross-Document Analysis Example

```python
from GLMReasoner import GLMReasoner, Document, Query

# Load multiple documents
docs = [
    Document.from_file("research_paper.pdf"),
    Document.from_file("technical_report.md"),
    Document.from_file("meeting_notes.txt"),
]

# Create reasoning query
query = Query(
    question="What are the key findings across all documents?",
    strategy=ReasoningStrategy.HYBRID
)

# Execute reasoning
reasoner = GLMReasoner(api_key="your-key")
result = reasoner.reason(docs, query)

print(f"Answer: {result.answer}")
print(f"Confidence: {result.confidence:.2%}")
print(f"Sources: {result.sources}")
```

---

## 🚀 Quick Start

### 📦 Installation

```bash
# Install from PyPI (coming soon)
pip install GLMReasoner

# Or install from source
git clone https://github.com/gitstq/GLMReasoner.git
cd GLMReasoner
pip install -e .
```

### 🔑 Configuration

Set your API key:

```bash
# Option 1: Environment variable (recommended)
export GLM_API_KEY="your-api-key-here"

# Option 2: CLI parameter
glmreasoner --api-key "your-api-key" "your question" document.txt
```

### 💻 Basic Usage

```bash
# Simple query
glmreasoner "What is the main topic?" document.txt

# With chain of thought reasoning
glmreasoner --strategy cot "Explain the relationship" report.pdf

# Batch queries from JSON
glmreasoner --queries questions.json corpus/

# Save results
glmreasoner --output results.json "your question" doc1.md doc2.txt
```

### 🐍 Python API

```python
from GLMReasoner import GLMReasoner, Document, Query

# Initialize
reasoner = GLMReasoner(api_key="your-api-key")

# Load document
doc = Document.from_file("report.pdf")

# Create query
query = Query(question="What are the key findings?")

# Execute
result = reasoner.reason([doc], query)

# Access results
print(result.answer)           # The answer
print(result.confidence)        # 0.0 - 1.0
print(result.sources)          # List of source files
print(result.tokens_used)      # Token consumption
print(result.latency_ms)       # Response time

# View statistics
print(reasoner.stats)
```

---

## 📖 Detailed Usage Guide

### Batch Processing

```python
# Multiple queries
queries = [
    Query(question="What is the main topic?"),
    Query(question="List all key findings."),
    Query(question="What are the recommendations?"),
]

results = reasoner.reason_batch(documents, queries)
```

### Custom Configuration

```python
from GLMReasoner import Config

config = Config(
    api_key="your-key",
    model="glm-5-plus",
    default_strategy="hybrid",
    default_temperature=0.7,
)

reasoner = GLMReasoner(**config.to_dict())
```

### CLI with Configuration File

```json
// config.json
{
    "api_key": "your-key",
    "model": "glm-5-plus",
    "default_temperature": 0.7,
    "log_level": "INFO"
}
```

```bash
export GLM_API_KEY="your-key"  # Load from env or config
glmreasoner "Your question" document.txt
```

---

## 💡 Design Philosophy

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    GLMReasoner                          │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │  Document   │  │   Query     │  │   Config    │   │
│  │  Loader    │  │  Builder    │  │   Manager   │   │
│  └──────┬──────┘  └──────┬──────┘  └─────────────┘   │
│         │                │                             │
│         └────────┬───────┘                             │
│                  ▼                                     │
│         ┌───────────────┐                             │
│         │ Prompt Engine │                             │
│         │ (Multi-Strategy)│                           │
│         └───────┬───────┘                             │
│                 │                                     │
│                 ▼                                     │
│         ┌───────────────┐                             │
│         │  GLM-5 API   │                             │
│         │  (128K ctx)   │                             │
│         └───────┬───────┘                             │
│                 │                                     │
│                 ▼                                     │
│         ┌───────────────┐                             │
│         │Result Parser │                             │
│         │& Analytics   │                             │
│         └───────────────┘                             │
└─────────────────────────────────────────────────────────┘
```

### Why GLM-5.1?

| Feature | GLM-5.1 | GPT-4 | Claude |
|---------|---------|-------|-------|
| Context Window | 128K ✅ | 128K | 200K |
| Chinese Performance | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Cost Efficiency | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Cross-Doc Reasoning | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| API Stability | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🔄 Roadmap

- [ ] **v1.1** - PDF parsing support
- [ ] **v1.2** - Streaming response support
- [ ] **v1.3** - Async/await API
- [ ] **v1.4** - Web UI dashboard
- [ ] **v2.0** - Multi-modal document support

---

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines first.

```bash
# Fork the repository
# Create your feature branch
git checkout -b feature/amazing-feature

# Commit your changes
git commit -m "feat: add amazing feature"

# Push to the branch
git push origin feature/amazing-feature

# Open a Pull Request
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- **GLM Team** - For the powerful GLM-5.1 model
- **Zhipu AI** - For providing the API
- **Open Source Community** - For inspiration and contributions

---

## 📬 Contact

- **Author**: [gitstq](https://github.com/gitstq)
- **Issues**: [GitHub Issues](https://github.com/gitstq/GLMReasoner/issues)
- **Discussions**: [GitHub Discussions](https://github.com/gitstq/GLMReasoner/discussions)

---

<p align="center">
  <strong>Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a></strong>
  <br>
  <sub>If this project helps you, please give it a ⭐</sub>
</p>

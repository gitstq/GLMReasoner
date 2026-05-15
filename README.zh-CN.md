# 🧠 GLMReasoner

> **基于GLM-5.1的长上下文跨文档智能推理引擎**
>
> 128K上下文窗口 | 多策略推理 | 跨文档分析

---

## 🌐 语言切换

[![English](https://img.shields.io/badge/English-自述文件-blue)](README.md)
[![简体中文](https://img.shields.io/badge/简体中文-自述文件-green)](README.zh-CN.md)
[![繁體中文](https://img.shields.io/badge/繁體中文-說明文件-orange)](README.zh-TW.md)
[![日本語](https://img.shields.io/badge/日本語-説明-green)](README.ja-JP.md)

---

## 🎯 项目介绍

**GLMReasoner** 是一款基于 GLM-5.1 模型 128K 上下文窗口构建的长上下文跨文档智能推理引擎。它能够同时对多个文档进行深度推理，提取洞察、识别关联、整合来自不同来源的信息。

### ✨ 核心亮点

- 🚀 **128K 超长上下文** - 单次处理整个文档集合
- 🧠 **多策略推理** - 思维链、思维树、自问自答、混合策略
- 📚 **跨文档分析** - 发现多个文档之间的关系
- ⚡ **零依赖核心** - 纯Python，最小依赖
- 🔄 **批量处理** - 高效处理多个查询
- 📊 **丰富元数据** - 置信度、来源追踪、令牌统计

---

## 🎪 核心功能

### 📖 多格式文档支持

| 格式 | 扩展名 | 状态 |
|------|--------|------|
| 纯文本 | `.txt` | ✅ 支持 |
| Markdown | `.md` | ✅ 支持 |
| JSON | `.json` | ✅ 支持 |
| CSV | `.csv` | ✅ 支持 |
| HTML | `.html` | ✅ 支持 |
| PDF | `.pdf` | 🔜 即将支持 |

### 🧠 推理策略

```python
from GLMReasoner import GLMReasoner, Document, Query, ReasoningStrategy

reasoner = GLMReasoner(api_key="your-key")

# 策略1：直接回答
query = Query(question="主要发现是什么？", strategy=ReasoningStrategy.DIRECT)

# 策略2：思维链
query = Query(question="解释其中的关系", strategy=ReasoningStrategy.CHAIN_OF_THOUGHT)

# 策略3：思维树
query = Query(question="比较不同方法", strategy=ReasoningStrategy.TREE_OF_THOUGHT)

# 策略4：自问自答
query = Query(question="分析其影响", strategy=ReasoningStrategy.SELF_ASK)

# 策略5：混合策略（推荐）
query = Query(question="综合所有发现", strategy=ReasoningStrategy.HYBRID)
```

### 🔍 跨文档分析示例

```python
from GLMReasoner import GLMReasoner, Document, Query

# 加载多个文档
docs = [
    Document.from_file("研究报告.pdf"),
    Document.from_file("技术报告.md"),
    Document.from_file("会议笔记.txt"),
]

# 创建推理查询
query = Query(
    question="所有文档中的关键发现是什么？",
    strategy=ReasoningStrategy.HYBRID
)

# 执行推理
reasoner = GLMReasoner(api_key="your-key")
result = reasoner.reason(docs, query)

print(f"答案：{result.answer}")
print(f"置信度：{result.confidence:.2%}")
print(f"来源：{result.sources}")
```

---

## 🚀 快速开始

### 📦 安装

```bash
# 从PyPI安装（即将上线）
pip install GLMReasoner

# 或者从源码安装
git clone https://github.com/gitstq/GLMReasoner.git
cd GLMReasoner
pip install -e .
```

### 🔑 配置

设置您的API密钥：

```bash
# 方式1：环境变量（推荐）
export GLM_API_KEY="your-api-key-here"

# 方式2：CLI参数
glmreasoner --api-key "your-api-key" "your question" document.txt
```

### 💻 基本用法

```bash
# 简单查询
glmreasoner "主题是什么？" document.txt

# 使用思维链推理
glmreasoner --strategy cot "解释关系" report.pdf

# 从JSON批量查询
glmreasoner --queries questions.json corpus/

# 保存结果
glmreasoner --output results.json "your question" doc1.md doc2.txt
```

### 🐍 Python API

```python
from GLMReasoner import GLMReasoner, Document, Query

# 初始化
reasoner = GLMReasoner(api_key="your-api-key")

# 加载文档
doc = Document.from_file("report.pdf")

# 创建查询
query = Query(question="主要发现是什么？")

# 执行推理
result = reasoner.reason([doc], query)

# 访问结果
print(result.answer)           # 答案
print(result.confidence)        # 0.0 - 1.0
print(result.sources)          # 来源文件列表
print(result.tokens_used)       # 令牌消耗
print(result.latency_ms)       # 响应时间

# 查看统计信息
print(reasoner.stats)
```

---

## 📖 详细使用指南

### 批量处理

```python
# 多个查询
queries = [
    Query(question="主题是什么？"),
    Query(question="列出所有关键发现。"),
    Query(question="有什么建议？"),
]

results = reasoner.reason_batch(documents, queries)
```

### 自定义配置

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

### CLI配置文件

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
export GLM_API_KEY="your-key"  # 从环境变量或配置文件加载
glmreasoner "你的问题" document.txt
```

---

## 💡 设计理念

### 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                    GLMReasoner                          │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │   文档     │  │   查询     │  │   配置     │   │
│  │   加载器   │  │   构建器   │  │   管理器   │   │
│  └──────┬──────┘  └──────┬──────┘  └─────────────┘   │
│         │                │                             │
│         └────────┬───────┘                             │
│                  ▼                                     │
│         ┌───────────────┐                             │
│         │  提示词引擎  │                             │
│         │ (多策略支持)  │                             │
│         └───────┬───────┘                             │
│                 │                                     │
│                 ▼                                     │
│         ┌───────────────┐                             │
│         │  GLM-5 API   │                             │
│         │  (128K上下文) │                             │
│         └───────┬───────┘                             │
│                 │                                     │
│                 ▼                                     │
│         ┌───────────────┐                             │
│         │ 结果解析器   │                             │
│         │ & 分析统计   │                             │
│         └───────────────┘                             │
└─────────────────────────────────────────────────────────┘
```

### 为什么选择GLM-5.1？

| 特性 | GLM-5.1 | GPT-4 | Claude |
|------|---------|-------|--------|
| 上下文窗口 | 128K ✅ | 128K | 200K |
| 中文表现 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 成本效益 | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| 跨文档推理 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| API稳定性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🔄 路线图

- [ ] **v1.1** - PDF解析支持
- [ ] **v1.2** - 流式响应支持
- [ ] **v1.3** - 异步API
- [ ] **v1.4** - Web UI仪表盘
- [ ] **v2.0** - 多模态文档支持

---

## 🤝 贡献

欢迎贡献！请先阅读贡献指南。

```bash
# Fork本仓库
# 创建功能分支
git checkout -b feature/amazing-feature

# 提交更改
git commit -m "feat: 添加新功能"

# 推送到分支
git push origin feature/amazing-feature

# 打开Pull Request
```

---

## 📄 许可证

本项目采用MIT许可证 - 详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- **GLM团队** - 提供强大的GLM-5.1模型
- **智谱AI** - 提供API服务
- **开源社区** - 提供灵感和贡献

---

## 📬 联系方式

- **作者**: [gitstq](https://github.com/gitstq)
- **问题反馈**: [GitHub Issues](https://github.com/gitstq/GLMReasoner/issues)
- **讨论区**: [GitHub Discussions](https://github.com/gitstq/GLMReasoner/discussions)

---

<p align="center">
  <strong>❤️ 由 <a href="https://github.com/gitstq">gitstq</a> 精心打造</strong>
  <br>
  <sub>如果这个项目对您有帮助，请给它一个 ⭐</sub>
</p>

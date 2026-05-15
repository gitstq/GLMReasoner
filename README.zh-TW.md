# 🧠 GLMReasoner

> **基於GLM-5.1的長上下文跨文檔智慧推理引擎**
>
> 128K上下文窗口 | 多策略推理 | 跨文檔分析

---

## 🌐 語言切換

[![English](https://img.shields.io/badge/English-說明文件-blue)](README.md)
[![简体中文](https://img.shields.io/badge/简体中文-自述文件-green)](README.zh-CN.md)
[![繁體中文](https://img.shields.io/badge/繁體中文-說明文件-orange)](README.zh-TW.md)
[![日本語](https://img.shields.io/badge/日本語-説明-green)](README.ja-JP.md)

---

## 🎯 專案介紹

**GLMReasoner** 是一款基於 GLM-5.1 模型 128K 上下文窗口構建的長上下文跨文檔智慧推理引擎。它能夠同時對多個文檔進行深度推理，提取洞察、識別關聯、整合來自不同來源的資訊。

### ✨ 核心亮點

- 🚀 **128K 超長上下文** - 單次處理整個文檔集合
- 🧠 **多策略推理** - 思維鏈、思維樹、自問自答、混合策略
- 📚 **跨文檔分析** - 發現多個文檔之間的關係
- ⚡ **零依賴核心** - 純Python，最小依賴
- 🔄 **批次處理** - 高效處理多個查詢
- 📊 **豐富元數據** - 置信度、來源追蹤、令牌統計

---

## 🎪 核心功能

### 📖 多格式文檔支援

| 格式 | 副檔名 | 狀態 |
|------|--------|------|
| 純文字 | `.txt` | ✅ 支援 |
| Markdown | `.md` | ✅ 支援 |
| JSON | `.json` | ✅ 支援 |
| CSV | `.csv` | ✅ 支援 |
| HTML | `.html` | ✅ 支援 |
| PDF | `.pdf` | 🔜 即將支援 |

### 🧠 推理策略

```python
from GLMReasoner import GLMReasoner, Document, Query, ReasoningStrategy

reasoner = GLMReasoner(api_key="your-key")

# 策略1：直接回答
query = Query(question="主要發現是什麼？", strategy=ReasoningStrategy.DIRECT)

# 策略2：思維鏈
query = Query(question="解釋其中的關係", strategy=ReasoningStrategy.CHAIN_OF_THOUGHT)

# 策略3：思維樹
query = Query(question="比較不同方法", strategy=ReasoningStrategy.TREE_OF_THOUGHT)

# 策略4：自問自答
query = Query(question="分析其影響", strategy=ReasoningStrategy.SELF_ASK)

# 策略5：混合策略（推薦）
query = Query(question="綜合所有發現", strategy=ReasoningStrategy.HYBRID)
```

### 🔍 跨文檔分析範例

```python
from GLMReasoner import GLMReasoner, Document, Query

# 載入多個文檔
docs = [
    Document.from_file("研究報告.pdf"),
    Document.from_file("技術報告.md"),
    Document.from_file("會議筆記.txt"),
]

# 建立推理查詢
query = Query(
    question="所有文檔中的關鍵發現是什麼？",
    strategy=ReasoningStrategy.HYBRID
)

# 執行推理
reasoner = GLMReasoner(api_key="your-key")
result = reasoner.reason(docs, query)

print(f"答案：{result.answer}")
print(f"置信度：{result.confidence:.2%}")
print(f"來源：{result.sources}")
```

---

## 🚀 快速開始

### 📦 安裝

```bash
# 從PyPI安裝（即將上線）
pip install GLMReasoner

# 或者從原始碼安裝
git clone https://github.com/gitstq/GLMReasoner.git
cd GLMReasoner
pip install -e .
```

### 🔑 配置

設定您的API密鑰：

```bash
# 方式1：環境變數（推薦）
export GLM_API_KEY="your-api-key-here"

# 方式2：CLI參數
glmreasoner --api-key "your-api-key" "your question" document.txt
```

### 💻 基本用法

```bash
# 簡單查詢
glmreasoner "主題是什麼？" document.txt

# 使用思維鏈推理
glmreasoner --strategy cot "解釋關係" report.pdf

# 從JSON批次查詢
glmreasoner --queries questions.json corpus/

# 儲存結果
glmreasoner --output results.json "your question" doc1.md doc2.txt
```

### 🐍 Python API

```python
from GLMReasoner import GLMReasoner, Document, Query

# 初始化
reasoner = GLMReasoner(api_key="your-api-key")

# 載入文檔
doc = Document.from_file("report.pdf")

# 建立查詢
query = Query(question="主要發現是什麼？")

# 執行推理
result = reasoner.reason([doc], query)

# 存取結果
print(result.answer)           # 答案
print(result.confidence)        # 0.0 - 1.0
print(result.sources)          # 來源檔案列表
print(result.tokens_used)       # 令牌消耗
print(result.latency_ms)       # 回應時間

# 檢視統計資訊
print(reasoner.stats)
```

---

## 🤝 貢獻

歡迎貢獻！請先閱讀貢獻指南。

```bash
# Fork本倉庫
# 建立功能分支
git checkout -b feature/amazing-feature

# 提交更改
git commit -m "feat: 添加新功能"

# 推送到分支
git push origin feature/amazing-feature

# 開啟Pull Request
```

---

## 📄 授權

本專案採用MIT授權 - 詳見 [LICENSE](LICENSE) 檔案。

---

## 📬 聯絡方式

- **作者**: [gitstq](https://github.com/gitstq)
- **問題回饋**: [GitHub Issues](https://github.com/gitstq/GLMReasoner/issues)

<p align="center">
  <strong>❤️ 由 <a href="https://github.com/gitstq">gitstq</a> 精心打造</strong>
  <br>
  <sub>如果這個專案對您有幫助，請給它一個 ⭐</sub>
</p>

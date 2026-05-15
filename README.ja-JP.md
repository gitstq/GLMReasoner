# 🧠 GLMReasoner

> **GLM-5.1に基づく長文脈クロpdocスマート推論エンジン**
>
> 128Kコンテキストウィンドウ | マルチストラテジー推論 | クロpdoc分析

---

## 🌐 言語切替

[![English](https://img.shields.io/badge/English-説明-blue)](README.md)
[![简体中文](https://img.shields.io/badge/简体中文-自述文件-green)](README.zh-CN.md)
[![繁體中文](https://img.shields.io/badge/繁體中文-說明文件-orange)](README.zh-TW.md)
[![日本語](https://img.shields.io/badge/日本語-説明-green)](README.ja-JP.md)

---

## 🎯 プロジェクト紹介

**GLMReasoner** は、GLM-5.1モデルの128Kコンテキストウィンドウに基づいて構築された長文脈クロpdocスマート推論エンジンです。複数のpdocを同時に深く推論し、インサイトを抽出し、リレーションシップを特定し、異なるソースからの情報を統合します。

### ✨ コア機能

- 🚀 **128K超長文脈** - 1パスでpdocコレクション全体 처리
- 🧠 **マルチストラテジー推論** - Chain-of-Thought、Tree-of-Thought、Self-Ask、Hybrid
- 📚 **クロpdoc分析** - 複数のpdoc間の関係を発見
- ⚡ **ゼロ依存コア** - ピュアPython、最小限の依存関係
- 🔄 **バッチ処理** - 複数のクエリを効率的に処理
- 📊 **豊富なメタデータ** - 信頼度、ソース追跡、トークン分析

---

## 🚀 クイックスタート

### 📦 インストール

```bash
# PyPIからインストール（近日公開）
pip install GLMReasoner

# またはソースからインストール
git clone https://github.com/gitstq/GLMReasoner.git
cd GLMReasoner
pip install -e .
```

### 🔑 設定

APIキーを設定します：

```bash
# オプション1：環境変数（推奨）
export GLM_API_KEY="your-api-key-here"

# オプション2：CLIパラメータ
glmreasoner --api-key "your-api-key" "your question" document.txt
```

### 💻 基本的な使用方法

```bash
# シンプルクエリ
glmreasoner "テーマは何か？" document.txt

# 思考連鎖推論を使用
glmreasoner --strategy cot "関係を説明" report.pdf

# JSONからバッチクエリ
glmreasoner --queries questions.json corpus/

# 結果を保存
glmreasoner --output results.json "your question" doc1.md doc2.txt
```

### 🐍 Python API

```python
from GLMReasoner import GLMReasoner, Document, Query

# 初期化
reasoner = GLMReasoner(api_key="your-api-key")

# pdocをロード
doc = Document.from_file("report.pdf")

# クエリを作成
query = Query(question="主要な発見は何か？")

# 推論を実行
result = reasoner.reason([doc], query)

# 結果にアクセス
print(result.answer)           # 回答
print(result.confidence)        # 0.0 - 1.0
print(result.sources)          # ソースファイルリスト
print(result.tokens_used)       # トークン消費
print(result.latency_ms)       # 応答時間

# 統計を表示
print(reasoner.stats)
```

---

## 🤝 コントリビューション

コントリビューションは歓迎です！コントリビューションガイドラインをご確認ください。

```bash
# リポジトリをフォーク
# フィーチャーブランチを作成
git checkout -b feature/amazing-feature

# 変更をコミット
git commit -m "feat: add amazing feature"

# ブランチにプッシュ
git push origin feature/amazing-feature

# Pull Requestを開く
```

---

## 📄 ライセンス

このプロジェクトはMITライセンスに基づいてライセンス供与されています - 詳細については[LICENSE](LICENSE)ファイルをご確認ください。

---

## 📬 連絡先

- **作者**: [gitstq](https://github.com/gitstq)
- **イシュー**: [GitHub Issues](https://github.com/gitstq/GLMReasoner/issues)

<p align="center">
  <strong>❤️ <a href="https://github.com/gitstq">gitstq</a> が作成</strong>
  <br>
  <sub>このプロジェクトが役に立ったら、⭐をください</sub>
</p>

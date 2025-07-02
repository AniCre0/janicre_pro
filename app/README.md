
# 📄 Contract AI Agent

AIを活用して、CLI上で日本語の契約書（賃貸契約書・業務委託契約書）を自動生成・PDF出力するツールです。

---

## 🔧 Features

- 🤖 **自然言語入力 → GPTで必要項目抽出**
- 🏷️ **契約タイプを自動判定（賃貸 / 業務委託）**
- 🔁 **欠落項目は自然な日本語でヒアリング**
- 📄 **Jinja2テンプレートでPDF出力**
- ✅ **スキーマベースバリデーション（`.janicre`）**
- 🌐 **`.apdf`対応：全文検索＋プレビュー可能な新フォーマット**

---

## 🚀 Usage

### 1. Install

```bash
git clone https://github.com/yourname/contract-ai-agent.git
cd contract-ai-agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Set API Key

`.env` ファイルを作成：

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Run CLI

```bash
python app/generate_interactive.py "株式会社ABCは、エンジニア業務を委託します。報酬は20万円です。"
```

---

## 🔍 検索・プレビュー（`.apdf`）

Flaskサーバー起動：

```bash
python app/server.py
```

ブラウザで開く：

[http://localhost:5000/static/index.html](http://localhost:5000/static/index.html)

- `.apdf`の全文検索
- クリックで即PDFプレビュー

---

## 📦 `.apdf`とは？

- 🧾 PDFレイアウトを保持
- 🔍 構造化テキストで全文検索対応
- 🧠 AIによる知識ベース化に最適

---

## ⚙️ 仕組み

```
+--------------------------------------------------------------+
|              🌐 ユーザー入力（自然文）                     |
|  例:「ABC株式会社は、XYZにアニメ制作を委託。」             |
+--------------------------------------------------------------+
                               |
                               v
+--------------------------------------------------------------+
| 🧠 ① 契約タイプの自動判定（classify_doc_type）             |
| - GPT-4o による判定: 'rental' or 'outsourcing'              |
| - フォールバック: キーワード（「家賃」等）で分類           |
+--------------------------------------------------------------+
                               |
                               v
+--------------------------------------------------------------+
| ② 対応テンプレート・スキーマ読み込み（.tpl / .janicre）     |
| - rental → rental_agreement.tpl / .janicre                   |
| - outsourcing → outsourcing_agreement.tpl / .janicre         |
+--------------------------------------------------------------+
                               |
                               v
+--------------------------------------------------------------+
| ③ 初期情報の構造化（generate_contract_context）             |
| - OpenAI API で context を生成（key-value）形式             |
+--------------------------------------------------------------+
                               |
                               v
+--------------------------------------------------------------+
| ④ janicre によるバリデーションと正規化（validate）         |
| - schema に基づき欠損フィールドを抽出                       |
+--------------------------------------------------------------+
                               |
           +-------------------+-------------------+
           |                                       |
           v                                       v
+-----------------------------+       +----------------------------------+
| ❓ 不足情報をユーザーに質問  |       | ✅ 情報がすべて揃っている場合       |
| - GPTで丁寧に聞き返す文生成 |       | - contextをテンプレートに流し込む  |
| - 入力を元に再生成          |       | - PDFとして出力（render_contract） |
+-----------------------------+       +----------------------------------+
           ^
           |
           +------（不足がある限りループ）------------------+
---
```
## 🧠 janicre の仕組み（簡易版）
```
janicre（Japanese Natural Input Contract REquirements）は、
自然言語で与えられた契約情報を 構造化して検証・補完 するための最小スキーマ仕様です。
AIによる契約書作成の精度と信頼性を向上させるために設計されました。

🔧 目的
✅ GPTなどのLLMが生成する不定形なJSONをバリデート＆正規化する

✅ 契約テンプレートに必要な構造的なフィールドを明示する

✅ ユーザー入力との不足項目を検出し、追加質問を自動生成する

📦 スキーマ定義形式
.janicre 拡張子を持つ JSON ファイルで定義。以下は例です：


{
  "spec": "rental_agreement",
  "fields": [
    {
      "name": "property_address",
      "type": "string",
      "required": true,
      "aliases": ["物件の住所", "所在地"]
    },
    {
      "name": "property_size",
      "type": "number",
      "required": true,
      "aliases": ["面積", "広さ"]
    }
    // 以降略
  ]
}
```
🎯 フィールド属性
属性名	説明
name	プログラム上での正式なキー名（テンプレートに流し込まれる）
type	string / number / boolean のいずれか
required	必須項目かどうか
aliases	自然文で使われることが多い日本語表現（GPT補完・照合に使用）

🔄 janicre の処理フロー
normalize(json, schema)

エイリアス名の補正や型補正を行い、形式を揃えます。

validate(json, schema)

スキーマ上 required: true で定義されたフィールドが埋まっているか検査します。

未入力のフィールドをリストで返します（後続の質問生成に使用）。

💡 導入のメリット
項目	janicre 導入前	janicre 導入後
JSON信頼性	GPT依存で形式ゆらぎが大きい	スキーマで構造を統一・正規化できる
欠損補完	手動で確認しながら聞き直しが必要	自動で「何が足りないか」を検出可能
契約テンプレート整合性	フィールド名ミスマッチが多発	テンプレートと完全に一致した構造へ
拡張性	各契約タイプの条件が混在しがち	各 .janicre によって分離・再利用可能

---

## 📂 ディレクトリ構成

```
.
├── app/
│   ├── ai_openai.py
│   ├── render.py
│   ├── generate_interactive.py
│   ├── janicre_schema.py
│   └── templates/
│       ├── rental_agreement.tpl
│       └── outsourcing_agreement.tpl
├── schemas/
│   ├── rental_agreement.janicre.json
│   └── outsourcing_agreement.janicre.json
├── output/
│   └── *.pdf
└── README.md
```

---

## 🔤 スキーマ形式（例：`.janicre`）

```json
{
  "spec": "outsourcing_agreement",
  "fields": [
    {
      "name": "client_name",
      "type": "string",
      "required": true,
      "aliases": ["クライアント名", "依頼者"]
    }
  ]
}
```

---

## 🤖 使用技術

- Python 3.9+
- OpenAI GPT-4o
- Jinja2
- WeasyPrint
- Flask
- `.janicre` スキーマ形式
- `.apdf` 拡張子（全文検索＋プレビュー統合）

---

## 📬 今後の展望

- CLIでの契約タイプ選択オプション
- PDFスタイルのカスタマイズ（印鑑・フォント等）
- 英語対応、Word出力対応

---

## 👤 作者

**岡崎 友哉（Tomoya Okazaki）**  
📧 [tomoya@anime-create.com](mailto:tomoya@anime-create.com)  
🌐 [https://anime-create.com](https://anime-create.com)

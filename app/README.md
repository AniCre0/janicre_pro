
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

```plaintext
ユーザー入力（自然文）
     ↓
契約タイプの自動判定（GPTまたはキーワード）
     ↓
テンプレートとスキーマの読み込み
     ↓
OpenAIで初期情報を構造化
     ↓
janicreでバリデーション・正規化
     ↓
不足項目があれば自然文でヒアリング
     ↓
すべて揃えばPDF出力（Jinja2 + WeasyPrint）
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

## 🧠 janicre の仕組み（簡易版）

1. **スキーマ読み込み**
   ```python
   schema = load_schema("rental_agreement.janicre")
   ```

2. **正規化（Normalize）**
   - 「契約開始日」→ `start_date` などに変換

3. **バリデーション（Validate）**
   - 必須項目が入力されているか確認

4. **不足項目の質問文生成**

5. **ループ再生成**
   - 入力が完全になるまで繰り返し

6. **PDF出力**
   ```python
   render_contract(template, context, output_path)
   ```

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

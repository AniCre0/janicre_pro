# 📄 Contract AI Agent

AIを活用して、CLI上で日本語の契約書（賃貸契約書・業務委託契約書）を自動生成・PDF出力し、さらに検索可能な `.apdf` 形式で統合管理するツールです。

## 🚀 特徴

- ✅ OpenAI GPTを用いた契約書自動生成（自然言語→構造化情報）
- ✅ Jinja2テンプレートで契約書を動的レンダリング
- ✅ PDFファイルとして出力・保存
- ✅ `.apdf`（PDF＋検索用テキストをZIP化）形式にまとめて一元管理  
- ✅ Flaskサーバーで `.apdf` を検索・プレビュー  
- ✅ CLIで簡単操作
- ✅ `.janicre` スキーマによる構造検証  
   → JSON形式の契約書情報がテンプレート仕様に準拠しているかを自動検証し、未記入項目や曖昧な入力（例："未定"）をインタラクティブにCLI上で聞き返します。  
   → `"question"` 属性を使った対話的な補完により、自然なUXで漏れのない契約書生成が可能です。

---

## 🛠️ セットアップ

```bash
git clone https://github.com/bakuraku-applicant-codes/coding-test-AniCre0-20250606.git
cd coding-test-AniCre0-20250606
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

※ `.env` ファイルに `OPENAI_API_KEY` を設定する必要があります。

```ini
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 📦 使い方

### 賃貸契約書の生成

```bash
python generate_pdf.py rental "山田 太郎が所有する東京都渋谷区○○1-2-3の物件を、佐藤 花子が1年間賃貸する。家賃は月12万円、毎月10日払い。敷金は2ヶ月分、礼金は1ヶ月分。契約開始は2025年7月1日で、終了は2026年6月30日。解約の際は30日前に通知が必要とする。"
```

### 業務委託契約書の生成

```bash
python generate_pdf.py outsourcing "株式会社ABCは、フリーランスの山本 太郎にWeb開発業務を委託する。契約期間は2025年7月1日から12月31日まで、報酬は月額30万円。成果物の納品は月末とし、納品後5営業日以内に検収を行う。守秘義務あり。"
```

生成後、`output/` フォルダ内に以下のファイルが揃います：

- `<テンプレート名>_YYYYMMDD_HHMMSS.pdf`  
- `<テンプレート名>_YYYYMMDD_HHMMSS.txt`  
- `<テンプレート名>_YYYYMMDD_HHMMSS.apdf`

---

## 🔍 検索・プレビュー
<img width="824" alt="スクリーンショット 2025-06-16 2 03 07" src="https://github.com/user-attachments/assets/3df379c3-28f6-4f3a-b198-bb4f7858c62b" />

Flaskサーバーを起動すると、`.apdf` の全文検索とPDFプレビューが可能です。

```bash
python app/server.py
```

ブラウザで開く：  
```
http://localhost:5000/static/index.html
```

- キーワード検索でヒットした `.apdf` を一覧表示  
- クリックで即プレビュー  

---

## 📁 ディレクトリ構成

```
.
├── app/
│   ├── ai_openai.py              ← OpenAI連携＆context生成
│   ├── generate_pdf.py           ← CLIから契約書生成
│   ├── render.py                 ← Jinja2でPDF描画
│   ├── server.py                 ← Flaskによる検索＆プレビュー
│   ├── template_prompts.py       ← 各契約テンプレートのsystem prompt定義 
│   └── templates/
│       ├── rental_agreement.tpl
│       └── outsourcing_agreement.tpl
├── contracts/                    ← 自動生成・検索対象の .apdf 格納先
├── output/                       ← CLI生成時のPDF/TXT/.apdf 保存先
├── static/
│   └── index.html                ← Vue.js + UI（PDF検索＆プレビュー）
├── requirements.txt
└── README.md

```

---
---

## 📚 関連研究・実績

本ツールの構造検証機能には、岡崎 友哉（Tomoya Okazaki）によって提案された構造仕様言語 `.janicre` を応用しています。

- **論文**:  
  Okazaki, T. (2025). *A Log-Scale, Reversible Semantic-Commit Manifest for Multi-Agent Software Reasoning*. [Zenodo]. https://doi.org/10.5281/zenodo.15466186  

この研究は、LLMと人間のインタラクションを形式化・強化するための構造的記述スキーマの設計に関するものであり、  
本プロジェクトでは `.janicre` に基づいたスキーマ検証を通じて、**対話可能で構造的な契約書生成プロセスの実現**を図っています。


## 🤖 使用技術

- Python 3.9+  
- [OpenAI GPT-4](https://platform.openai.com/)  
- [Jinja2](https://palletsprojects.com/p/jinja/)  
- [WeasyPrint](https://weasyprint.org/)（PDFレンダリング）  
- [Flask](https://flask.palletsprojects.com/)（検索API）  
- [Vue.js](https://vuejs.org/)（フロントエンド）

---

## 📬 今後の展望

- CLIで対話式モード（契約タイプ選択やプレビュー）  
- PDFスタイルカスタマイズ（フォント・印鑑欄など）  
- BLOBストアやDB連携による `.apdf` 管理  
- 英語対応、Word出力などの拡張

---

## 🧠 作者

岡崎 友哉（Tomoya Okazaki）  
お問い合わせ: [tomoya@anime-create.com]  

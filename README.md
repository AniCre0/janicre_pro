
# 📄 Contract AI Agent

AIを活用して、CLI上で日本語の契約書（賃貸契約書・業務委託契約書）を自動生成・PDF出力するツールです。

## 🚀 特徴

- ✅ OpenAI GPTを用いた契約書自動生成（自然言語→構造化情報）
- ✅ Jinja2テンプレートで契約書を動的レンダリング
- ✅ PDFファイルとして出力・保存
- ✅ CLIで簡単操作

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

```env
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

出力されたPDFは `output/契約書_日付.pdf` に保存されます。

---

## 📁 ディレクトリ構成

```
.
├── ai_openai.py            # OpenAIとのインターフェース
├── generate_pdf.py         # CLIから契約書PDFを生成するメインスクリプト
├── templates/
│   ├── rental_agreement.tpl         # 賃貸契約書テンプレート
│   └── outsourcing_agreement.tpl    # 業務委託契約書テンプレート
├── output/                 # 生成されたPDFファイル保存先
├── requirements.txt
└── README.md
```

---

## 🤖 使用技術

- Python 3.9+
- [OpenAI GPT-4](https://platform.openai.com/)
- [Jinja2](https://palletsprojects.com/p/jinja/)
- [WeasyPrint](https://weasyprint.org/)（PDFレンダリング）

---

## 📬 今後の展望

- CLIで契約タイプ選択可能な対話式モードの実装
- PDFスタイルのカスタマイズ（フォント・印鑑欄追加など）
- 英語対応、Word出力などの拡張

---

## 🧠 作者

岡崎 友哉（Tomoya Okazaki）  
お問い合わせ: [tomoya@anime-create.com]  

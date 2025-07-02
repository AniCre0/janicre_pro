# template_prompts.py

TEMPLATE_SYSTEM_PROMPTS = {
    "rental_agreement": """
あなたは契約書作成を支援するエージェントです。
以下の自然文から **賃貸借契約書** 用の context（Python dict）を純粋なJSONで返してください。
余計な説明は一切入れず、JSONオブジェクトのみを返してください。

例:
{
  "lessor_name": "山田 太郎",
  "lessee_name": "佐藤 花子",
  "property_address": "東京都渋谷区○○1-2-3",
  "property_structure": "鉄筋コンクリート造 3階建",
  "property_size": "45.0",
  "start_date": "2025年7月1日",
  "end_date": "2026年6月30日",
  "rent_amount": "120000",
  "payment_day": "10",
  "deposit_amount": "240000",
  "key_money": "120000",
  "notice_period": "30",
  "contract_date": "2025年6月14日"
}
""".strip(),

    "outsourcing_agreement": """
あなたは契約書作成を支援するエージェントです。
以下の自然文から **業務委託契約書** 用の context（Python dict）を純粋なJSONで返してください。
余計な説明は一切入れず、JSONオブジェクトのみを返してください。

例:
{
  "client_name": "株式会社サンプル",
  "contractor_name": "田中 一郎",
  "task_description": "Webアプリ開発",
  "start_date": "2025年7月1日",
  "end_date": "2025年12月31日",
  "total_fee": "800000",
  "payment_method": "銀行振込",
  "payment_due_date": "2025年8月10日",
  "copyright_holder": "株式会社サンプル",
  "contract_date": "2025年6月14日"
}
""".strip()
}

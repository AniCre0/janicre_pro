#!/usr/bin/env python3
# generate_pdf.py

import sys
import os

from ai_openai import generate_contract_context
from render import render_contract
from janicre_schema import load_schema, validate

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("❌ 使い方: python generate_pdf.py [rental|outsourcing] \"自然文\"")
        sys.exit(1)

    doc_type = sys.argv[1].lower()
    prompt = sys.argv[2]

    # テンプレート種別マッピング
    TEMPLATE_MAP = {
        "rental": "rental_agreement",
        "outsourcing": "outsourcing_agreement"
    }
    template_type = TEMPLATE_MAP.get(doc_type)
    if not template_type:
        print("❌ 契約タイプは 'rental' か 'outsourcing' のどちらかを指定してください。")
        sys.exit(1)

    # テンプレートと出力先パス決定
    tpl = f"{template_type}.tpl"
    output_path = f"output/{template_type}.pdf"

    print(f"🧾 契約タイプ: {doc_type} ({template_type})")
    print(f"📝 入力内容: {prompt}")

    # GPTでcontext生成
    context = generate_contract_context(prompt, template_type=template_type)

    # janicreスキーマで不足チェック
    schema = load_schema(f"{template_type}.janicre")
    missing = validate(context, schema)

    while missing:
        print(f"⚠️ 欠落フィールド: {', '.join(missing)}")
        print("以下の形式で補足してください（空行で完了）:")
        print("例: total_fee: 300000")

        while True:
            line = input("> ").strip()
            if not line:
                break
            try:
                key, value = [s.strip() for s in line.split(":", 1)]
                context[key] = value
            except ValueError:
                print("💡 'key: value' の形式で入力してください")

        missing = validate(context, schema)

    os.makedirs("output", exist_ok=True)
    render_contract(tpl, context, output_path)
    print(f"✅ PDF を出力しました: {output_path}")

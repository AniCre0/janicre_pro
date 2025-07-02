#!/usr/bin/env python3
# generate_interactive.py – GPT ↔ janicre 双方向やり取り
# ❶ 入力文から契約書タイプを自動判定
# ❷ 必須項目を GPT に JSON で生成させる（創作禁止）
# ❸ 欠落項目があれば GPT 経由で聞き返す
# ❹ すべて埋まったら PDF (.pdf + .apdf) を出力

from __future__ import annotations
import sys
import os
from typing import Dict, List

from ai_openai import client, generate_contract_context
from render import render_contract
from janicre_schema import load_schema, validate, normalize, _build_alias_map   # _build_alias_map も利用
# -------------------------------------------------------------
# ユーティリティ
# -------------------------------------------------------------
def get_japanese_name(key: str, schema: Dict) -> str:
    """スキーマの aliases から代表となる日本語名を返す"""
    for fld in schema["fields"]:
        if fld["name"] == key:
            return fld.get("aliases", [key])[0]
    return key

# -------------------------------------------------------------
# 1. 契約タイプを判定（rental / outsourcing） ※temperature=0
# -------------------------------------------------------------
def classify_doc_type(text: str) -> str:
    system_msg = (
        "あなたは契約書作成アシスタントです。"
        "次の文章が『賃貸借契約書』を求めている場合は rental、"
        "『業務委託契約書』を求めている場合は outsourcing と、"
        "必ず小文字一語のみで回答してください。他の語や説明は一切不要です。"
    )
    try:
        res = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user",   "content": text}
            ],
            temperature=0.0
        )
        choice = res.choices[0].message.content.strip().lower()
        if choice in ("rental", "outsourcing"):
            return choice
    except Exception:
        pass  # API エラー時はフォールバックへ
    # フォールバック：キーワード判定
    if any(k in text for k in ("家賃", "賃料", "貸主", "借主", "物件")):
        return "rental"
    return "outsourcing"

# -------------------------------------------------------------
# 2. 欠落項目を尋ねる自然言語文を GPT に生成
# -------------------------------------------------------------
def ask_user_for_missing(missing: List[str], schema: Dict) -> str:
    japanized = "、".join(get_japanese_name(f, schema) for f in missing)
    system_msg = (
        "あなたは契約書作成アシスタントです。"
        f"次の不足項目をユーザーに丁寧に尋ねる一文を日本語で返してください。"
        "例示や余計な説明は不要。一文だけ："
    )
    user_msg = f"不足項目: {japanized}"
    try:
        res = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": system_msg},
                      {"role": "user",   "content": user_msg}],
            temperature=0.0
        )
        return res.choices[0].message.content.strip()
    except Exception:
        return f"以下の情報が不足しています：{japanized}。ご入力ください。"

# -------------------------------------------------------------
# 3. strict_JSON_suffix – GPT への創作禁止・JSON縛り
# -------------------------------------------------------------
STRICT_SUFFIX = (
    "\n\n【重要ルール】\n"
    "1. 与えられた情報以外は一切追加してはいけません。\n"
    "2. 推測・創作は禁止。\n"
    "3. 返答は必ず JSON オブジェクトのみ。```json ... ``` で囲んでください。\n"
    "4. 説明文やコメントは禁止。\n"
)

# -------------------------------------------------------------
# 4. メイン
# -------------------------------------------------------------
def main() -> None:
    if len(sys.argv) < 2:
        print("❌ 使い方: python generate_interactive.py \"契約内容の自然文\"")
        sys.exit(1)

    original_prompt = sys.argv[1]

    # --- 初回タイプ判定 ---
    doc_type = classify_doc_type(original_prompt)
    print(f"🧾 判定された契約タイプ: {doc_type}")

    template_map = {"rental": "rental_agreement",
                    "outsourcing": "outsourcing_agreement"}
    template_type = template_map[doc_type]
    tpl_path = f"{template_type}.tpl"
    output_path = f"output/{template_type}.pdf"
    schema = load_schema(f"{template_type}.janicre")

    # 補足履歴
    supplements: List[str] = []

    # --- 1st GPT 呼び出し ---
    prompt_for_gpt = original_prompt + STRICT_SUFFIX
    context = generate_contract_context(prompt_for_gpt, template_type)
    context = normalize(context, schema)
    missing = validate(context, schema)

    # --- ループ：欠落がある限り ---
    while missing:
        # ユーザーへ質問
        print(ask_user_for_missing(missing, schema))
        answer = input(">> ").strip()
        if not answer:
            print("入力が無いので終了します。")
            sys.exit(1)
        supplements.append(answer)

        # 入力全文で doc_type を再判定（必要ならテンプレート切替）
        combined_text = original_prompt + "\n".join(supplements)
        new_type = classify_doc_type(combined_text)
        if new_type != doc_type:
            doc_type = new_type
            template_type = template_map[doc_type]
            tpl_path = f"{template_type}.tpl"
            output_path = f"output/{template_type}.pdf"
            schema = load_schema(f"{template_type}.janicre")
            print(f"🔄 契約タイプを再判定し更新: {doc_type}")

        # GPT へ再投げ
        prompt_for_gpt = (
            original_prompt +
            "\n\n追加情報:\n" + "\n".join(supplements) +
            STRICT_SUFFIX
        )
        context = generate_contract_context(prompt_for_gpt, template_type)
        context = normalize(context, schema)
        missing = validate(context, schema)

    # --- 想定外キーの混入チェック ---
    alias_map, allowed_keys = _build_alias_map(schema)
    unexpected = [k for k in context.keys() if k not in allowed_keys]
    if unexpected:
        raise ValueError(f"想定外キーを検出: {unexpected}")

    # --- PDF & .apdf 出力 ---
    os.makedirs("output", exist_ok=True)
    render_contract(tpl_path, context, output_path)
    print(f"✅ PDF を出力しました: {output_path}")

# -------------------------------------------------------------
if __name__ == "__main__":
    main()

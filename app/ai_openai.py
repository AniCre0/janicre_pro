from dotenv import load_dotenv
load_dotenv()

import os
import json
import re
from langfuse import get_client
from openai import OpenAI, OpenAIError
from template_prompts import TEMPLATE_SYSTEM_PROMPTS  # ← これだけ

client = OpenAI()
langfuse = get_client()

def generate_contract_context(prompt: str, template_type="rental_agreement") -> dict:
    trace_id = langfuse.create_trace_id()
    system_prompt = TEMPLATE_SYSTEM_PROMPTS.get(template_type)
    if not system_prompt:
        raise ValueError(f"未定義のテンプレートタイプです: {template_type}")

    with langfuse.start_as_current_span(
        name="generate_context",
        trace_context={"trace_id": trace_id}
    ) as span:
        try:
            res = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )
        except OpenAIError as e:
            print("🛑 OpenAI API呼び出しエラー:", e)
            raise

        raw = res.to_dict()
        print("🔁 OpenAI full response:")
        print(json.dumps(raw, indent=2, ensure_ascii=False))

        choices = raw.get("choices", [])
        if not choices or not choices[0].get("message", {}).get("content"):
            raise ValueError("OpenAIからの返答が空です")

        raw_reply = choices[0]["message"]["content"]
        print("🔁 受信したreply (raw):", repr(raw_reply))

        # コードブロック ```json ... ``` を除去
        reply = re.sub(r"^```json\s*|\s*```$", "", raw_reply.strip(), flags=re.DOTALL)

        span.update(input=prompt, output=reply)
        langfuse.flush()
        print("🧠 trace URL:", langfuse.get_trace_url(trace_id=trace_id))

        try:
            return json.loads(reply)
        except json.JSONDecodeError as e:
            print("🛑 JSONデコード失敗:", e)
            print("🔁 失敗したreply:", repr(reply))
            raise

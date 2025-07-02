from dotenv import load_dotenv
load_dotenv()

from langfuse import get_client

# CLIや短命スクリプトでも動くように .env から client を初期化
langfuse = get_client()

# (省略可) 固有の trace ID を作る場合は seed も使える
trace_id = langfuse.create_trace_id()  # -> 32文字の16進ID

# span を開始し trace_context に trace_id を指定
with langfuse.start_as_current_span(
    name="hello-world",
    trace_context={"trace_id": trace_id}
) as span:
    # 入力・出力を記録
    span.update(input="こんにちは", output="Langfuse バージョン3！")
    print("✅ span 内の trace_id:", span.trace_id)

# 短いスクリプトでは flush を忘れずに
langfuse.flush()

print("✅ トレース完了:", trace_id)
print("✅ Langfuse URL:", langfuse.get_trace_url(trace_id=trace_id))

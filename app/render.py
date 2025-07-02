# app/render.py

import os
import zipfile
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

def render_contract(template_name: str, context: dict, output_target: str):
    """
    template_name: 'rental_agreement.tpl' などテンプレートファイル名
    context: Jinja2 に渡す辞書
    output_target: 
      ・ディレクトリを指定 → <dir>/<tpl>_<timestamp>.apdf
      ・.apdf 指定 → 指定ファイル名で出力
      ・.pdf 指定 → 同ディレクトリに同ベース名.apdf を出力
    """

    # 拡張子を小文字でチェック
    lower = output_target.lower()
    name, ext = os.path.splitext(output_target)

    if lower.endswith(".apdf"):
        # .apdf 指定 → そのままファイル名として使う
        output_dir = os.path.dirname(output_target) or "."
        apdf_filename = os.path.basename(output_target)
        use_timestamp = False

    elif lower.endswith(".pdf"):
        # .pdf 指定 → 同じディレクトリに .apdf を出力
        output_dir = os.path.dirname(output_target) or "."
        base = os.path.basename(name)
        apdf_filename = f"{base}.apdf"
        use_timestamp = False

    else:
        # ディレクトリ指定 → timestamp付きファイル名を生成
        output_dir = output_target
        base = os.path.splitext(template_name)[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        apdf_filename = f"{base}_{timestamp}.apdf"
        use_timestamp = True

    # 出力ディレクトリを作成
    os.makedirs(output_dir, exist_ok=True)

    # テンプレート読み込み
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)
    rendered_html = template.render(context)

    # 一時PDF/TXTファイル名ベース
    if use_timestamp:
        file_base = os.path.splitext(apdf_filename)[0]
    else:
        # 同名が上書きされるのを避けるなら、ここで timestamp を付与できます
        file_base = os.path.splitext(apdf_filename)[0]

    pdf_path = os.path.join(output_dir, f"{file_base}.pdf")
    txt_path = os.path.join(output_dir, f"{file_base}.txt")
    apdf_path = os.path.join(output_dir, apdf_filename)

    # PDF出力
    HTML(string=rendered_html).write_pdf(pdf_path)
    print(f"✅ PDF生成: {pdf_path}")

    # テキスト出力
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)
    print(f"📝 テキスト生成: {txt_path}")

    # .apdf (ZIP) 出力
    with zipfile.ZipFile(apdf_path, "w", compression=zipfile.ZIP_DEFLATED) as apdf:
        apdf.write(pdf_path, arcname="document.pdf")
        apdf.write(txt_path, arcname="content.txt")
    print(f"📦 .apdf生成完了: {apdf_path}")

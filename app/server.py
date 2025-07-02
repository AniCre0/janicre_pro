# app/server.py

import os
import zipfile
from flask import Flask, request, jsonify, send_file, Response
from io import BytesIO

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONTRACT_DIR = os.path.join(BASE_DIR, "output")


@app.route("/search")
def search():
    keyword = request.args.get("keyword", "").strip().lower()
    results = []

    for filename in os.listdir(CONTRACT_DIR):
        if not filename.endswith(".apdf"):
            continue

        apdf_path = os.path.join(CONTRACT_DIR, filename)
        try:
            with zipfile.ZipFile(apdf_path) as zf:
                # content.txt があれば中身を読む
                if "content.txt" in zf.namelist():
                    text = zf.read("content.txt").decode("utf-8")
                    if not keyword or keyword in text.lower():
                        results.append({
                            "name": filename,
                            "url": f"/view?file={filename}"
                        })
        except zipfile.BadZipFile:
            # ZIP が壊れていたらスキップ
            continue

    return jsonify(results)


@app.route("/view")
def view():
    filename = request.args.get("file", "")
    if not filename.endswith(".apdf"):
        return "Invalid file", 400

    apdf_path = os.path.join(CONTRACT_DIR, filename)
    if not os.path.isfile(apdf_path):
        return "File not found", 404

    # .apdf を開いて document.pdf をバイトで取り出す
    with zipfile.ZipFile(apdf_path) as zf:
        try:
            pdf_bytes = zf.read("document.pdf")
        except KeyError:
            return "PDF not found in archive", 500

    # BytesIO でレスポンスを返却
    return send_file(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        download_name=filename.replace(".apdf", ".pdf")
    )


if __name__ == "__main__":
    # debug モード＋リローダーで開発効率UP
    app.run(debug=True, use_reloader=True)

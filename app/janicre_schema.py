"""
janicre_schema.py – スキーマ読込・正規化・バリデーション
"""

from __future__ import annotations
import json
import pathlib
from typing import Dict, List, Tuple


# -------------------------------------------------------------
# スキーマ読み込み
# -------------------------------------------------------------
def load_schema(name: str) -> Dict:
    """
    app/schema/{name}.json を読み込んで dict で返す
    例: name="outsourcing_agreement.janicre" → app/schema/outsourcing_agreement.janicre.json
    """
    base = pathlib.Path(__file__).parent
    path = base / "schema" / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"スキーマが見つかりません: {path}")
    with path.open(encoding="utf-8") as f:
        return json.load(f)


# -------------------------------------------------------------
# 正規化：日本語キー → 正式キー への変換
# -------------------------------------------------------------
def _build_alias_map(schema: Dict) -> Tuple[Dict[str, str], List[str]]:
    alias_to_canonical: Dict[str, str] = {}
    canonicals: List[str] = []

    for fld in schema.get("fields", []):
        canonical = fld["name"]
        canonicals.append(canonical)
        alias_to_canonical[canonical] = canonical
        for alias in fld.get("aliases", []):
            alias_to_canonical[alias] = canonical

    return alias_to_canonical, canonicals


def normalize(data: Dict, schema: Dict) -> Dict:
    alias_map, _ = _build_alias_map(schema)
    return {alias_map.get(k, k): v for k, v in data.items()}


# -------------------------------------------------------------
# バリデーション
# -------------------------------------------------------------
def validate(data: Dict, schema: Dict) -> List[str]:
    missing: List[str] = []
    for fld in schema.get("fields", []):
        if not fld.get("required"):
            continue
        key = fld["name"]
        val = data.get(key, "")
        if isinstance(val, str):
            val = val.strip()
        if not val or (isinstance(val, str) and "未定" in val):
            missing.append(key)
    return missing


# -------------------------------------------------------------
# CLI テスト
# -------------------------------------------------------------
if __name__ == "__main__":
    schema = load_schema("outsourcing_agreement.janicre")
    sample = {
        "クライアント名": "株式会社ABC",
        "受託者名": "山本 太郎",
        "業務内容": "Webアプリ開発"
    }
    norm = normalize(sample, schema)
    print("★ 正規化結果:", json.dumps(norm, ensure_ascii=False, indent=2))
    print("★ 欠落:", validate(norm, schema))

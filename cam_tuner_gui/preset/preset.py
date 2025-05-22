"""파라미터 프리셋 저장/불러오기 모듈."""

from __future__ import annotations

import json


def save_json(params: dict, path: str) -> None:
    """파라미터 딕셔너리를 JSON 파일로 저장한다."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(params, f, ensure_ascii=False, indent=2)


def load_json(path: str) -> dict:
    """JSON 파일에서 파라미터를 읽어 반환한다."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

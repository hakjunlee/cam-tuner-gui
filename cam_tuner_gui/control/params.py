"""카메라 파라미터 매핑 및 제어 함수."""

from __future__ import annotations

import cv2
from typing import Any, Dict

class ParamMap:
    """슬라이더와 디바이스 파라미터 사이의 매핑을 관리한다."""

    def __init__(self) -> None:
        """매핑 초기화."""
        self._map: Dict[str, str] = {
            "exposure": "exposure_absolute",
            "gain": "gain",
        }

    def get(self, name: str):
        """파라미터 정보를 반환한다."""
        return self._map.get(name)

PARAM_CV2_MAP = {
    "exposure_absolute": cv2.CAP_PROP_EXPOSURE,
    "gain": cv2.CAP_PROP_GAIN,
}


def set_param(device: Any, param_id: str, value) -> None:
    """주어진 파라미터 ID에 값을 설정한다."""
    prop = PARAM_CV2_MAP.get(param_id)
    if prop is None:
        return
    cap = getattr(device, "cap", None)
    if cap is not None:
        cap.set(prop, value)

"""카메라 파라미터 매핑 및 제어 함수."""

from __future__ import annotations

import cv2

class ParamMap:
    """슬라이더와 디바이스 파라미터 사이의 매핑을 관리한다."""

    def __init__(self) -> None:
        """매핑 초기화."""
        self._map = {
            "exposure_abs": cv2.CAP_PROP_EXPOSURE,
            "auto_exposure": cv2.CAP_PROP_AUTO_EXPOSURE,
            "gain": cv2.CAP_PROP_GAIN,
            "gamma": cv2.CAP_PROP_GAMMA,
            "contrast": cv2.CAP_PROP_CONTRAST,
        }

    def get(self, name: str):
        """파라미터 정보를 반환한다."""
        return self._map.get(name)

def set_param(capture: cv2.VideoCapture, param_id: str, value) -> None:
    """주어진 파라미터 ID에 값을 설정한다."""
    prop = ParamMap().get(param_id)
    if prop is None:
        raise KeyError(f"Unknown parameter: {param_id}")
    if not capture.set(prop, value):
        raise RuntimeError(f"Failed to set {param_id} to {value}")


def get_param(capture: cv2.VideoCapture, param_id: str):
    """현재 장치에서 주어진 파라미터 값을 읽어 반환한다."""
    prop = ParamMap().get(param_id)
    if prop is None:
        raise KeyError(f"Unknown parameter: {param_id}")
    return capture.get(prop)


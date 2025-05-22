"""카메라 장치를 추상화하는 모듈."""

from __future__ import annotations

import cv2
from typing import Optional

class CameraDevice:
    """단일 카메라 장치를 제어하고 프레임을 스트림하는 클래스."""

    def __init__(self, device_id: str) -> None:
        """디바이스 ID를 받아 초기화."""
        self.device_id = device_id
        self.cap: Optional[cv2.VideoCapture] = None

    def start_stream(self) -> None:
        """카메라 스트림을 시작한다."""
        if self.cap is None:
            self.cap = cv2.VideoCapture(self.device_id)
        if not self.cap.isOpened():
            raise RuntimeError(f"Unable to open device {self.device_id}")

    def stop_stream(self) -> None:
        """카메라 스트림을 중지한다."""
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def read_frame(self):
        """한 프레임을 반환한다."""
        if self.cap is None:
            raise RuntimeError("Stream not started")
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

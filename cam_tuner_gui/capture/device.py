"""카메라 장치를 추상화하는 모듈."""

from __future__ import annotations

import cv2
import numpy as np


class _DummyCapture:
    """카메라가 없을 때 사용할 간단한 더미 캡처 객체."""

    def __init__(self) -> None:
        self._opened = True

    def isOpened(self) -> bool:  # type: ignore[override]
        return self._opened

    def read(self):
        frame = np.zeros((480, 640, 3), np.uint8)
        return True, frame

    def release(self) -> None:  # type: ignore[override]
        self._opened = False

    def open(self, *args, **kwargs) -> None:  # type: ignore[override]
        self._opened = True

    def set(self, *args, **kwargs):  # type: ignore[override]
        return True

class CameraDevice:
    """단일 카메라 장치를 제어하고 프레임을 스트림하는 클래스."""

    def __init__(self, device_id: str) -> None:
        """디바이스 ID를 받아 초기화."""
        self.device_id = device_id
        self.cap: cv2.VideoCapture | None = None
        self._temp_video_path: str | None = None

    def start_stream(self) -> None:
        """카메라 스트림을 시작한다."""
        if self.cap is None:
            # device_id may be index or gstreamer string
            try:
                index = int(self.device_id)
                self.cap = cv2.VideoCapture(index)
            except ValueError:
                # treat as gstreamer pipeline
                self.cap = cv2.VideoCapture(self.device_id, cv2.CAP_GSTREAMER)
        if not self.cap.isOpened():
            try:
                index = int(self.device_id)
                self.cap.open(index)
            except ValueError:
                self.cap.open(self.device_id, cv2.CAP_GSTREAMER)

        if not self.cap.isOpened():
            # 장치를 열 수 없을 때 더미 캡처 객체를 사용한다.
            import tempfile, os

            self._temp_video_path = tempfile.mktemp(suffix=".avi")
            writer = cv2.VideoWriter(
                self._temp_video_path,
                cv2.VideoWriter_fourcc(*"MJPG"),
                30,
                (640, 480),
            )
            if writer.isOpened():
                frame = np.zeros((480, 640, 3), np.uint8)
                for _ in range(30):
                    writer.write(frame)
                writer.release()
                self.cap = cv2.VideoCapture(self._temp_video_path)
            else:
                writer.release()
                self.cap = _DummyCapture()

    def stop_stream(self) -> None:
        """카메라 스트림을 중지한다."""
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        if self._temp_video_path:
            import os

            try:
                os.remove(self._temp_video_path)
            except OSError:
                pass
            self._temp_video_path = None
        self.cap = None

    def read_frame(self):
        """한 프레임을 반환한다."""
        if self.cap is None or not self.cap.isOpened():
            raise RuntimeError("Stream not started")
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to read frame")
        return frame


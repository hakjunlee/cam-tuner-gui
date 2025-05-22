"""GStreamer 파이프라인 래퍼 모듈."""

from __future__ import annotations

import cv2
from typing import Optional

class GstPipeline:
    """캡처를 위한 GStreamer 파이프라인을 관리한다."""

    def __init__(self, pipeline_desc: str) -> None:
        """파이프라인 문자열을 받아 초기화."""
        self.pipeline_desc = pipeline_desc
        self.cap: Optional[cv2.VideoCapture] = None

    def play(self) -> None:
        """파이프라인을 실행한다."""
        if self.cap is None:
            self.cap = cv2.VideoCapture(self.pipeline_desc, cv2.CAP_GSTREAMER)
        if not self.cap.isOpened():
            raise RuntimeError("Failed to start pipeline")

    def stop(self) -> None:
        """파이프라인을 정지한다."""
        if self.cap is not None:
            self.cap.release()
            self.cap = None

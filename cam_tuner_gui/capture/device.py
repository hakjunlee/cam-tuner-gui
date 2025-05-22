"""카메라 장치를 추상화하는 모듈."""

from __future__ import annotations

class CameraDevice:
    """단일 카메라 장치를 제어하고 프레임을 스트림하는 클래스."""

    def __init__(self, device_id: str) -> None:
        """디바이스 ID를 받아 초기화."""
        # TODO: 장치 초기화 로직 구현
        pass

    def start_stream(self) -> None:
        """카메라 스트림을 시작한다."""
        # TODO: 스트림 시작 구현
        pass

    def stop_stream(self) -> None:
        """카메라 스트림을 중지한다."""
        # TODO: 스트림 중지 구현
        pass

    def read_frame(self):
        """한 프레임을 반환한다."""
        # TODO: 프레임 읽기 구현
        pass

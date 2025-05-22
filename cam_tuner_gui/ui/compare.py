"""영상 비교용 도킹 위젯."""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QWidget

from ..metric import metrics


class CompareDock(QWidget):
    """두 스트림을 나란히 비교하는 도킹 위젯."""

    def __init__(self) -> None:
        """위젯 초기화."""
        super().__init__()

        self.left_label = QLabel()
        self.right_label = QLabel()
        self.left_label.setAlignment(Qt.AlignCenter)
        self.right_label.setAlignment(Qt.AlignCenter)

        image_layout = QHBoxLayout()
        image_layout.addWidget(self.left_label)
        image_layout.addWidget(self.right_label)

        self.mtf_label = QLabel("MTF50: N/A | N/A")
        self.mtf_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addLayout(image_layout)
        layout.addWidget(self.mtf_label)
        self.setLayout(layout)

        self._left_image: Optional[QImage] = None
        self._right_image: Optional[QImage] = None

    def _to_qimage(self, frame) -> QImage:
        """NumPy 배열이나 이미지를 ``QImage`` 로 변환한다."""
        if isinstance(frame, QImage):
            return frame

        # ``frame`` 이 NumPy 배열이라고 가정
        import numpy as np

        if frame is None or not isinstance(frame, np.ndarray):
            return QImage()

        if frame.ndim == 2:  # grayscale
            h, w = frame.shape
            return QImage(
                frame.data, w, h, w, QImage.Format_Grayscale8
            ).copy()

        if frame.ndim == 3:
            h, w, c = frame.shape
            if c == 3:
                fmt = QImage.Format_BGR888
            else:  # assume RGBA
                fmt = QImage.Format_RGBA8888
            return QImage(
                frame.data, w, h, c * w, fmt
            ).copy()

        return QImage()

    def set_images(self, left, right) -> None:
        """좌/우 이미지 업데이트."""

        self._left_image = self._to_qimage(left)
        self._right_image = self._to_qimage(right)

        self.left_label.setPixmap(QPixmap.fromImage(self._left_image))
        self.right_label.setPixmap(QPixmap.fromImage(self._right_image))

        # MTF50 계산
        mtf_left = self._calc_mtf50_safe(left)
        mtf_right = self._calc_mtf50_safe(right)
        self.mtf_label.setText(f"MTF50: {mtf_left:.2f} | {mtf_right:.2f}")

    def _calc_mtf50_safe(self, img) -> float:
        try:
            return metrics.calc_mtf50(img)
        except Exception:
            return 0.0

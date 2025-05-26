"""영상 비교용 도킹 위젯."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QDockWidget, QLabel, QHBoxLayout, QWidget


class CompareDock(QDockWidget):
    """두 스트림을 나란히 비교하는 도킹 위젯."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """위젯 초기화."""
        super().__init__("Compare", parent)

        self._left_label = QLabel()
        self._right_label = QLabel()
        self._left_label.setAlignment(Qt.AlignCenter)
        self._right_label.setAlignment(Qt.AlignCenter)

        container = QWidget(self)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._left_label)
        layout.addWidget(self._right_label)
        self.setWidget(container)

    def set_images(self, left, right) -> None:
        """좌/우 이미지 업데이트."""
        self._update_label(self._left_label, left)
        self._update_label(self._right_label, right)

    def _update_label(self, label: QLabel, image) -> None:
        """이미지를 QLabel에 설정한다."""
        if image is None:
            label.clear()
            return

        if isinstance(image, QPixmap):
            label.setPixmap(image)
            return

        if isinstance(image, QImage):
            pixmap = QPixmap.fromImage(image)
        else:
            # Assume ndarray from OpenCV (BGR or GRAY)
            height, width = image.shape[:2]
            if len(image.shape) == 2:
                qimage = QImage(
                    image.data, width, height, image.strides[0], QImage.Format_Grayscale8
                )
            else:
                qimage = QImage(
                    image.data, width, height, image.strides[0], QImage.Format_BGR888
                )
            pixmap = QPixmap.fromImage(qimage)
        label.setPixmap(pixmap)

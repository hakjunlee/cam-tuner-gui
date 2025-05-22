"""영상 비교용 도킹 위젯."""

from __future__ import annotations

from typing import Optional

import cv2
from PySide6 import QtGui, QtWidgets


class CompareDock(QtWidgets.QDockWidget):
    """두 스트림을 나란히 비교하는 도킹 위젯."""

    def __init__(self) -> None:
        """위젯 초기화."""
        super().__init__("Compare")
        self.left_label = QtWidgets.QLabel()
        self.right_label = QtWidgets.QLabel()
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.addWidget(self.left_label)
        layout.addWidget(self.right_label)
        self.setWidget(widget)

    def set_images(self, left, right) -> None:
        """좌/우 이미지 업데이트."""
        if left is not None:
            self.left_label.setPixmap(self._to_pixmap(left))
        if right is not None:
            self.right_label.setPixmap(self._to_pixmap(right))

    @staticmethod
    def _to_pixmap(img) -> QtGui.QPixmap:
        if img is None:
            return QtGui.QPixmap()
        if img.ndim == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h, w, ch = img.shape
            bytes_per_line = ch * w
            qimg = QtGui.QImage(img.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        else:
            h, w = img.shape
            bytes_per_line = w
            qimg = QtGui.QImage(img.data, w, h, bytes_per_line, QtGui.QImage.Format_Grayscale8)
        return QtGui.QPixmap.fromImage(qimg.copy())

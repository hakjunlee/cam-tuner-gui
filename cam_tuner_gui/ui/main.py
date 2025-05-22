"""메인 GUI 창을 정의한다."""

from __future__ import annotations

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from .compare import CompareDock


class MainWindow(QMainWindow):
    """애플리케이션의 주 윈도우."""

    def __init__(self) -> None:
        """UI 요소 초기화."""
        super().__init__()

        self.setWindowTitle("Camera Tuner")
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        central.setLayout(layout)

        self.compare = CompareDock()
        layout.addWidget(self.compare)

    def show(self) -> None:
        """윈도우 표시."""
        super().show()

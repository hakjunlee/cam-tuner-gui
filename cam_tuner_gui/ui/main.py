"""메인 GUI 창을 정의한다."""

from __future__ import annotations

from typing import Optional

from PySide6 import QtCore, QtWidgets

from ..metric.metrics import calc_snr


class MainWindow(QtWidgets.QMainWindow):
    """애플리케이션의 주 윈도우."""

    def __init__(self) -> None:
        """UI 요소 초기화."""
        super().__init__()
        self.setWindowTitle("Camera Tuner")
        self.label = QtWidgets.QLabel("SNR: N/A")
        central = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(central)
        layout.addWidget(self.label)
        self.setCentralWidget(central)

        self.current_image: Optional = None

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_metrics)

    def show(self) -> None:
        """윈도우 표시."""
        super().show()
        self.timer.start(1000)

    def update_metrics(self) -> None:
        if self.current_image is None:
            return
        snr = calc_snr(self.current_image)
        self.label.setText(f"SNR: {snr:.2f} dB")

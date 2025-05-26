"""메인 GUI 창을 정의한다."""

from __future__ import annotations

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget

from cam_tuner_gui.metric.metrics import calc_snr


class MainWindow(QMainWindow):
    """애플리케이션의 주 윈도우."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Camera Tuner")

        self._snr_label = QLabel("SNR: -- dB")
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(self._snr_label)
        self.setCentralWidget(container)

        self.device = None
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_metrics)

    def _update_metrics(self) -> None:
        if self.device is None:
            return
        frame = self.device.read_frame()
        if frame is None:
            return
        snr = calc_snr(frame)
        self._snr_label.setText(f"SNR: {snr:.2f} dB")

    def show(self) -> None:
        super().show()
        self._timer.start(1000)

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
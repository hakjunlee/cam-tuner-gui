"""메인 GUI 창을 정의한다."""

from __future__ import annotations

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from cam_tuner_gui.metric.metrics import calc_snr
from cam_tuner_gui.capture.device import CameraDevice
from cam_tuner_gui.control.params import set_param


class MainWindow(QMainWindow):
    """애플리케이션의 주 윈도우."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Camera Tuner")

        # Top control bar
        self._device_combo = QComboBox()
        self._device_combo.addItem("0")
        self._start_btn = QPushButton("Start")
        self._stop_btn = QPushButton("Stop")
        top_bar = QHBoxLayout()
        top_bar.addWidget(self._device_combo)
        top_bar.addWidget(self._start_btn)
        top_bar.addWidget(self._stop_btn)

        # Preview and snapshot area
        self._preview_label = QLabel()
        self._preview_label.setAlignment(Qt.AlignCenter)
        self._snapshot_label = QLabel()
        self._snapshot_label.setAlignment(Qt.AlignCenter)
        preview_row = QHBoxLayout()
        preview_row.addWidget(self._preview_label)
        preview_row.addWidget(self._snapshot_label)

        # Metrics
        self._snr_label = QLabel("SNR: -- dB")

        # Sliders for basic controls
        self._exp_slider = QSlider(Qt.Horizontal)
        self._exp_slider.setRange(1, 1000)
        self._exp_slider.setValue(100)
        self._gain_slider = QSlider(Qt.Horizontal)
        self._gain_slider.setRange(0, 255)
        controls_col = QVBoxLayout()
        controls_col.addWidget(QLabel("Exposure"))
        controls_col.addWidget(self._exp_slider)
        controls_col.addWidget(QLabel("Gain"))
        controls_col.addWidget(self._gain_slider)

        self._snapshot_btn = QPushButton("Snapshot")
        self._export_btn = QPushButton("Export Report")
        bottom_bar = QHBoxLayout()
        bottom_bar.addWidget(self._snapshot_btn)
        bottom_bar.addWidget(self._export_btn)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addLayout(top_bar)
        layout.addLayout(preview_row)
        layout.addWidget(self._snr_label)
        layout.addLayout(controls_col)
        layout.addLayout(bottom_bar)
        self.setCentralWidget(container)

        self.device = None
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_frame)

        self._start_btn.clicked.connect(self._start_stream)
        self._stop_btn.clicked.connect(self._stop_stream)
        self._snapshot_btn.clicked.connect(self._take_snapshot)
        self._exp_slider.valueChanged.connect(self._apply_exposure)
        self._gain_slider.valueChanged.connect(self._apply_gain)

    def _ndarray_to_pixmap(self, frame) -> QPixmap:
        height, width = frame.shape[:2]
        if len(frame.shape) == 2:
            qimage = QImage(frame.data, width, height, frame.strides[0], QImage.Format_Grayscale8)
        else:
            qimage = QImage(frame.data, width, height, frame.strides[0], QImage.Format_BGR888)
        return QPixmap.fromImage(qimage)

    def _update_frame(self) -> None:
        if self.device is None:
            return
        frame = self.device.read_frame()
        pixmap = self._ndarray_to_pixmap(frame)
        self._preview_label.setPixmap(pixmap)
        snr = calc_snr(frame)
        self._snr_label.setText(f"SNR: {snr:.2f} dB")

    def _start_stream(self) -> None:
        if self.device is None:
            device_id = self._device_combo.currentText()
            self.device = CameraDevice(device_id)
        self.device.start_stream()
        self._apply_exposure(self._exp_slider.value())
        self._apply_gain(self._gain_slider.value())
        self._timer.start(30)

    def _stop_stream(self) -> None:
        if self.device:
            self.device.stop_stream()
        self._timer.stop()

    def _take_snapshot(self) -> None:
        if self.device is None:
            return
        frame = self.device.read_frame()
        self._snapshot_label.setPixmap(self._ndarray_to_pixmap(frame))

    def _apply_exposure(self, value: int) -> None:
        if self.device and self.device.cap and self.device.cap.isOpened():
            try:
                set_param(self.device.cap, "auto_exposure", 1)
                set_param(self.device.cap, "exposure_abs", value)
            except Exception:
                pass

    def _apply_gain(self, value: int) -> None:
        if self.device and self.device.cap and self.device.cap.isOpened():
            try:
                set_param(self.device.cap, "gain", value)
            except Exception:
                pass

    def show(self) -> None:
        super().show()
        # Stream is started via button

    def closeEvent(self, event) -> None:  # type: ignore[override]
        self._stop_stream()
        super().closeEvent(event)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

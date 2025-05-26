"""두 카메라 스트림을 비교하기 위한 윈도우."""

from __future__ import annotations

from typing import List, Dict

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QImage, QPixmap
import cv2

from cam_tuner_gui.capture.device import CameraDevice
from cam_tuner_gui.metric import metrics as m
from cam_tuner_gui.report.builder import render_html, export_pdf


THRESHOLDS = {
    "mtf50": 1.0,
    "snr": 20.0,
    "flicker": 10.0,
    "lapvar": 50.0,
    "motion_blur": 5.0,
}


class CompareWindow(QMainWindow):
    """두 카메라 성능 비교용 메인 윈도우."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Camera Tuner Compare")

        self.cam1 = None
        self.cam2 = None

        self._combo1 = QComboBox()
        self._combo1.addItem("0")
        self._combo2 = QComboBox()
        self._combo2.addItem("1")

        self._start1 = QPushButton("Start")
        self._stop1 = QPushButton("Stop")
        self._start2 = QPushButton("Start")
        self._stop2 = QPushButton("Stop")

        top = QHBoxLayout()
        top.addWidget(self._combo1)
        top.addWidget(self._start1)
        top.addWidget(self._stop1)
        top.addSpacing(20)
        top.addWidget(self._combo2)
        top.addWidget(self._start2)
        top.addWidget(self._stop2)

        self._view1 = QLabel()
        self._view1.setAlignment(Qt.AlignCenter)
        self._view2 = QLabel()
        self._view2.setAlignment(Qt.AlignCenter)

        views = QHBoxLayout()
        views.addWidget(self._view1)
        views.addWidget(self._view2)

        # Metrics
        self.metrics1: Dict[str, QLabel] = {}
        self.metrics2: Dict[str, QLabel] = {}
        form1 = QFormLayout()
        form2 = QFormLayout()
        for key in ["mtf50", "snr", "motion_blur", "lapvar", "flicker"]:
            lbl1 = QLabel("--")
            lbl2 = QLabel("--")
            form1.addRow(key, lbl1)
            form2.addRow(key, lbl2)
            self.metrics1[key] = lbl1
            self.metrics2[key] = lbl2

        metrics_layout = QGridLayout()
        metrics_layout.addLayout(form1, 0, 0)
        metrics_layout.addLayout(form2, 0, 1)

        self._snap_btn = QPushButton("Snapshot Both")
        self._report_btn = QPushButton("Export Report")
        self._save_btn = QPushButton("Save Metrics.csv")
        bottom = QHBoxLayout()
        bottom.addWidget(self._snap_btn)
        bottom.addWidget(self._report_btn)
        bottom.addWidget(self._save_btn)

        container = QWidget()
        main = QVBoxLayout(container)
        main.addLayout(top)
        main.addLayout(views)
        main.addLayout(metrics_layout)
        main.addLayout(bottom)
        self.setCentralWidget(container)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update)

        self._buffers1: List = []
        self._buffers2: List = []

        self._start1.clicked.connect(self._start_cam1)
        self._stop1.clicked.connect(self._stop_cam1)
        self._start2.clicked.connect(self._start_cam2)
        self._stop2.clicked.connect(self._stop_cam2)
        self._snap_btn.clicked.connect(self._snapshot)
        self._report_btn.clicked.connect(self._export_report)
        self._save_btn.clicked.connect(self._save_metrics)

    # Utils
    def _ndarray_to_pixmap(self, frame):
        h, w = frame.shape[:2]
        if len(frame.shape) == 2:
            img = QImage(frame.data, w, h, frame.strides[0], QImage.Format_Grayscale8)
        else:
            img = QImage(frame.data, w, h, frame.strides[0], QImage.Format_BGR888)
        return QPixmap.fromImage(img)

    def _start_cam1(self) -> None:
        if self.cam1 is None:
            self.cam1 = CameraDevice(self._combo1.currentText())
        self.cam1.start_stream()
        if not self._timer.isActive():
            self._timer.start(30)

    def _start_cam2(self) -> None:
        if self.cam2 is None:
            self.cam2 = CameraDevice(self._combo2.currentText())
        self.cam2.start_stream()
        if not self._timer.isActive():
            self._timer.start(30)

    def _stop_cam1(self) -> None:
        if self.cam1:
            self.cam1.stop_stream()
        if self.cam2 is None or (self.cam2 and self.cam2.cap is None):
            self._timer.stop()

    def _stop_cam2(self) -> None:
        if self.cam2:
            self.cam2.stop_stream()
        if self.cam1 is None or (self.cam1 and self.cam1.cap is None):
            self._timer.stop()

    def _update(self) -> None:
        if self.cam1 and self.cam1.cap and self.cam1.cap.isOpened():
            frame1 = self.cam1.read_frame()
            self._view1.setPixmap(self._ndarray_to_pixmap(frame1))
            self._buffers1.append(frame1)
            if len(self._buffers1) > 10:
                self._buffers1.pop(0)
            self._update_metrics(frame1, self.metrics1, self._buffers1)
        if self.cam2 and self.cam2.cap and self.cam2.cap.isOpened():
            frame2 = self.cam2.read_frame()
            self._view2.setPixmap(self._ndarray_to_pixmap(frame2))
            self._buffers2.append(frame2)
            if len(self._buffers2) > 10:
                self._buffers2.pop(0)
            self._update_metrics(frame2, self.metrics2, self._buffers2)

    def _update_metrics(self, frame, labels: Dict[str, QLabel], buffer: List) -> None:
        mtf50 = m.calc_mtf50(frame)
        snr = m.calc_snr(frame)
        lapvar = m.calc_lapvar(frame)
        blur = m.calc_motion_blur_width(frame)
        flicker = m.detect_flicker(buffer)
        metrics = {
            "mtf50": mtf50,
            "snr": snr,
            "motion_blur": blur,
            "lapvar": lapvar,
            "flicker": flicker,
        }
        for key, val in metrics.items():
            thresh = THRESHOLDS.get(key)
            if thresh is None:
                status = "PASS"
            else:
                if key == "motion_blur":
                    status = "PASS" if val <= thresh else "FAIL"
                else:
                    status = "PASS" if val >= thresh else "FAIL"
            labels[key].setText(f"{val:.2f} ({status})")

    def _snapshot(self) -> None:
        if self.cam1 and self.cam1.cap and self.cam1.cap.isOpened():
            frame1 = self.cam1.read_frame()
            cv2.imwrite("snapshot_cam1.jpg", frame1)
        if self.cam2 and self.cam2.cap and self.cam2.cap.isOpened():
            frame2 = self.cam2.read_frame()
            cv2.imwrite("snapshot_cam2.jpg", frame2)

    def _export_report(self) -> None:
        data = {
            "cam1": {k: lbl.text() for k, lbl in self.metrics1.items()},
            "cam2": {k: lbl.text() for k, lbl in self.metrics2.items()},
        }
        html = render_html(data)
        export_pdf(html, "compare_report.pdf")

    def _save_metrics(self) -> None:
        import csv

        with open("metrics.csv", "w", newline="", encoding="utf-8") as fp:
            writer = csv.writer(fp)
            writer.writerow(["metric", "cam1", "cam2"])
            for key in ["mtf50", "snr", "motion_blur", "lapvar", "flicker"]:
                writer.writerow([
                    key,
                    self.metrics1[key].text(),
                    self.metrics2[key].text(),
                ])

    def closeEvent(self, event) -> None:  # type: ignore[override]
        if self.cam1:
            self.cam1.stop_stream()
        if self.cam2:
            self.cam2.stop_stream()
        super().closeEvent(event)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    win = CompareWindow()
    win.resize(1000, 600)
    win.show()
    sys.exit(app.exec())

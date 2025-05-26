import sys
import unittest
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import cv2

from cam_tuner_gui.capture.device import CameraDevice
from cam_tuner_gui.control.params import set_param

class CameraDeviceTests(unittest.TestCase):
    def test_start_stream_opens_capture(self):
        device = CameraDevice("0")
        device.start_stream()
        # Ensure that an actual VideoCapture object is created and opened
        self.assertIsInstance(device.cap, cv2.VideoCapture)
        self.assertTrue(device.cap.isOpened())
        device.stop_stream()

    def test_read_frame_without_start_raises(self):
        device = CameraDevice("0")
        with self.assertRaises(RuntimeError):
            device.read_frame()

    def test_read_frame_returns_frame(self):
        device = CameraDevice("0")
        device.start_stream()
        frame = device.read_frame()
        # Frame should not be None when capture succeeds
        self.assertIsNotNone(frame)
        device.stop_stream()

    def test_stop_stream_releases_capture(self):
        device = CameraDevice("0")
        device.start_stream()
        device.stop_stream()
        self.assertIsNone(device.cap)

class SetParamTests(unittest.TestCase):
    def test_set_param_sets_value(self):
        cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        if not cap.isOpened():
            self.skipTest("Camera device 0 not available")
        set_param(cap, "auto_exposure", 1)
        set_param(cap, "gain", 100)
        set_param(cap, "gamma", 100)
        set_param(cap, "contrast", 10)
        cap.release()

    def test_set_param_unknown_key(self):
        cap = cv2.VideoCapture(0)
        with self.assertRaises(KeyError):
            set_param(cap, "unknown", 1)
        cap.release()

if __name__ == "__main__":
    unittest.main()

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import cv2

from cam_tuner_gui.capture.device import CameraDevice
from cam_tuner_gui.control.params import set_param, get_param


def test_start_stream_opens_capture():
    device = CameraDevice("0")
    device.start_stream()
    assert isinstance(device.cap, cv2.VideoCapture)
    assert device.cap.isOpened()
    device.stop_stream()


def test_read_frame_without_start_raises():
    device = CameraDevice("0")
    with pytest.raises(RuntimeError):
        device.read_frame()


def test_read_frame_returns_frame():
    device = CameraDevice("0")
    device.start_stream()
    frame = device.read_frame()
    assert frame is not None
    device.stop_stream()


def test_stop_stream_releases_capture():
    device = CameraDevice("0")
    device.start_stream()
    device.stop_stream()
    assert device.cap is None


def test_set_param_sets_value():
    cap = cv2.VideoCapture(0)
    cap.open(0)
    if not cap.isOpened():
        pytest.skip("Camera device 0 not available")
    set_param(cap, "gain", 5)
    set_param(cap, "gamma", 100)
    set_param(cap, "contrast", 10)
    cap.release()


def test_get_param_reads_value():
    cap = cv2.VideoCapture(0)
    cap.open(0)
    if not cap.isOpened():
        pytest.skip("Camera device 0 not available")
    set_param(cap, "gain", 5)
    val = get_param(cap, "gain")
    assert isinstance(val, float)
    cap.release()


def test_set_param_unknown_key():
    cap = cv2.VideoCapture(0)
    with pytest.raises(KeyError):
        set_param(cap, "unknown", 1)
    cap.release()


import sys
import types
import pytest

# Create a minimal cv2 stub so modules can be imported without OpenCV.
class DummyVideoCapture:
    def __init__(self, source, backend=None):
        self.source = source
        self.backend = backend
        self.open_called_with = None
        self.release_called = False
        self.read_called = False
        self.set_calls = []
        self._opened = False
    def isOpened(self):
        return self._opened
    def open(self, source, backend=None):
        self.open_called_with = (source, backend)
        self._opened = True
    def release(self):
        self.release_called = True
        self._opened = False
    def read(self):
        self.read_called = True
        if not self._opened:
            return False, None
        return True, "frame"
    def set(self, prop, value):
        self.set_calls.append((prop, value))
        return True

cv2_stub = types.SimpleNamespace(
    VideoCapture=DummyVideoCapture,
    CAP_GSTREAMER=1,
    CAP_PROP_EXPOSURE=0,
    CAP_PROP_GAIN=1,
)

sys.modules['cv2'] = cv2_stub

from cam_tuner_gui.capture.device import CameraDevice
from cam_tuner_gui.control.params import set_param


def test_start_stream_opens_capture():
    device = CameraDevice("0")
    device.start_stream()
    assert isinstance(device.cap, DummyVideoCapture)
    # Since DummyVideoCapture starts closed, open() should be called with the device id
    assert device.cap.open_called_with == ("0", None)
    assert device.cap.isOpened()


def test_read_frame_without_start_raises():
    device = CameraDevice("0")
    with pytest.raises(RuntimeError):
        device.read_frame()


def test_read_frame_returns_frame():
    device = CameraDevice("0")
    device.start_stream()
    frame = device.read_frame()
    assert frame == "frame"
    assert device.cap.read_called


def test_stop_stream_releases_capture():
    device = CameraDevice("0")
    device.start_stream()
    device.stop_stream()
    # stop_stream should release and clear the capture
    assert device.cap is None


def test_set_param_sets_value():
    cap = DummyVideoCapture(0)
    set_param(cap, "gain", 5)
    assert cap.set_calls == [(cv2_stub.CAP_PROP_GAIN, 5)]


def test_set_param_unknown_key():
    cap = DummyVideoCapture(0)
    with pytest.raises(KeyError):
        set_param(cap, "unknown", 1)

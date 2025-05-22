"""영상 품질 지표 계산 모듈."""

from __future__ import annotations

from typing import Sequence
import math

try:
    import numpy as np  # type: ignore
except Exception:  # pragma: no cover - optional
    np = None  # type: ignore

try:
    import cv2  # type: ignore
except Exception:  # pragma: no cover - optional
    cv2 = None  # type: ignore


def calc_mtf50(image) -> float:
    """이미지로부터 MTF50을 계산한다."""
    if np is None or cv2 is None:
        raise ImportError("NumPy와 OpenCV가 필요합니다")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobel = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    mag = np.abs(sobel)
    profile = np.mean(mag, axis=0)
    fft = np.abs(np.fft.rfft(profile))
    freqs = np.fft.rfftfreq(profile.size)
    half_max = fft.max() / 2.0
    idx = np.where(fft >= half_max)[0][-1]
    mtf50 = freqs[idx] * image.shape[1]
    return float(mtf50)


def calc_snr(image) -> float:
    """이미지의 신호 대 잡음비(SNR)를 계산한다."""
    if np is None:
        raise ImportError("NumPy가 필요합니다")

    gray = image.mean(axis=2) if image.ndim == 3 else image
    mean_val = float(np.mean(gray))
    std_val = float(np.std(gray))
    if std_val == 0:
        return math.inf
    return 20 * math.log10(mean_val / std_val)


def detect_flicker(frames) -> float:
    """프레임 시퀀스에서 플리커율을 계산한다."""
    if np is None:
        raise ImportError("NumPy가 필요합니다")

    if not isinstance(frames, Sequence) or len(frames) < 2:
        return 0.0

    diffs = []
    for a, b in zip(frames[:-1], frames[1:]):
        a_gray = a.mean(axis=2) if a.ndim == 3 else a
        b_gray = b.mean(axis=2) if b.ndim == 3 else b
        diff = np.abs(a_gray.astype(np.float32) - b_gray.astype(np.float32)).mean()
        diffs.append(diff)

    avg = float(np.mean(diffs))
    base = frames[0].mean() if frames[0].ndim == 3 else frames[0].mean()
    if base == 0:
        return 0.0
    return (avg / float(base)) * 100.0

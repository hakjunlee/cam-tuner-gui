"""영상 품질 지표 계산 모듈."""

from __future__ import annotations

import math
from typing import Sequence

import cv2
import numpy as np


def calc_mtf50(image) -> float:
    """이미지로부터 MTF50을 계산한다."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image
    f = np.fft.fftshift(np.fft.fft2(gray))
    magnitude = np.abs(f)
    center_line = magnitude[magnitude.shape[0] // 2]
    center_line = center_line[: center_line.size // 2]
    mtf = center_line / (center_line[0] + 1e-6)
    idx = np.argmin(np.abs(mtf - 0.5))
    return float(idx) / float(center_line.size)


def calc_snr(image) -> float:
    """이미지의 신호 대 잡음비(SNR)를 계산한다."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image
    mean = float(np.mean(gray))
    std = float(np.std(gray))
    if std == 0:
        return 0.0
    return 20 * math.log10(mean / std)


def detect_flicker(frames: Sequence[np.ndarray]) -> float:
    """프레임 시퀀스에서 플리커율을 계산한다."""
    if len(frames) < 2:
        return 0.0
    means = [np.mean(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) if f.ndim == 3 else f) for f in frames]
    diffs = [abs(means[i] - means[i + 1]) for i in range(len(means) - 1)]
    baseline = np.mean(means)
    if baseline == 0:
        return 0.0
    return float(max(diffs) / baseline * 100)

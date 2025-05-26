"""영상 품질 지표 계산 모듈."""

from __future__ import annotations

import numpy as np
import cv2

def calc_mtf50(image) -> float:
    """이미지로부터 MTF50을 계산한다.

    Notes
    -----
    이 함수는 간단한 FFT 기반 방식으로 이미지를 분석하여
    50% Modulation Transfer Frequency를 추정한다. 정확도는
    전문 라이브러리 대비 낮을 수 있지만 의존성을 최소화하기
    위한 구현이다.
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    row = gray[gray.shape[0] // 2].astype(np.float32)
    row -= row.mean()
    spec = np.abs(np.fft.rfft(row))
    if spec.size == 0:
        return 0.0
    max_val = spec.max()
    if max_val == 0:
        return 0.0
    spec /= max_val
    idx = np.searchsorted(spec, 0.5)
    if idx >= spec.size:
        idx = spec.size - 1
    return float(idx / len(row))

def calc_snr(image) -> float:
    """이미지의 신호 대 잡음비(SNR)를 계산한다."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    data = gray.astype(np.float32)
    mean = float(data.mean())
    std = float(data.std())
    if std == 0:
        return float("inf")
    snr = 20 * np.log10(mean / (std + 1e-8))
    return float(snr)

def detect_flicker(frames) -> float:
    """프레임 시퀀스에서 플리커율을 계산한다."""
    if not frames:
        return 0.0

    means = []
    for img in frames:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        means.append(float(gray.mean()))

    diffs = np.abs(np.diff(means))
    flicker = diffs.mean() / (np.mean(means) + 1e-8) * 100
    return float(flicker)


def calc_lapvar(image) -> float:
    """라플라시안 분산을 이용한 샤프니스 지표."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    return float(lap.var())


def calc_motion_blur_width(image) -> float:
    """간단한 에지 전이 폭 기반 모션 블러 추정."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    row = gray[gray.shape[0] // 2].astype(np.float32)
    row_blur = cv2.GaussianBlur(row.reshape(1, -1), (9, 1), 0).ravel()
    grad = np.abs(np.gradient(row_blur))
    if grad.max() == 0:
        return 0.0
    peak = np.argmax(grad)
    thresh = grad.max() * 0.1
    left = peak
    while left > 0 and grad[left] > thresh:
        left -= 1
    right = peak
    while right < len(grad) - 1 and grad[right] > thresh:
        right += 1
    width = right - left
    return float(width)

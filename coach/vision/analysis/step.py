from __future__ import annotations

import math
from collections import deque

import numpy as np

from coach.vision.analysis.quality import QualityReport
from coach.vision.constants import Issues
from coach.vision.constants import PoseLandmark
from coach.vision.pose import SmoothedPoseResult


class StepDetector:
    # CHACHA_IDEAL_BPM = 120.0
    TEMPO_TOLERANCE = 0.15
    MIN_INTERVAL_S = 0.15

    MOVE_VELOCITY_THRESHOLD = 0.20
    PLANT_VELOCITY_THRESHOLD = 0.05

    def __init__(self):
        self._step_times: deque = deque(maxlen=10)
        self._last_step_t: float = 0.0
        self._current_tempo_issue: Issues | None = None
        self._prev_l_ankle: tuple[float, float] | None = None
        self._prev_r_ankle: tuple[float, float] | None = None
        self._prev_time: float = 0.0
        self._l_moving: bool = False
        self._r_moving: bool = False

    def analyze(
        self,
        landmarks: list[SmoothedPoseResult],
        timestamp_ms: float,
        tempo: float,
    ) -> QualityReport:
        report = QualityReport()
        if not landmarks:
            return report

        l_ankle = landmarks[PoseLandmark.LEFT_ANKLE]
        r_ankle = landmarks[PoseLandmark.RIGHT_ANKLE]
        timestamp_s = timestamp_ms / 1000.0

        if self._prev_l_ankle is not None and self._prev_time > 0:
            dt = timestamp_s - self._prev_time
            if dt > 0:
                l_dx = l_ankle.x - self._prev_l_ankle[0]
                l_dy = l_ankle.y - self._prev_l_ankle[1]
                l_vel = math.hypot(l_dx, l_dy) / dt

                r_dx = r_ankle.x - self._prev_r_ankle[0]
                r_dy = r_ankle.y - self._prev_r_ankle[1]
                r_vel = math.hypot(r_dx, r_dy) / dt

                if l_vel > self.MOVE_VELOCITY_THRESHOLD:
                    self._l_moving = True
                elif self._l_moving and l_vel < self.PLANT_VELOCITY_THRESHOLD:
                    self._l_moving = False
                    self._register_step(timestamp_s, tempo)

                if r_vel > self.MOVE_VELOCITY_THRESHOLD:
                    self._r_moving = True
                elif self._r_moving and r_vel < self.PLANT_VELOCITY_THRESHOLD:
                    self._r_moving = False
                    self._register_step(timestamp_s, tempo)

        self._prev_l_ankle = (l_ankle.x, l_ankle.y)
        self._prev_r_ankle = (r_ankle.x, r_ankle.y)
        self._prev_time = timestamp_s

        if self._current_tempo_issue:
            report.issues.append(self._current_tempo_issue)

        return report

    def _register_step(self, timestamp_s: float, tempo: float):
        """Wewnętrzna metoda obsługująca zaliczenie kroku."""
        if (timestamp_s - self._last_step_t) > self.MIN_INTERVAL_S:
            self._step_times.append(timestamp_s)
            self._last_step_t = timestamp_s
            self._update_tempo_issue(tempo)

    def _update_tempo_issue(self, tempo: float):
        """Aktualizuje flagę błędu na podstawie ostatnich kroków."""
        if len(self._step_times) < 4:
            self._current_tempo_issue = None
            return

        intervals = np.diff(list(self._step_times))
        median_interval = float(np.median(intervals))

        if median_interval <= 0:
            return

        bpm = 60.0 / median_interval
        diff = (bpm - tempo) / tempo

        if abs(diff) <= self.TEMPO_TOLERANCE:
            self._current_tempo_issue = None
        elif diff < 0:
            self._current_tempo_issue = Issues.TEMPO_ZA_WOLNE
        else:
            self._current_tempo_issue = Issues.TEMPO_ZA_SZYBKIE

from __future__ import annotations

from collections import deque

from coach.vision.constants import Issues


class ErrorDetector:
    def __init__(
        self,
        window_size: int = 15,
        threshold: int = 10,
        cooldown_frames: int = 90,
    ) -> None:
        self.window_size = window_size
        self.threshold = threshold
        self.cooldown_frames = cooldown_frames
        self._windows: dict[Issues, deque] = {}
        self._cooldowns: dict[Issues, int] = {}
        self._frame = 0

    def update(self, issues: list[Issues]) -> None:
        self._frame += 1
        all_issues = set(issues) | set(self._windows.keys())

        for issue in all_issues:
            if issue not in self._windows:
                self._windows[issue] = deque(maxlen=self.window_size)
            self._windows[issue].append(issue in issues)

    def is_active(self, issue: Issues) -> bool:
        window = self._windows.get(issue)
        return bool(window) and sum(window) >= self.threshold

    def get_active_errors(self) -> list[Issues]:
        return [issue for issue in self._windows if self.is_active(issue)]

    def show_alerts(self) -> list[Issues]:
        alerts = []
        for issue in self.get_active_errors():
            last = self._cooldowns.get(issue, -self.cooldown_frames)
            if self._frame - last >= self.cooldown_frames:
                self._cooldowns[issue] = self._frame
                alerts.append(issue)

        return alerts

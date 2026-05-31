from collections import deque

from coach.vision.constants import Issues


class ErrorDetector:
    def __init__(self, window_size: int, threshold: int):
        self.window_size = window_size
        self.threshold = threshold
        self._windows: dict[Issues, deque] = {}
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

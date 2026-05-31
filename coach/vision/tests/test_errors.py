import unittest

from coach.vision.constants import Issues
from coach.vision.errors import ErrorDetector


class TestErrorDetector(unittest.TestCase):
    def test_error_while_above_threshold(self):
        detect = ErrorDetector(window_size=15, threshold=3)

        for _ in range(3):
            detect.update([Issues.RECE_ZA_NISKO])
            detect.tick()

        assert detect.is_active(Issues.RECE_ZA_NISKO)

    def test_error_while_below_threshold(self):
        detect = ErrorDetector(window_size=15, threshold=3)

        for _ in range(2):
            detect.update([Issues.RECE_ZA_NISKO])
            detect.tick()

        assert not detect.is_active(Issues.RECE_ZA_NISKO)

    def test_error_while_never_added(self):
        detect = ErrorDetector(window_size=15, threshold=3)
        assert not detect.is_active(Issues.RECE_ZA_NISKO)

    def test_old_frames_leave_window(self):
        detect = ErrorDetector(window_size=5, threshold=3)

        for _ in range(3):
            detect.update([Issues.RECE_ZA_NISKO])
            detect.tick()

        for _ in range(3):
            detect.update([])
            detect.tick()

        assert not detect.is_active(Issues.RECE_ZA_NISKO)

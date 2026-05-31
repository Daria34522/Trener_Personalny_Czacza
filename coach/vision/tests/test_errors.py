import unittest

from coach.vision.constants import Issues
from coach.vision.errors import ErrorDetector


class TestErrorDetector(unittest.TestCase):
    def test_error_while_above_threshold(self):
        detect = ErrorDetector(window_size=15, threshold=3)

        for _ in range(3):
            detect.update([Issues.RECE_ZA_NISKO])

        assert detect.is_active(Issues.RECE_ZA_NISKO)

    def test_error_while_below_threshold(self):
        detect = ErrorDetector(window_size=15, threshold=3)

        for _ in range(2):
            detect.update([Issues.RECE_ZA_NISKO])

        assert not detect.is_active(Issues.RECE_ZA_NISKO)

    def test_error_while_never_added(self):
        detect = ErrorDetector(window_size=15, threshold=3)
        assert not detect.is_active(Issues.RECE_ZA_NISKO)

    def test_old_frames_leave_window(self):
        detect = ErrorDetector(window_size=5, threshold=3)

        for _ in range(3):
            detect.update([Issues.RECE_ZA_NISKO])

        for _ in range(3):
            detect.update([])

        assert not detect.is_active(Issues.RECE_ZA_NISKO)

    def test_two_errors_independent(self):
        detect = ErrorDetector(window_size=15, threshold=3)

        for _ in range(3):
            detect.update([Issues.RECE_ZA_NISKO])

        assert detect.is_active(Issues.RECE_ZA_NISKO)
        assert not detect.is_active(Issues.KOLANO_UGIETE)

    def test_error_from_two_updates(self):
        detect = ErrorDetector(window_size=15, threshold=3)

        for _ in range(3):
            detect.update([Issues.KOLANO_UGIETE])
            detect.update([Issues.RECE_ZA_NISKO])

        assert detect.is_active(Issues.KOLANO_UGIETE)
        assert detect.is_active(Issues.RECE_ZA_NISKO)

    def test_get_active_errors_active(self):
        detect = ErrorDetector(window_size=15, threshold=3)

        for _ in range(3):
            detect.update([Issues.KOLANO_UGIETE, Issues.RECE_ZA_NISKO])

        active = detect.get_active_errors()
        assert Issues.KOLANO_UGIETE in active
        assert Issues.RECE_ZA_NISKO in active

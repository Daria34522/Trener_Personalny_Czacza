import unittest

from coach.vision.constants import Issues
from coach.vision.errors import ErrorDetector


class TestErrorDetector(unittest.TestCase):
    def test_error_while_above_threshold(self):
        detect = ErrorDetector(window_size=15, threshold=3)

        for _ in range(3):
            detect.update([Issues.RECE_ZA_NISKO])

        print(detect.is_active(Issues.RECE_ZA_NISKO))

        assert detect.is_active(Issues.RECE_ZA_NISKO)

    def test_error_while_below_threshold(self):
        detect = ErrorDetector(window_size=15, threshold=3)

        for _ in range(2):
            detect.update([Issues.RECE_ZA_NISKO])

        assert not detect.is_active(Issues.RECE_ZA_NISKO)

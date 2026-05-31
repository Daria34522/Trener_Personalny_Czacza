from __future__ import annotations

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
        assert any(active)
        assert Issues.KOLANO_UGIETE in active
        assert Issues.RECE_ZA_NISKO in active

    def test_get_active_errors_inactive(self):
        detect = ErrorDetector(window_size=15, threshold=3)

        for _ in range(2):
            detect.update([Issues.KOLANO_UGIETE, Issues.RECE_ZA_NISKO])

        active = detect.get_active_errors()
        assert not any(active)
        assert Issues.KOLANO_UGIETE not in active
        assert Issues.RECE_ZA_NISKO not in active

    def test_get_active_errors_empty(self):
        detect = ErrorDetector(window_size=15, threshold=3)
        assert not any(detect.get_active_errors())

    def test_show_alerts_returns_active_errors(self):
        detect = ErrorDetector(window_size=15, threshold=3, cooldown_frames=10)

        for _ in range(3):
            detect.update([Issues.KOLANO_UGIETE])

        alerts = detect.show_alerts()
        assert any(alerts)
        assert Issues.KOLANO_UGIETE in alerts

    def test_show_alerts_respects_cooldown(self):
        detect = ErrorDetector(window_size=15, threshold=3, cooldown_frames=10)

        for _ in range(3):
            detect.update([Issues.KOLANO_UGIETE])

        alerts = detect.show_alerts()
        assert any(alerts)
        assert Issues.KOLANO_UGIETE in alerts

        detect.update([Issues.KOLANO_UGIETE])
        assert not detect.show_alerts()

    def test_show_alerts_after_cooldown(self):
        detect = ErrorDetector(window_size=15, threshold=3, cooldown_frames=5)

        for _ in range(3):
            detect.update([Issues.KOLANO_UGIETE])

        alerts = detect.show_alerts()
        assert any(alerts)
        assert Issues.KOLANO_UGIETE in alerts

        for _ in range(5):
            detect.update([Issues.KOLANO_UGIETE])

        alerts = detect.show_alerts()
        assert any(alerts)
        assert Issues.KOLANO_UGIETE in alerts

    def test_show_alerts_empty_below_threshold(self):
        detect = ErrorDetector(window_size=15, threshold=3, cooldown_frames=10)

        for _ in range(2):
            detect.update([Issues.KOLANO_UGIETE])

        assert not any(detect.show_alerts())

    def test_two_errors_independent_cooldown(self):
        detect = ErrorDetector(window_size=5, threshold=3, cooldown_frames=10)

        for _ in range(3):
            detect.update([Issues.KOLANO_UGIETE, Issues.RECE_ZA_NISKO])

        alerts = detect.show_alerts()
        assert any(alerts)
        assert Issues.KOLANO_UGIETE in alerts
        assert Issues.RECE_ZA_NISKO in alerts

        for _ in range(10):
            detect.update([Issues.KOLANO_UGIETE])

        alerts = detect.show_alerts()
        assert any(alerts)
        assert Issues.KOLANO_UGIETE in alerts
        assert Issues.RECE_ZA_NISKO not in alerts

    def test_real_two_cameras_scenario(self):
        detect = ErrorDetector(window_size=60, threshold=10, cooldown_frames=240)

        # kamera z przodu
        for _ in range(15):
            detect.update([Issues.ZA_DLUGI_KROK])
            detect.update([])

        # kamera z boku
        for _ in range(30):
            detect.update([])

        alerts = detect.show_alerts()
        assert any(alerts)
        assert Issues.ZA_DLUGI_KROK in alerts

        # kamera z przodu
        for _ in range(30):
            detect.update([])

        # kamera z boku
        for _ in range(15):
            detect.update([Issues.ZA_GLEBOKI_KROK])
            detect.update([])

        alerts = detect.show_alerts()
        assert any(alerts)
        assert Issues.ZA_DLUGI_KROK not in alerts
        assert Issues.ZA_GLEBOKI_KROK in alerts

        for _ in range(3):
            detect.update([Issues.BIODRA_NIEROWNE])
            detect.update([])

        assert not any(detect.show_alerts())

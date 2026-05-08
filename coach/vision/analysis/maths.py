from __future__ import annotations

import numpy as np
from coach.vision.pose import SmoothedPoseResult


def angle(a: SmoothedPoseResult, b: SmoothedPoseResult, c: SmoothedPoseResult) -> float:
    """Liczy kąt w stopniach pomiędzy 3 punktami

    - a (Punkt): koniec trójkąta
    - b (Punkt): wierzchołek trójkąta
    - c (Punkt): koniec trójkąta

    Zwraca:
    - Wartość typu float kąta w stopniach
    """
    ab = [a.x - b.x, a.y - b.y]
    cb = [c.x - b.x, c.y - b.y]

    dot = np.dot(ab, cb)
    mag_ab = np.hypot(ab[0], ab[1])
    mag_cb = np.hypot(cb[0], cb[1])

    if mag_ab * mag_cb == 0:
        return 0

    cos_angle = dot / (mag_ab * mag_cb)
    cos_angle = np.clip(cos_angle, -1, 1)
    return np.degrees(np.acos(cos_angle))

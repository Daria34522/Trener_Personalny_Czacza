from __future__ import annotations

import numpy as np

from dataclasses import dataclass
from dataclasses import field

from coach.vision.constants import PoseLandmark
from coach.vision.constants import Issues
from coach.vision.pose import SmoothedPoseResult

from coach.vision.analysis import maths


@dataclass
class QualityReport:
    issues: list[Issues] = field(default_factory=list)


def analyze_front(landmarks: list[SmoothedPoseResult]) -> QualityReport:
    """
    Analiza z kamery frontowej:
    - przeniesienie ciężaru (shift bioder)
    - poziom bioder
    - pozycja rąk
    """
    report = QualityReport()

    if not landmarks:
        return report

    l_hip = landmarks[PoseLandmark.LEFT_HIP]
    r_hip = landmarks[PoseLandmark.RIGHT_HIP]

    l_wrist = landmarks[PoseLandmark.LEFT_WRIST]
    r_wrist = landmarks[PoseLandmark.RIGHT_WRIST]

    l_shoulder = landmarks[PoseLandmark.LEFT_SHOULDER]
    r_shoulder = landmarks[PoseLandmark.RIGHT_SHOULDER]

    r_ankle = landmarks[PoseLandmark.RIGHT_ANKLE]
    l_ankle = landmarks[PoseLandmark.LEFT_ANKLE]

    hip_center_x = (l_hip.x + r_hip.x) / 2.0
    weight_shift = np.abs(hip_center_x - 0.5)

    ankle_spread_x = np.abs(l_ankle.x - r_ankle.x)

    hip_level = np.abs(l_hip.y - r_hip.y)
    if hip_level > 0.06:
        report.issues.append(Issues.BIODRA_NIEROWNE)

    if ankle_spread_x > 0.07 and weight_shift < 0.025:
        report.issues.append(Issues.SLABE_PRZENIESIENIE_CIEZARU)

    # W cha-cha ręce powinny być mniej więcej na poziomie łokcia,
    # nie opuszczone poniżej bioder
    avg_wrist_y = np.mean([l_wrist.y, r_wrist.y])
    avg_hip_y = np.mean([l_hip.y, r_hip.y])
    avg_shldr_y = np.mean([l_shoulder.y, r_shoulder.y])

    if avg_wrist_y > avg_hip_y + 0.05:
        report.issues.append(Issues.RECE_ZA_NISKO)
    elif avg_wrist_y < avg_shldr_y - 0.05:
        report.issues.append(Issues.RECE_ZA_WYSOKO)

    ankle_spread_x = np.abs(l_ankle.x - r_ankle.x)
    if ankle_spread_x > 0.15:
        report.issues.append(Issues.ZA_DLUGI_KROK)

    return report


def analyze_side(landmarks: list[SmoothedPoseResult]) -> QualityReport:
    """
    Analiza z kamery bocznej:
    - czy kolano nie wybiega przed stopę
    - głębokość kroku (przód/tył)
    """
    report = QualityReport()

    if not landmarks:
        return report

    # Kamera boczna: oś X odpowiada głębokości (przód/tył)
    l_knee = landmarks[PoseLandmark.LEFT_KNEE]
    l_ankle = landmarks[PoseLandmark.LEFT_ANKLE]
    l_hip = landmarks[PoseLandmark.LEFT_HIP]

    r_knee = landmarks[PoseLandmark.RIGHT_KNEE]
    r_ankle = landmarks[PoseLandmark.RIGHT_ANKLE]
    r_hip = landmarks[PoseLandmark.RIGHT_HIP]

    l_angle = maths.angle(l_hip, l_knee, l_ankle)
    r_angle = maths.angle(r_hip, r_knee, r_ankle)
    if l_angle < 140 or r_angle < 140:
        report.issues.append(Issues.KOLANO_UGIETE)

    # sprawdzenie czy krok w przód/tył jest dobry, a nie za duży
    ankle_spread_x = np.abs(l_ankle.x - r_ankle.x)
    if ankle_spread_x > 0.15:
        report.issues.append(Issues.ZA_GLEBOKI_KROK)

    return report

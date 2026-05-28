from __future__ import annotations

import os
from enum import IntEnum
from enum import StrEnum

MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "assets", "pose_landmarker_full.task"
)


class PoseLandmark(IntEnum):
    NOSE = 0
    LEFT_EYE_INNER = 1
    LEFT_EYE = 2
    LEFT_EYE_OUTER = 3
    RIGHT_EYE_INNER = 4
    RIGHT_EYE = 5
    RIGHT_EYE_OUTER = 6
    LEFT_EAR = 7
    RIGHT_EAR = 8
    MOUTH_LEFT = 9
    MOUTH_RIGHT = 10

    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12

    LEFT_ELBOW = 13
    RIGHT_ELBOW = 14
    LEFT_WRIST = 15
    RIGHT_WRIST = 16

    LEFT_HIP = 23
    RIGHT_HIP = 24

    LEFT_KNEE = 25
    RIGHT_KNEE = 26
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28

    LEFT_HEEL = 29
    RIGHT_HEEL = 30
    LEFT_FOOT = 31
    RIGHT_FOOT = 32


class Issues(StrEnum):
    SLABE_PRZENIESIENIE_CIEZARU = "SLABE_PRZENIESIENIE_CIEZARU"
    BIODRA_NIEROWNE = "BIODRA_NIEROWNE"
    RECE_ZA_NISKO = "RECE_ZA_NISKO"
    RECE_ZA_WYSOKO = "RECE_ZA_WYSOKO"
    KOLANO_UGIETE = "KOLANO_UGIETE"
    MALO_WIDOCZNY_W_KAMERACH = "MALO_WIDOCZNY_W_KAMERACH"
    ZA_GLEBOKI_KROK = "ZA_GLEBOKI_KROK"
    ZA_DLUGI_KROK = "ZA_DLUGI_KROK"

    @staticmethod
    def to_polish(issues: list[Issues]) -> list[str]:
        """Zamienia kody błędów na czytelne komunikaty po polsku."""
        translations = {
            "SLABE_PRZENIESIENIE_CIEZARU": "Przenieś bardziej ciężar bioder na noge z aktualnym ciężarem",
            "BIODRA_NIEROWNE": "Biodra nie są prosto – wyrównaj",
            "RECE_ZA_NISKO": "Unieś ręce – są zbyt nisko",
            "RECE_ZA_WYSOKO": "Opuść ręce – są zbyt wysoko",
            "KOLANO_UGIETE": "Kolano jest za bardzo ugięte – uważaj na kolana!",
            "MALO_WIDOCZNY_W_KAMERACH": "Jesteś mało widoczny w kamerach – popraw ustawienie",
            "ZA_GLEBOKI_KROK": "Krok w przód/tył jest zbyt głęboki, przybliż troche stopy do siebie",
            "ZA_DLUGI_KROK": "Krok w lewo/prawo jest zbyt szeroki, przybliż troche stopy od siebie",
        }
        result = []
        for issue in issues:
            result.append(translations.get(issue))
        return result

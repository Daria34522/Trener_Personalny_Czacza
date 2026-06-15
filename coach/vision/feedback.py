import random


def _choose(variants):
    return random.choice(variants)


def posture_feedback(error_count: int) -> str:
    if error_count <= 2:
        variants = [
            "Dobra postawa",
            "Plecy proste, wzrok przed siebie",
            "Klatka piersiowa wypchnięta, sylwetka stabilna",
            "Wysoka dokładność ruchów",
        ]
        return _choose(variants)

    if error_count <= 5:
        variants = [
            "Drobne zachwiania, ale ogólnie stabilnie",
            "Lekka korekta postawy wystarczy",
            "Niewielkie odchylenia, skup się na prostowaniu pleców",
        ]
        return _choose(variants)

    if error_count <= 10:
        variants = [
            "Postawa wymaga poprawy",
            "Skup się na stabilności tułowia",
            "Ćwicz prostowanie pleców i otwieranie klatki",
        ]
        return _choose(variants)

    variants = [
        "Znaczne zachwiania postawy — warto popracować nad podstawami",
        "Postawa niestabilna, potrzebne ćwiczenia stabilizujące",
        "Skoncentruj się na ustawieniu tułowia przed kolejną próbą",
    ]
    return _choose(variants)


def steps_feedback(error_count: int) -> str:
    if error_count <= 2:
        variants = [
            "Wszystkie kroki precyzyjne",
            "Wysoka dokładność ruchów",
            "Kroki równe i kontrolowane",
            "Precyzyjne sekwencje",
        ]
        return _choose(variants)

    if error_count <= 5:
        variants = [
            "Drobne niedokładności w krokach",
            "Kilka potknięć, ale ogólnie spójne sekwencje",
            "Trzeba dopracować detale kroków",
        ]
        return _choose(variants)

    if error_count <= 10:
        variants = [
            "Kroki wymagają pracy — ćwicz powoli sekwencje",
            "Brakuje precyzji w przejściach",
            "Warto odrobić podstawy kroków",
        ]
        return _choose(variants)

    variants = [
        "Częste błędy w krokach — wróć do podstaw",
        "Kroki chaotyczne, potrzebna systematyczna praca",
        "Skup się na pojedynczych elementach sekwencji",
    ]
    return _choose(variants)


def tempo_feedback(error_count: int) -> str:
    if error_count <= 2:
        variants = [
            "Idealne tempo",
            "Stabilne, równe tempo",
            "Tempo pod kontrolą",
        ]
        return _choose(variants)

    if error_count <= 5:
        variants = [
            "Trochę za szybko pod koniec",
            "Lekkie rozjeżdżanie tempa",
            "Kilka nieregularności rytmicznych",
        ]
        return _choose(variants)

    if error_count <= 10:
        variants = [
            "Tempo nieregularne — warto popracować nad rytmem",
            "Rytm chwilami się gubi",
            "Zwróć uwagę na równomierne tempo",
        ]
        return _choose(variants)

    variants = [
        "Duże odchylenia tempa — trzeba popracować nad rytmem",
        "Tempo niestabilne, powtórz ćwiczenia rytmiczne",
        "Potrzeba pracy z metronomem dla stabilnego tempa",
    ]
    return _choose(variants)


def session_summary(
    posture_errors: int,
    step_errors: int,
    tempo_errors: int,
) -> str:
    total_errors = posture_errors + step_errors + tempo_errors
    if total_errors <= 2:
        openers = [
            "Fenomenalnie!",
            "Rewelacja!",
            "Wyjątkowy postęp!",
        ]
    elif total_errors <= 6:
        openers = [
            "Świetna sesja",
            "Bardzo dobrze",
            "Dobra robota",
        ]
    elif total_errors <= 15:
        openers = [
            "Solidna praca",
            "Widać zaangażowanie",
            "Postępy są, choć jeszcze trochę pracy",
        ]
    else:
        openers = [
            "Trzeba popracować",
            "Mamy pole do poprawy",
            "Potrzeba więcej skupienia",
        ]

    return _choose(openers)

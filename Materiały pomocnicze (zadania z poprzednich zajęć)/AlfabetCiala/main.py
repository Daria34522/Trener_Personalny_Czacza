import cv2
import math
import mediapipe as mp
from collections import deque
from collections import namedtuple

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=0,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

lm_history = deque(maxlen=5)
letter_history = deque(maxlen=5)
word_buffer = deque()

NormalisedFrame = namedtuple("NormalisedFrame", ["x", "y", "z", "visibility"])

def angle(a: NormalisedFrame, b: NormalisedFrame, c: NormalisedFrame) -> float:
    """Liczy kąt w stopniach pomiędzy 3 punktami
    
    - a (Punkt): koniec trójkąta
    - b (Punkt): wierzchołek trójkąta
    - c (Punkt): koniec trójkąta
    
    Zwraca:
    - Wartość typu float kąta w stopniach
    """
    ab = [a.x - b.x, a.y - b.y]
    cb = [c.x - b.x, c.y - b.y]

    dot = ab[0]*cb[0] + ab[1]*cb[1]
    mag_ab = math.hypot(ab[0], ab[1])
    mag_cb = math.hypot(cb[0], cb[1])

    if mag_ab * mag_cb == 0:
        return 0

    cos_angle = dot / (mag_ab * mag_cb)
    cos_angle = max(-1, min(1, cos_angle))
    return math.degrees(math.acos(cos_angle))

def smooth_landmarks(new_lm) -> list[NormalisedFrame]:
    """Funkcja licząca średnią dla wszystkich kończyn z maksymalnie 5 klatek (rozwiązanie na migotanie)"""
    lm_history.append(new_lm)
    smoothed = []
    for idx, _ in enumerate(new_lm):
        x = sum(l[idx].x for l in lm_history)/len(lm_history)
        y = sum(l[idx].y for l in lm_history)/len(lm_history)
        z = sum(l[idx].z for l in lm_history)/len(lm_history)
        visibility = sum(l[idx].visibility for l in lm_history)/len(lm_history)

        smoothed.append(NormalisedFrame(x=x, y=y, z=z, visibility=visibility))

    return smoothed

def detect_letter(lm: list[NormalisedFrame]) -> str:
    ls = lm[mp_pose.PoseLandmark.LEFT_SHOULDER]
    rs = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    le = lm[mp_pose.PoseLandmark.LEFT_ELBOW]
    re = lm[mp_pose.PoseLandmark.RIGHT_ELBOW]
    lw = lm[mp_pose.PoseLandmark.LEFT_WRIST]
    rw = lm[mp_pose.PoseLandmark.RIGHT_WRIST]

    visibility_threshold = 0.85
    straight = 150
    straight_vertically_threshold = 0.2
    down_horizontally_threshold = 0.25
    up_horizontally_threshold = 0.20
    wrist_close_threshold = 0.30

    # Sprawdzamy czy wszystkie kończyny są widoczne w 85%, jeśli nie, nie wykrywamy nic.
    if (
        ls.visibility < visibility_threshold or
        rs.visibility < visibility_threshold or
        lw.visibility < visibility_threshold or
        rw.visibility < visibility_threshold or
        re.visibility < visibility_threshold or
        le.visibility < visibility_threshold
    ):
        return "?" 

    left_angle = angle(ls, le, lw)
    right_angle = angle(rs, re, rw)

    # Dla T sprawdzamy czy ręka jest na prosto z poziomem ufności od 150 stopni i 
    # sprawdzamy czy nadgarstek jest mniej więcej na wysokości barku z błędem 20%
    left_straight = left_angle > straight
    right_straight = right_angle > straight

    left_arm_straight = abs(lw.y - ls.y) < straight_vertically_threshold
    right_arm_straight = abs(rw.y - rs.y) < straight_vertically_threshold

    # Dla I sprawdzamy czy ręka jest wyprostowana i sprawdzamy czy 
    # nadgarstek jest niżej niż bark z poziomem nieufności 25%
    left_arm_down = lw.y > ls.y + down_horizontally_threshold
    right_arm_down = rw.y > rs.y + down_horizontally_threshold

    # Dla Y sprawdzamy czy nadgarski są wyżej niż barki z błędem 20% 
    # oraz sprawdzamy czy nadgarski są 30% i więcej od siebie.
    left_arm_up = lw.y < ls.y - up_horizontally_threshold
    right_arm_up = rw.y < rs.y - up_horizontally_threshold
    wrist_close_to = abs(lw.x - rw.x) > wrist_close_threshold

    # Dla L sprawdzamy czy prawa ręka (odbicie lustrzane, tak naprawde lewa) 
    # jest całkowicie w górze oraz czy lewa (czyli prawa) jest prosto w bok.
    right_arm_straight_horizontally = rw.y + up_horizontally_threshold < rs.y

    if left_straight and right_straight and left_arm_straight and right_arm_straight:
        return "T"
    
    if left_straight and right_straight and left_arm_down and right_arm_down:
        return "I"
    
    if left_straight and right_straight and left_arm_up and right_arm_up and wrist_close_to:
        return "Y"
    
    if right_arm_straight_horizontally and left_arm_straight:
        return "L"
    
    return "?"

def main() -> int:
    cam1_source = 0
    capture = cv2.VideoCapture(cam1_source)
    # Mniejsze użycie zasobów przez zmniejszenie rozmiaru przesyłanego obrazu
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    current_letter = "?"

    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame_rgb.flags.writeable = False
        results = pose.process(frame_rgb)
        frame_rgb.flags.writeable = True

        landmarks = results.pose_landmarks
        if landmarks is not None:
            lm = smooth_landmarks(landmarks.landmark)

            letter = detect_letter(lm)

            # Sprawdzanie czy 3/5 ostatnich klatek zawierało litere, jeśli tak to ją program wyświetli.
            letter_history.append(letter)
            if letter_history.count(letter) >= 3 and letter != "?":
                current_letter = letter

            # Dodawanie litery do buforu słowa.
            if current_letter != "?" and (not word_buffer or word_buffer[-1] != current_letter):
                word_buffer.append(current_letter)

            cv2.putText(frame, f"Litera: {letter}", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                    (0, 255, 0), 3)
            
            cv2.putText(frame, f"Slowo: {''.join(word_buffer)}", (20, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                    (0, 255, 255), 2)

            # Rysowanie szkieletu
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

            # Zresetuj słowo na ekranie spacją
            if cv2.waitKey(1) & 0xFF == 32:
                current_letter = "?"
                word_buffer.clear()
                letter_history.clear()
                lm_history.clear()

            
        cv2.imshow("Alfabet ciala", frame)
        
        # Wyłącz program przyciskiem ESC.
        if cv2.waitKey(1) & 0xFF == 27:
            break


    capture.release()
    cv2.destroyAllWindows()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
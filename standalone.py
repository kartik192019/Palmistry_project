import cv2
import mediapipe as mp
import os

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def euclidean_distance(p1, p2):
    return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2) ** 0.5

def get_finger_length(landmarks, tip_idx, base_idx):
    return euclidean_distance(landmarks[tip_idx], landmarks[base_idx])

def get_avg_finger_length(landmarks):
    fingers = [
        get_finger_length(landmarks, 8, 5),
        get_finger_length(landmarks, 12, 9),
        get_finger_length(landmarks, 16, 13),
        get_finger_length(landmarks, 20, 17)
    ]
    return sum(fingers) / len(fingers)

def get_palm_length(landmarks):
    return euclidean_distance(landmarks[0], landmarks[9])

def get_palm_width(landmarks):
    return euclidean_distance(landmarks[5], landmarks[17])

def classify_finger_type(ratio):
    if ratio < 0.8:
        return "Short"
    elif ratio <= 0.9:
        return "Mid"
    else:
        return "Long"

def classify_palm_shape(aspect_ratio, finger_type):
    if aspect_ratio < 1.3:
        palm_shape = "Square"
    else:
        palm_shape = "Oblong"

    if palm_shape == "Square" and finger_type == "Short":
        return "Earth"
    elif palm_shape == "Square" and finger_type == "Long":
        return "Water"
    elif palm_shape == "Oblong" and finger_type == "Short":
        return "Fire"
    elif palm_shape == "Oblong" and finger_type == "Long":
        return "Air"
    elif finger_type == "Mid":
        # Additional classification for "Mid" fingers
        return "Air" if palm_shape == "Square" else "Fire"

def finger_meaning(finger_type):
    return {
        "Short": "Decisive and action-oriented.",
        "Mid": "Balanced and adaptable.",
        "Long": "Analytical and thoughtful."
    }[finger_type]

def palm_meaning(palm_type):
    return {
        "Fire": "Enthusiastic, energetic, and spontaneous.",
        "Earth": "Practical, grounded, and reliable.",
        "Air": "Intellectual, communicative, and curious.",
        "Water": "Sensitive, intuitive, and imaginative."
    }[palm_type]

def analyze_image(image_path, output_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_hands.Hands(static_image_mode=True, max_num_hands=1) as hands:
        result = hands.process(image_rgb)

        if not result.multi_hand_landmarks:
            print(f"[❌] No hand detected in {os.path.basename(image_path)}")
            return

        landmarks = result.multi_hand_landmarks[0].landmark

        avg_finger_len = get_avg_finger_length(landmarks)
        palm_len = get_palm_length(landmarks)
        palm_width = get_palm_width(landmarks)
        palm_height = palm_len

        finger_ratio = avg_finger_len / palm_len
        palm_aspect_ratio = palm_height / palm_width

        finger_type = classify_finger_type(finger_ratio)
        palm_type = classify_palm_shape(palm_aspect_ratio, finger_type)

        print(f"[✅] {os.path.basename(image_path)}")
        print(f"    → Finger Length: {finger_type} ({finger_meaning(finger_type)})")
        print(f"    → Palm Shape: {palm_type} Hand ({palm_meaning(palm_type)})\n")

        annotated = image.copy()
        mp_drawing.draw_landmarks(annotated, result.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)
        cv2.imwrite(output_path, annotated)

# ----------- Process all images in a folder -----------
input_folder = "test"
output_folder = "static"
os.makedirs(output_folder, exist_ok=True)

for file in os.listdir(input_folder):
    if file.lower().endswith((".png", ".jpg", ".jpeg")):
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, f"annotated_{file}")
        analyze_image(input_path, output_path)
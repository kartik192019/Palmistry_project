import cv2
import mediapipe as mp
import random

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
    if ratio < 0.7:
        return "Short"
    elif ratio <= 0.8:
        return "Mid"
    else:
        return "Long"

def classify_palm_shape(aspect_ratio, finger_type):
    palm_shape = "Oblong" if aspect_ratio < 1.1 else "Square"

    if palm_shape == "Square" and finger_type == "Short":
        return "Earth"
    elif palm_shape == "Square" and finger_type == "Long":
        return "Air"
    elif palm_shape == "Oblong" and finger_type == "Short":
        return "Fire"
    elif palm_shape == "Oblong" and finger_type == "Long":
        return "Water"
    elif finger_type == "Mid":
        return "Air" if palm_shape == "Square" else "Fire"

# ----------- Main Analysis Function -----------

def analyze_fingers(image_path, result_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_hands.Hands(static_image_mode=True, max_num_hands=1) as hands:
        result = hands.process(image_rgb)

        if not result.multi_hand_landmarks:
            return {
                "overall": "Unknown",
                "meaning": "Hand landmarks not detected.",
                "palm_shape": "Unknown",
                "palm_meaning": "Palm shape couldn't be analyzed.",
                "finger_desc": "No output.",
                "palm_desc": "No output."
            }

        landmarks = result.multi_hand_landmarks[0].landmark

        avg_finger_len = get_avg_finger_length(landmarks)
        palm_len = get_palm_length(landmarks)
        palm_width = get_palm_width(landmarks)
        palm_aspect_ratio = palm_len / palm_width

        finger_ratio = avg_finger_len / palm_len
        finger_type = classify_finger_type(finger_ratio)
        palm_type = classify_palm_shape(palm_aspect_ratio, finger_type)

        finger_desc = random.choice(finger_psychology[finger_type])
        palm_desc = random.choice(palm_psychology[palm_type])
        final_paragraph = f"You have {finger_type.lower()} fingers and a {palm_type} hand which conveys that {finger_desc} {palm_desc}"
        # Save annotated image
        annotated = image.copy()
        mp_drawing.draw_landmarks(annotated, result.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)
        cv2.imwrite(result_path, annotated)

        return {
            "analysis": final_paragraph,
            "result_path": result_path
        }
# ----------- Psychology Descriptions -----------

finger_psychology = {
    "Short": [
        "You’re always busy. Sometimes you may start something new before you’ve finished the last task. You often have several things on the go at the same time.You tend to want everything right now, so patience is not your strong suit. Your impulsiveness has gotten you into trouble in the past. In some ways you are a jack-of-all-trades."
    ],
    "Mid": [
        "At times you can be very patient. However, at other times you’re inclined to jump first and think later. If something really interests you, you want to get right down to the bottom of it and work it all out. If it’s only a passing interest, you’re more inclined to skim over it and not learn it in much detail."
    ],
    "Long": [
        "You enjoy complex work. You’re patient and enjoy all the fiddly bits – you like the details in things. Your work must be very consuming and gratifying. If it’s too simple you lose interest very quickly"
    ]
}

palm_psychology = {
    "Fire": [
        "You have a great mind, full of wonderful ideas. These ideas excite you. Your enthusiasm may not last for long, but it’s extremely important to you at the time. Your emotions can be a bit hard to handle at times, but they enable you to experience life to the fullest. Details are not your strong point and you tend to prefer the overall picture to the fiddly bits. You are likely to be creative and need to be busy to be happy."
    ],
    "Earth": [
        "You’re a hard worker. You enjoy physical challenges and your hands can think for themselves. You can be stubborn at times, and you don’t easily change your mind. You enjoy rhythm and movement. You’re not usually good with details, unless you’re making something. You probably prefer working outdoors, doing something practical. You’re reliable, honest and somewhat reserved"
    ],
    "Air": [
        "You’re intelligent, clear-thinking and discriminating. Relationships are important to you, but you sometimes find logic getting in the way of your feelings. You’re reliable and like to do things completely. You’re a stimulating companion and life is never dull when you’re around."
    ],
    "Water": [
        "You have an extremely rich inner life. Your imagination is keen and you fantasize about just about everything. You can be influenced by others, so you’re flexible with your ideas. Your intuition is strong. You’re emotional. If you’re interested in someone, you love spending time with them. You also need time by yourself to reflect on your own life. You are happiest inside the right relationship with someone to depend and rely upon."
    ]
}

# ----------- Helper Functions -----------
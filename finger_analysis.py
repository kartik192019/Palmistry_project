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
    if ratio < 0.9:
        return "Short"
    elif ratio <= 1.0:
        return "Mid"
    else:
        return "Long"

def classify_palm_shape(aspect_ratio, finger_type):
    palm_shape = "Oblong" if aspect_ratio > 1.3 else "Square"
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
        talent_desc = random.choice(palm_talent_career[palm_type])

        final_paragraph = (
            f"You have {finger_type.lower()} fingers and a {palm_type} hand. "
            f"This suggests: \n\n"
            f"Personality Insight  ---->  {finger_desc} {palm_desc}\n\n "
            f"Talent & Career Insight  ---->  {talent_desc}"
        )

        # Save annotated image
        annotated = image.copy()
        mp_drawing.draw_landmarks(annotated, result.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)
        cv2.imwrite(result_path, annotated)

        return {
            "analysis": final_paragraph,
            "result_path": result_path,
            "palm_shape": palm_type
        }

# ----------- Psychology Descriptions -----------

finger_psychology = {
    "Short": [
        "You’re always busy. Sometimes you may start something new before you’ve finished the last task. You often have several things on the go at the same time.You tend to want everything right now, so patience is not your strong suit. Your impulsiveness has gotten you into trouble in the past. In some ways you are a jack-of-all-trades.",
        "You dive into things without much hesitation and your curiosity keeps life exciting. However, follow-through isn’t your strongest skill. You thrive in chaos and seem to function best juggling multiple projects, but structure may not be your best friend.",
        "Multitasking is your middle name. You act fast, think fast, and sometimes forget to pause. While this can be thrilling, it may lead to frequent restarts. Still, your energy is infectious and people often admire your go-getter attitude."
    ],
    "Mid": [
        "At times you can be very patient. However, at other times you’re inclined to jump first and think later. If something really interests you, you want to get right down to the bottom of it and work it all out. If it’s only a passing interest, you’re more inclined to skim over it and not learn it in much detail.",
        "You possess a flexible mind—sometimes contemplative, sometimes impulsive. When engaged, you’re all in. But when disinterested, even caffeine can’t help. You dance between thinker and doer depending on your mood or the moon, maybe both.",
        "Balanced in approach, you may not always finish what you start, but you make up for it with curiosity. Deep dives only happen when something grabs you; otherwise, you’re off to explore the next shiny idea in the distance."
    ],
    "Long": [
        "You enjoy complex work. You’re patient and enjoy all the fiddly bits – you like the details in things. Your work must be very consuming and gratifying. If it’s too simple you lose interest very quickly.",
        "Detail-oriented to a fault, you find pleasure in puzzles that others abandon. Monotony bores you, but intricate projects that require finesse and depth? That’s your playground. Complexity brings you calm.",
        "Your patience is your power. You take the scenic route, absorbing every detail like a sponge. Simplicity doesn’t satisfy you—you're wired for rich, layered experiences where every piece matters."
    ]
}

palm_psychology = {
    "Fire": [
        "Fire is hot, energizing and constantly moving.You have a great mind, full of wonderful ideas. These ideas excite you. Your enthusiasm may not last for long, but it’s extremely important to you at the time. Your emotions can be a bit hard to handle at times, but they enable you to experience life to the fullest. Details are not your strong point and you tend to prefer the overall picture to the fiddly bits. You are likely to be creative and need to be busy to be happy.",
        "Your spark lights up a room, and your mind races with ideas. You love novelty and stimulation, though your passion can fizzle fast. Emotions run high, but they’re part of your magic. Boredom is your nemesis, adventure your muse.",
        "Like a wildfire, you blaze brightly with energy and ambition. Your creativity knows no bounds. Though focus might wander, your big-picture thinking is unmatched. You thrive in motion, not in monotony."
    ],
    "Earth": [
        "Earth is the dry, solid part of our planet. Everything that happens on earth is subject to the natural rhythms of germination, growth, death and decay. You’re a hard worker. You enjoy physical challenges and your hands can think for themselves. You can be stubborn at times, and you don’t easily change your mind. You enjoy rhythm and movement. You’re not usually good with details, unless you’re making something. You probably prefer working outdoors, doing something practical.",
        "Grounded and reliable, you’re not easily swayed. You value routine, and your hands seem to have their own intelligence. You might not fuss over small details—unless you're building something with care. Nature calls you often.",
        "You march to your own rhythm, usually a practical and productive one. Routine suits you, and your stubborn streak ensures you stick to your goals. You enjoy hands-on work and thrive when you’re building or fixing things."
    ],
    "Air": [
        "Air is essential for life. We take it for granted and seldom notice it, except on windy days. Air is also essential for communications, as it carries sound waves. You’re intelligent, clear-thinking and discriminating. Relationships are important to you, but you sometimes find logic getting in the way of your feelings. You’re reliable and like to do things completely. You’re a stimulating companion and life is never dull when you’re around.",
        "Sharp-witted and analytical, your mind never sits still. You often hover between intellect and empathy, sometimes choosing reason over heart. Conversation is your playground, and you bring a breeze of clarity wherever you go.",
        "You think fast and speak clearly, but feelings sometimes get stuck in the filter of logic. Still, you’re loyal, insightful, and curious. Friends appreciate your thoughtful advice and your knack for turning small talk into deep dives."
    ],
    "Water": [
        "Water is essential. Other forces have to act upon it to make it change. It’s also shapeless as it simply moves to fill up whatever space is available. You have an extremely rich inner life. Your imagination is keen and you fantasize about just about everything. You can be influenced by others, so you’re flexible with your ideas. Your intuition is strong. You’re emotional. If you’re interested in someone, you love spending time with them. You also need time by yourself to reflect on your own life. You are happiest inside the right relationship with someone to depend and rely upon",
        "Deep and intuitive, your thoughts flow like a quiet stream. You're highly empathetic, and though easily influenced, you bring a sense of calm to those around you. You cherish meaningful connection and recharge in solitude.",
        "Your emotions run deep, like an ocean current. You feel everything intensely—joy, sorrow, inspiration. You're artistic and sensitive, often dreaming with your eyes open. You need space, silence, and soulful bonds to feel fulfilled."
    ]
}

palm_talent_career = {
    "Fire": [
        "The person with a Fire Hand will use intuition to make quick decisions. He or she will need change, variety and some way to express themselves. They would be good at sales or any other career where they’re left to “get on with it.”",
        "Quick on their feet and even quicker with ideas, Fire Hand individuals thrive in fast-paced roles. Marketing, startups, or event planning would let them unleash their creativity while staying engaged.",
        "Change isn’t scary—it’s essential. Fire types excel in dynamic work environments like travel journalism, entrepreneurship, or anything that doesn’t involve a desk and routine. Their passion sells ideas before the pitch is even over."
    ],
    "Earth": [
        "You will enjoy repetitive tasks and relish practical work. This person will be reliable, honest and have hands that can think for themselves. They would be happy as a carpenter, plumber, mechanic or any field where they can use their head and hands.",
        "Earth Hand folks are builders of the world—mechanics, farmers, engineers. They flourish in jobs with routine and physicality, where results can be seen, touched, or repaired.",
        "Hands-on work suits Earth types best—whether it’s woodwork, gardening, or running a workshop. Their patience and persistence make them perfect for long-term, skill-based careers."
    ],
    "Air": [
        "They will be happy in a field where they can communicate with others. Radio broadcasting, television announcing, teaching and sales would all be good career choices for this person. They’ll actively use the analytical side of their brain and be reliable and conscientious.",
        "Air Hand individuals are made for intellectual conversations and verbal agility. They’d thrive as writers, public speakers, or data analysts—anything that blends logic with communication.",
        "Teaching, journalism, and tech support are natural habitats for Air types. Their ability to simplify complex ideas makes them a gift to curious minds everywhere."
    ],
    "Water": [
        "Someone with a Water Hand will need pleasant surroundings and work that provides aesthetic pleasure. If this person is creative, they’ll be able to develop this talent, but may need constant encouragement from family and friends to keep working. Suitable careers would include interior design, fashion and theatre.",
        "Water Hands flow best in art studios, film sets, or peaceful therapy rooms. They crave calm environments where their emotional depth and creativity can thrive without judgment.",
        "Idealistic and intuitive, they’re drawn to emotionally meaningful careers—art therapy, floral design, acting, or music. Their challenge isn’t creativity, but consistency—and a little support goes a long way."
    ]
}
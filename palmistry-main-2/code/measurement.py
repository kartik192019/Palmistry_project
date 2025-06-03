from PIL import Image, ImageDraw
import cv2
import mediapipe as mp
import random

contents = []

def measure(path_to_warped_image_mini, lines):
    global contents
    heart_thres_x = 0
    head_thres_x = 0
    life_thres_y = 0

    mp_hands = mp.solutions.hands
    with mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5) as hands:
        image = cv2.flip(cv2.imread(path_to_warped_image_mini), 1)
        image_height, image_width, _ = image.shape

        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        hand_landmarks = results.multi_hand_landmarks[0]

        zero = hand_landmarks.landmark[mp_hands.HandLandmark(0).value].y
        one = hand_landmarks.landmark[mp_hands.HandLandmark(1).value].y
        five = hand_landmarks.landmark[mp_hands.HandLandmark(5).value].x
        nine = hand_landmarks.landmark[mp_hands.HandLandmark(9).value].x
        thirteen = hand_landmarks.landmark[mp_hands.HandLandmark(13).value].x

        heart_thres_x = image_width * (1 - (nine + (five - nine) * 2 / 5))
        head_thres_x = image_width * (1 - (thirteen + (nine - thirteen) / 3))
        life_thres_y = image_height * (one + (zero - one) / 3)

    im = Image.open(path_to_warped_image_mini)
    width = 3
    if (None in lines) or (len(lines) < 3):
        return None, None
    else:
        draw = ImageDraw.Draw(im)

        heart_line = lines[0]
        head_line = lines[1]
        life_line = lines[2]

        # --- HEART LINE ---
        heart_line_points = [tuple(reversed(l[:2])) for l in heart_line]
        heart_line_tip = heart_line_points[0]
        draw.line(heart_line_points, fill="red", width=width)

        heart_content_1 = (
            "The Heart Line reflects your emotional core. It's the pulse of your affection, "
            "your empathy, and your romantic compass. In palmistry, this line tells us how you love"
        )

        if heart_line_tip[0] < heart_thres_x:
            heart_content_2_variants = [
                "Your Heart Line stretches far, indicating deep, lasting love. You’re in it for the long haul — love, loyalty, and probably playlist-sharing too. You carry love in your bones, not just your heart. Relationships aren’t fleeting connections for you — they’re lifelong investments. You're the type to remember anniversaries, favourite colours, and how someone takes their tea. Your love runs deep and details matter. A long Heart Line like yours reflects someone who treasures connection, who believes in ‘forever’, and who can feel a heartbreak in high definition.  ",
                "A long Heart Line means you're emotionally generous. You invest wholeheartedly and love like you’re writing a sonnet every time.A long Heart Line like yours reflects someone who treasures connection, who believes in ‘forever’, and who can feel a heartbreak in high definition. Love is no passing cloud for you — it's an epic saga, full of feels, late-night calls, and poetic texts. You don’t love halfway — you dive in, headfirst, no lifejacket. Your emotional spectrum is broad, colourful, and intense — your love isn’t lukewarm, it’s lava-hot"
            ]
        else:
            heart_content_2_variants = [
                "Your Heart Line is short and sweet — just like your approach to relationships. Quick sparks, passionate moments, and you’re off to the next adventure. With a concise Heart Line, you likely prioritise quality over quantity. You love with intention, and you’re selective about who earns your emotional investment. You live in the moment and love in the now. You may not send love letters, but your DMs are legendary. Romance for you is about joy, connection, and growth — not emotional weight-lifting. You care, just with boundaries and clarity. ",
                "Short Heart Line? You’re a sampler of life’s emotional buffet. Diverse, dynamic, and always interesting. You’re not cold — just clear. You know that love is a dance, not a chain, and you won’t settle for anything less than mutual harmony. You believe every connection teaches something new. Even brief romances leave fingerprints on your heart. values mutual freedom, and isn’t afraid to walk away when the rhythm fades. Your style of love is modern, free-spirited, and refreshingly honest."
            ]
        heart_content_2 = random.choice(heart_content_2_variants)

        # --- HEAD LINE ---
        head_line_points = [tuple(reversed(l[:2])) for l in head_line]
        head_line_tip = head_line_points[-1]
        draw.line(head_line_points, fill="green", width=width)

        head_content_1 = (
            "The Head Line governs how you think. It's not just about intellect, but the very framework "
            "of your decision-making, logic, imagination, and how you solve life’s puzzles. "
        )

        if head_line_tip[0] > head_thres_x:
            head_content_2_variants = [
                "You have a long Head Line — meaning your brain has a season pass to every idea theme park. Inventive, curious, and always expanding. as you are charting blueprints to ground them. Innovation isn’t a skill for you — it’s a reflex. Your mind is a deep ocean. You're not content with surface-level knowledge — you dive deep and emerge with pearls of wisdom. You’re a big-picture thinker, someone who considers not just the ‘how’, but the ‘why’ and the ‘what next’. When others pause, you ponder. ",
                "Analytical yet imaginative, you're the type who can design a spaceship... and then paint it with starry art. You have a cinematic imagination. A long Head Line suggests deep thought, strategic planning, and a love for the abstract. Your thoughts wander far and wide — sometimes even forgetting where they were headed, but always picking up treasures along the way. Your thoughts travel like epic sagas — elaborate, expansive, and visionary. You see the connections others miss, and you’re as comfortable building castles in the air  "
            ]
        else:
            head_content_2_variants = [
                "Short Head Line? Focused and fierce. You pick a topic and conquer it like a champion playing trivia night. You’re decisive, efficient, and grounded in reality — a natural problem-solver who doesn’t chase mental rabbit holes.You have a creative, imaginative approach to everything you do. Your work must be interesting, or you quickly lose focus. You work best in aesthetic surroundings and appreciate the finer things in life. You have refined tastes.",
                "You’re a deep thinker — just not a wide one. What you lack in range, you make up for in razor-sharp insights. You don’t dwell, you decide. Your clarity cuts through confusion like a laser through fog. When life gets messy, you get moving. One subject at a time is your mantra. You're like a laser beam — narrow focus, but incredibly powerful. You’d rather master one thing than dabble in many. Your mental compass is finely tuned. You prefer clean, clear logic over dreamy ideals."
            ]
        head_content_2 = random.choice(head_content_2_variants)

        # --- LIFE LINE ---
        life_line_points = [tuple(reversed(l[:2])) for l in life_line]
        life_line_tip = life_line_points[-1]
        draw.line(life_line_points, fill="blue", width=width)

        life_content_1 = (
            "The Life Line reveals vitality, enthusiasm, and how energetically you live. "
            "It's not about how long you live, but how well you *live*. "
        )

        if life_line_tip[1] > life_thres_y:
            life_content_2_variants = [
                "You’re a team player and problem-solver — the kind who hosts game nights and offers emotional support with snacks. A Life Line close to the thumb suggests a more conservative use of energy. You may recharge alone, take careful steps, and choose depth over dazzle. Energy meets empathy in you. You take people along for the ride and never leave anyone behind. You’re a thoughtful soul — not one to leap before looking. A tighter Life Line implies you conserve your strength, make strategic moves,  ",
                "You believe life is better shared — whether it’s meals, moments, or morning walks. Reserved yet resilient, you conserve your fire for what truly matters. A closely-drawn Life Line shows a preference for peace, stability, and emotional grounding. You gain strength from others. The more the merrier, and your circle is full of laughter and loyalty. and live with intentionality. You may not seek drama, but you definitely create impact. Quiet strength defines you."
            ]
        else:
            life_content_2_variants = [
                "Your Life Line suggests a solo warrior’s path. You need no map — your instincts are your guide. You live like it’s a story worth telling. A wide Life Line reflects vigour, optimism, and a love for motion — both physical and emotional. You’re fiercely independent — you’ve probably tried assembling furniture without the manual (and succeeded). You live like it’s a story worth telling. A wide Life Line reflects vigour, optimism, and a love for motion — both physical and emotional.",
                "You recharge best in solitude and prefer solving life’s puzzles your own way. You're not antisocial, just selectively social. You prefer the quiet roar of your thoughts over the noise of a crowd. Zen mode: always on. You’re here to experience, to evolve, and to say yes to what sets your soul on fire. A wide Life Line reflects vigour, optimism, and a love for motion — both physical and emotional.  "
            ]
        life_content_2 = random.choice(life_content_2_variants)

        # Final collected content
        contents = [
            heart_content_1, heart_content_2,
            head_content_1, head_content_2,
            life_content_1, life_content_2
        ]

        return im, contents
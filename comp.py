from flask import Flask, render_template, request, jsonify
from finger_analysis import analyze_fingers
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'static/results'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Compatibility messages
compatibility_chart = {
    ("Fire", "Fire"): "🔥🔥 Double fire? Sparks are flying! It’s a positive sign you both have the same type of hands. You’re both passionate, energetic, and spontaneous. Think weekend getaways planned on impulse, deep conversations at 3 AM, and lots of fiery debates that end in laughter. But beware — two fires can ignite into something powerful or burn out fast if neither cools down occasionally. You thrive on adventure and challenge — just don’t forget to pack patience along the way.",
    
    ("Fire", "Air"): "🔥💨 A legendary match! Air fans Fire's flames, turning sparks into fireworks. You two energize each other — one throws out bold ideas, the other runs with them. Expect thrilling adventures, creative projects, and playful banter. Communication flows effortlessly, and passion follows right behind. Just make sure Air doesn’t blow too hard, or Fire might flicker from the chaos.",
    ("Air", "Fire"): "🔥💨 A legendary match! Air fans Fire's flames, turning sparks into fireworks. You two energize each other — one throws out bold ideas, the other runs with them. Expect thrilling adventures, creative projects, and playful banter. Communication flows effortlessly, and passion follows right behind. Just make sure Air doesn’t blow too hard, or Fire might flicker from the chaos.",
    ("Fire", "Earth"): "🔥🌍 Opposites trying to make it work. Fire is all about action and movement, while Earth is steady and grounded. Fire may see Earth as too slow, Earth may see Fire as reckless. But if you find your rhythm, you can build something lasting — Fire brings inspiration, Earth brings stability. Just don’t try to change each other. Think of this as a volcano: slow-building, but capable of great things if respected.",
    ("Earth", "Fire"): "🔥🌍 Opposites trying to make it work. Fire is all about action and movement, while Earth is steady and grounded. Fire may see Earth as too slow, Earth may see Fire as reckless. But if you find your rhythm, you can build something lasting — Fire brings inspiration, Earth brings stability. Just don’t try to change each other. Think of this as a volcano: slow-building, but capable of great things if respected.",
    ("Fire", "Water"): "🔥💧 An intense, steamy mix — or a recipe for emotional floods. Fire is bold and expressive, Water is deep and sensitive. Water might feel overwhelmed by Fire’s intensity, while Fire might feel doused by Water’s moods. Still, the contrast can be magnetic. If you both learn to balance passion with empathy, this can become an unforgettable love story with all the drama of a romance novel — just add trust.",
    ("Water", "Fire"): "🔥💧 An intense, steamy mix — or a recipe for emotional floods. Fire is bold and expressive, Water is deep and sensitive. Water might feel overwhelmed by Fire’s intensity, while Fire might feel doused by Water’s moods. Still, the contrast can be magnetic. If you both learn to balance passion with empathy, this can become an unforgettable love story with all the drama of a romance novel — just add trust.",
    ("Earth", "Earth"): "🌍🌍 Solid as a rock. It’s a positive sign you both have the same type of hands. This is the kind of match where both partners value loyalty, long-term goals, and shared routines. Think slow-burning love, stable homes, and a deep sense of peace. While spontaneity might not be your thing, you’ll always know where you stand. Just be careful not to get stuck in the mud — shake things up once in a while to keep the spark alive.",
    
    ("Earth", "Water"): "🌍💧 A nurturing, emotionally grounded bond. Water brings emotional intelligence and empathy, while Earth offers stability and support. It’s like a garden — with Earth as soil and Water as rain, you two help each other grow. Expect quiet nights, deep talks, and a feeling of home. There’s a natural rhythm here that feels timeless. Soulmate energy, if you let it bloom.",
    ("Water", "Earth"): "🌍💧 A nurturing, emotionally grounded bond. Water brings emotional intelligence and empathy, while Earth offers stability and support. It’s like a garden — with Earth as soil and Water as rain, you two help each other grow. Expect quiet nights, deep talks, and a feeling of home. There’s a natural rhythm here that feels timeless. Soulmate energy, if you let it bloom.",
    ("Earth", "Air"): "🌍💨 A practical dreamer and a dreamy realist walk into a relationship... and it just might work! Air brings fresh ideas and new perspectives, Earth turns them into reality. Air may find Earth too slow, and Earth may find Air too flighty — but together, you’re the bridge between imagination and manifestation. You ground each other in beautiful ways. Respect the differences and the rest will fall into place.",
    ("Air", "Earth"): "🌍💨 A practical dreamer and a dreamy realist walk into a relationship... and it just might work! Air brings fresh ideas and new perspectives, Earth turns them into reality. Air may find Earth too slow, and Earth may find Air too flighty — but together, you’re the bridge between imagination and manifestation. You ground each other in beautiful ways. Respect the differences and the rest will fall into place.",
    ("Air", "Air"): "💨💨 Two free spirits soaring through conversations, dreams, and inside jokes. It’s a positive sign you both have the same type of hands. You understand each other’s need for independence, mental stimulation, and novelty. Life with you two is anything but boring — it’s a whirlwind of creativity, social adventures, and endless intellectual flirtation. Just watch for commitment issues — someone has to land eventually.",
    
    ("Air", "Water"): "💨💧 Logic meets emotion in this intriguing union. Air wants clarity and conversation, Water craves depth and connection. You’ll need patience — Air might struggle with Water’s emotional waves, and Water might feel unheard by Air’s rational lens. But when balanced, this duo can write poetry together — one pens the words, the other feels them. It’s a heart-and-mind harmony waiting to happen.",
    ("Water", "Air"): "💨💧 Logic meets emotion in this intriguing union. Air wants clarity and conversation, Water craves depth and connection. You’ll need patience — Air might struggle with Water’s emotional waves, and Water might feel unheard by Air’s rational lens. But when balanced, this duo can write poetry together — one pens the words, the other feels them. It’s a heart-and-mind harmony waiting to happen.",
    ("Water", "Water"): "💧💧 Deep calls unto deep. This match is a sea of emotion, intuition, and shared understanding. It’s a positive sign you both have the same type of hands. You’ll finish each other’s sentences, sense each other’s moods, and connect on a soulful level. But beware — too much water can flood the relationship with sensitivity and overthinking. You’ll need healthy boundaries and lots of communication. Think twin souls adrift on a dreamy sea.",
}

def get_compatibility(palm1, palm2):
    key1 = (palm1, palm2)
    key2 = (palm2, palm1)
    return compatibility_chart.get(key1) or compatibility_chart.get(key2) or \
        "You're a unique pair — this combination isn't common, but opposites often attract!"

@app.route("/")
def index():
    return render_template("index2.html")

@app.route("/compatibility", methods=["POST"])
def compatibility():
    file1 = request.files["file1"]
    file2 = request.files["file2"]

    unique_id1 = str(uuid.uuid4())
    unique_id2 = str(uuid.uuid4())

    path1 = os.path.join(UPLOAD_FOLDER, f"{unique_id1}.jpg")
    path2 = os.path.join(UPLOAD_FOLDER, f"{unique_id2}.jpg")

    result_filename1 = f"annotated_{unique_id1}.jpg"
    result_filename2 = f"annotated_{unique_id2}.jpg"

    result_path1 = os.path.join(RESULT_FOLDER, result_filename1)
    result_path2 = os.path.join(RESULT_FOLDER, result_filename2)

    file1.save(path1)
    file2.save(path2)

    # Analyze both hands
    result1 = analyze_fingers(path1, result_path1)
    result2 = analyze_fingers(path2, result_path2)

    palm_type1 = result1['palm_shape']
    palm_type2 = result2['palm_shape']

    compatibility_text = get_compatibility(palm_type1, palm_type2)

    return jsonify({
        "image1_url": f"/static/results/{result_filename1}",
        "image2_url": f"/static/results/{result_filename2}",
        "palm_type1": palm_type1,
        "palm_type2": palm_type2,
        "compatibility_text": compatibility_text
    })

if __name__ == "__main__":
    app.run(port=5003)
from flask import Flask, render_template, request, jsonify
from finger_analysis import analyze_fingers
import os
import uuid
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'static/results'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

def get_zodiac_sign(dob_str):
    date = datetime.strptime(dob_str, "%Y-%m-%d")
    day, month = date.day, date.month
    zodiac = [
        ("Capricorn",  (12, 22), (1, 19)),
        ("Aquarius",   (1, 20),  (2, 18)),
        ("Pisces",     (2, 19),  (3, 20)),
        ("Aries",      (3, 21),  (4, 19)),
        ("Taurus",     (4, 20),  (5, 20)),
        ("Gemini",     (5, 21),  (6, 20)),
        ("Cancer",     (6, 21),  (7, 22)),
        ("Leo",        (7, 23),  (8, 22)),
        ("Virgo",      (8, 23),  (9, 22)),
        ("Libra",      (9, 23),  (10, 22)),
        ("Scorpio",    (10, 23), (11, 21)),
        ("Sagittarius",(11, 22), (12, 21))
    ]
    for sign, start, end in zodiac:
        if (month == start[0] and day >= start[1]) or (month == end[0] and day <= end[1]):
            return sign
    return "Capricorn"

def get_gender_message(gender):
    messages = {
        "male": "your approach to challenges is often rooted in logic and resilience. You bring strength, protection, and drive to all areas of your life.",
        "female": "your intuitive power shines through. You bring nurturing energy, depth of emotion, and inner strength to those around you.",
    }
    return messages.get(gender.lower(), "You are wonderfully individualistic and defy conventional boundaries with grace.")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    dob = request.form["dob"]
    gender = request.form["gender"]
    file = request.files["file"]

    unique_id = str(uuid.uuid4())
    image_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}.jpg")
    result_filename = f"annotated_{unique_id}.jpg"
    result_path = os.path.join(RESULT_FOLDER, result_filename)
    file.save(image_path)

    # Core palm analysis
    results = analyze_fingers(image_path, result_path)
    
    # If analysis failed, return error message
    if 'analysis' not in results:
        return jsonify({
            "error": "Could not detect hand in the image. Please try again with a clearer image of your palm.",
            "success": False
        }), 400

    # Zodiac + Gender Analysis
    zodiac_sign = get_zodiac_sign(dob)
    gender_text = get_gender_message(gender)

    zodiac_description = {
        "Aries": "You're driven and bold, often blazing trails where others hesitate.",
        "Taurus": "You're grounded, loyal, and drawn to beauty and comfort.",
        "Gemini": "Your dual nature makes you both social and thoughtful — full of curiosity.",
        "Cancer": "You lead with your heart, offering empathy, intuition, and fierce protection.",
        "Leo": "You radiate confidence and leadership, with a heart that seeks recognition and love.",
        "Virgo": "Detail-oriented and reliable, your analytical mind keeps things running smoothly.",
        "Libra": "You seek harmony, beauty, and justice — a peaceful force in every space.",
        "Scorpio": "You're intense, passionate, and deeply perceptive of life's mysteries.",
        "Sagittarius": "A true explorer, your heart seeks knowledge, philosophy, and freedom.",
        "Capricorn": "Ambitious and structured, you manifest visions into reality.",
        "Aquarius": "Independent, inventive, and idealistic, you challenge norms to better the world.",
        "Pisces": "Dreamy, artistic, and deeply empathetic, your soul feels the world in waves."
    }

    zodiac_text = zodiac_description.get(zodiac_sign, "")

    full_analysis = f"{results['analysis']}\n\n" \
                    f"\n{gender_text}\n\n" \
                    f"Zodiac sign --> {zodiac_sign}.\n\n" \
                    f" Zodiac insight : \n{zodiac_text}"

    return jsonify({
        "analysis": full_analysis,
        "annotated_image_url": f"/static/results/{result_filename}"
    })

if __name__ == "__main__":
    app.run(port=5001)
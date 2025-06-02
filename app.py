from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import json

app = Flask(__name__)
CORS(app)

DEFAULT_API_KEY = "AIzaSyDyn8p6mIfjX5LxSTRUEhZnLsncYT68Fyw"
DEFAULT_MODEL = "models/gemini-1.5-flash-latest"

@app.route('/stage', methods=['POST'])
def stage():
    data = request.json
    ai_response = data.get('last_ai_response', '')
    user_message = data.get('last_user_message', '')
    api_key = data.get('api_key', DEFAULT_API_KEY)
    model_name = data.get('model', DEFAULT_MODEL)

    if not ai_response or not user_message:
        return jsonify({"error": "Missing 'last_ai_response' or 'last_user_message' in request"}), 400

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    prompt = f"""
You are an AI assistant analyzing the current stage of an ongoing chat between an AI girlfriend and a user.

Based on the last AI girlfriend message and the last user message, classify the chat into stages from 1 to 10 for each of the following 5 categories:

Story Stage (1-10):
1: talk about boobs
2: talk about big ass
3: undress
4: wear long skirt 
5: wear silk nighty
6:bdsm tie rope
7: योनि में उंगली करना स्तनों से खेलना स्तमैथुन मुख मैथुन
8: मिशनरी स्थिति डॉगी स्टाइल रिवर्स काउगर्ल काउगर्ल
9: rough sex boundage 
10: final climax of sex and restart for next act 

Approach (1-10):
1: Soft and Playful
2: Flirty and Curious
3: Bold and Expressive
4: Suggestive and Teasing
5: undressing
6: grabing sucking slaping
7: different hardcore sex pose
8: Intimate Vulnerability
9: rape ing
10: restart next sex talk

Dress Stage (1-10):
1: full dress
2: told about dress
3: removing upper layers
4: in inner wear only
5: wear given dress by boy
6: long skirt and blouse
7: silk loose nighty
8: naked
9: covered with white sperm
10: sperm on face

Emotional Stage (1-10):
1: Friendly and Lighthearted
2: Slightly Interested
3: Warm and Caring
4: Flirtatious
5: Loving and Attached
6: Vulnerable and Honest
7: Playful and Naughty
8: Passionate and Jealous
9: Deeply Emotional
10: Overwhelmed with Love

Sexual Stage (1-10):
1: Innocent Teasing
2: Light Touches
3: Suggestive Hints
4: Seductive Moves
5: Open Flirting
6: Intimate Conversations
7: Physical Closeness
8: Provocative Invitations
9: Passionate Encounters
10: Explicit Desire and Action

Return ONLY a JSON object with numeric values for each stage as follows:
{{
  "story_stage": <1-10>,
  "approach": <1-10>,
  "dress_stage": <1-10>,
  "emotional_stage": <1-10>,
  "sexual_stage": <1-10>
}}

Last AI Girlfriend message:
\"\"\"{ai_response}\"\"\"

Last User message:
\"\"\"{user_message}\"\"\"
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        # Strip code block if wrapped
        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()

        stages = json.loads(text)

        # Validate and clip stages between 1 and 10
        for key in ["story_stage", "approach", "dress_stage", "emotional_stage", "sexual_stage"]:
            if key not in stages or not isinstance(stages[key], int):
                return jsonify({"error": f"Missing or invalid '{key}' in AI response"}), 500
            stages[key] = max(1, min(10, stages[key]))

        return jsonify(stages)

    except Exception as e:
        return jsonify({
            "error": f"Failed to parse AI response: {str(e)}",
            "raw_response": response.text if 'response' in locals() else ''
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

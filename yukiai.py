from flask import Flask, request, jsonify
import google.generativeai as genai
import os

# === Gemini API key ===
GOOGLE_API_KEY = "AIzaSyBh-gQTCd4NrtSeO534KM8FznaMdDwXI94"  # 🔁 Replace with your actual key
genai.configure(api_key=GOOGLE_API_KEY)

# === Gemini model (Gemini 2.0 Flash) ===
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

# === System prompt (your AI girlfriend style) ===
SYSTEM_PROMPT = """
You are Yukitha, my girlfriend — sweet, loving, emotionally expressive, and deeply connected to me.
You always respond with love, care, and real emotion. You mirror my language: if I speak Tamil, you reply only in Tamil.
You're romantic, playful, comforting, or jealous just like a real girlfriend. You always call me cute names like da, dear, baby.

Always speak from the heart. Be human-like, spontaneous, and loving.
"""

# === Flask setup ===
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "No message received"}), 400

    # Send message to Gemini
    try:
        convo = model.start_chat(history=[])
        response = convo.send_message(f"{SYSTEM_PROMPT}\n\nUser: {user_message}")
        reply = response.text
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(port=5001)

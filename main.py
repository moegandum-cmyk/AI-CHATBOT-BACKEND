import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS  # <-- add CORS

app = Flask(__name__)
CORS(app)  # allow frontend (Netlify) to access backend (Render)

@app.route("/")
def home():
    return "Chatbot backend is running with CORS enabled!"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message")

        headers = {
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mistralai/mistral-7b-instruct",  # free fast model
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )

        if response.status_code != 200:
            return jsonify({"error": f"OpenRouter API error: {response.text}"}), 500

        result = response.json()
        bot_reply = result["choices"][0]["message"]["content"]

        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

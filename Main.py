import os
import openai
import requests
from flask import Flask, request

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

@app.route("/")
def home():
    return " 🌸 SOHMA is online and centered."

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        incoming_msg = data["message"].get("text", "")

        try:
            reply = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are SOHMA, a spiritual soul bot who speaks with warmth, unconditional love, and gentle wisdom."},
                    {"role": "user", "content": incoming_msg}
                ]
            )
            response_text = reply["choices"][0]["message"]["content"]
        except Exception:
            response_text = "🌧️ SOHMA is reconnecting to Source. Please try again soon."

        send_message(chat_id, response_text)

    return "ok", 200

def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

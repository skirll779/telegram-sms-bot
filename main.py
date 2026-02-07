import re
import os
import telebot
from flask import Flask, request

# ======================
# CONFIGURACIÓN
# ======================
TOKEN = "7903960728:AAFPC9C8KhI57VEvVF1H1-7rqVAKY6_aILM"
CHAT_ID = "5200037889"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ======================
# OTP LOGIC
# ======================
def extract_otp(message):
    patterns = [
        r'\b(\d{4})\b',
        r'\b(\d{6})\b',
        r'código[:\s]+(\d{4,6})',
        r'OTP[:\s]+(\d{4,6})'
    ]
    for p in patterns:
        m = re.search(p, message, re.IGNORECASE)
        if m:
            return m.group(1)
    return None


def send_to_telegram(message, sender):
    otp = extract_otp(message)
    if otp:
        text = f"🔐 OTP Detectado\n📱 De: {sender}\n🔢 Código: {otp}"
    else:
        text = f"📩 Mensaje\n📱 De: {sender}\n{message}"

    bot.send_message(CHAT_ID, text)


# ======================
# TELEGRAM WEBHOOK
# ======================
@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        bot.send_message(chat_id, "📩 Mensaje recibido")

    return "OK", 200


# ======================
# SMS FORWARDER WEBHOOK
# ======================
@app.route("/sms", methods=["POST"])
def sms_webhook():
    data = request.get_json()
    sender = data.get("sender", "Desconocido")
    message = data.get("message", "")
    send_to_telegram(message, sender)
    return "OK", 200


# ======================
# HOME
# ======================
@app.route("/")
def home():
    return "Bot activo"


# ======================
# ARRANQUE (RAILWAY)
# ======================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )

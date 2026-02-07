import telebot
import re
from flask import Flask, request
import threading
import os

# ======================
# CONFIGURACIÓN
# ======================
TOKEN = "7903960728:AAFPC9C8KhI57VEvVF1H1-7rqVAKY6_aILM"
CHAT_ID = "5200037889"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ======================
# BOT TELEGRAM
# ======================
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "✅ Bot activo.\nEnvía mensajes o espera OTP.")


@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.send_message(message.chat.id, "📩 Mensaje recibido")


# ======================
# OTP LOGIC
# ======================
def extract_otp(message):
    patterns = [
        r'\b(\d{4})\b', r'\b(\d{6})\b', r'código[:\s]+(\d{4,6})',
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
# WEBHOOK & PREVIEW
# ======================
@app.route('/')
def index():
    public_url = f"https://{os.environ.get('REPLIT_DEV_DOMAIN')}"
    return f"""
    <h1>✅ Bot activo</h1>
    <p>El servidor y el bot de Telegram están funcionando correctamente.</p>
    <p><b>Tu URL de Webhook es:</b> <code>{public_url}/webhook</code></p>
    """

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    sender = data.get('sender', 'Desconocido')
    message = data.get('message', '')
    send_to_telegram(message, sender)
    return 'OK'


# ======================
# ARRANQUE
# ======================
def run_flask():
    app.run(host='0.0.0.0', port=5000)


if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.polling(none_stop=True)

from flask import Flask, request
from zalo_bot import Bot, Update
from zalo_bot.ext import Dispatcher, CommandHandler, MessageHandler, filters

BOT_TOKEN = "3222229135581534944:CTggeFHwGxfZaLeIBppjLsapWDhrNHaoSiLhhvfeuFmOdgrhdIYmabRTKofimvOU"
SECRET_TOKEN = "new_secret_123"

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

# ===== HANDLERS (KHÔNG ASYNC) =====
def start(update, context):
    update.message.reply_text("Xin chào! Tôi là Zalo Bot 👋")

def echo(update, context):
    update.message.reply_text(f"Bạn vừa nói: {update.message.text}")

# ===== DISPATCHER =====
dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# ===== WEBHOOK =====
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    print("=== WEBHOOK DATA ===")
    print(data)

    # Trường hợp Zalo gửi payload trực tiếp
    payload = data.get("result") if isinstance(data, dict) else None

    # Nếu không có result thì bỏ qua
    if not payload:
        return "ok"

    update = Update.de_json(payload, bot)
    dispatcher.process_update(update)
    return "ok"

# ===== RUN SERVER =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
